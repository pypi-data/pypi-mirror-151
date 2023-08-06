from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from textwrap import dedent
from time import time
from typing import (
    Any,
    Callable,
    Collection,
    Iterable,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
)

from atoti_core import JavaType, keyword_only_dataclass, parse_java_type
from py4j.java_collections import ListConverter

from .._java_api import JavaApi
from .._operation import JavaFunctionOperation, Operation
from .._py4j_utils import to_python_list
from .java_operation_element import JavaOperationElement

_METHOD_TEMPLATE = dedent(
    """\
    public {output_type} {method_name}({input_string}) {{
        {method_body}
    }}
"""
)

_UDAF_TYPES: Mapping[JavaType, str] = {
    "double": "double",
    "float": "float",
    "long": "long",
    "int": "int",
    "double[]": "IVector",
    "float[]": "IVector",
    "long[]": "IVector",
    "int[]": "IVector",
}

_TYPE_CONSTRAINTS: Mapping[JavaType, Iterable[JavaType]] = {
    "double": ["double", "float", "long", "int"],
    "float": ["float", "long", "int"],
    "long": ["long", "int"],
    "int": ["int"],
    "double[]": ["double[]"],
    "float[]": ["float[]"],
    "long[]": ["long[]"],
    "int[]": ["int[]"],
    "Object": ["Object"],
}


@keyword_only_dataclass
@dataclass(frozen=True, eq=False)
class AppliedJavaFunctionOperation(JavaFunctionOperation):
    _underlyings: Sequence[Operation]
    _java_function: JavaFunction

    @property
    def java_function(self) -> JavaFunction:
        return self._java_function

    @property
    def underlyings(self) -> Sequence[Operation]:
        return self._underlyings


class JavaFunction(ABC):
    @abstractmethod
    def add_method_source_codes(self, method_codes: Set[str]) -> None:
        """Adds the source code of methods to be declared in the compiled Java class."""
        ...

    @abstractmethod
    def update_class_imports(self, additional_imports: Set[str]) -> None:
        """Updates the class's imports with the requirements for this function."""
        ...

    @abstractmethod
    def get_output_type_function(
        self,
    ) -> Callable[[Iterable[JavaOperationElement], JavaApi], JavaType]:
        """Get the output type of the function."""
        ...

    def __call__(self, *values: Any) -> JavaFunctionOperation:
        """Apply this function to the passed values."""
        from .._operation import _to_operation

        operations = [_to_operation(value) for value in values]
        return AppliedJavaFunctionOperation(
            _underlyings=operations, _java_function=self
        )

    @abstractmethod
    def get_java_source_code(
        self, *operation_elements: JavaOperationElement, java_api: JavaApi
    ) -> str:
        """Generate and return the Java source code which calls this function on the passed operation elements."""
        ...


class CustomJavaFunction(JavaFunction):
    """A custom Java function which can be applied to constants, columns or operations."""

    def __init__(
        self,
        *signatures: Sequence[Tuple[str, JavaType]],
        method_name: str,
        method_body: str,
        output_type: JavaType,
        additional_imports: Optional[Set[str]] = None,
    ):
        """Creates a new JavaFunction.

        Args:
            signatures: Sequence of tuples containing the variable name and type, used to declare the method.
            method_name: The name of the method, this should be unique.
            method body: The java code to be executed inside the method.
            output_type: The data type of the output.
            additional_imports: Java packages which need importing for the function to work.
        """
        self.inputs = signatures
        self.signatures: Sequence[Sequence[JavaType]] = [
            [input[1] for input in signature] for signature in signatures
        ]
        self.method_name = f"{method_name}{round(time())}"
        self.method_body = method_body
        self.output_type: JavaType = output_type
        self.additional_imports = additional_imports

    def update_class_imports(self, additional_imports: Set[str]) -> None:
        if self.additional_imports is not None:
            additional_imports.update(self.additional_imports)

    def add_method_source_codes(self, method_codes: Set[str]) -> None:
        method_implementations = [
            self.get_java_method_code(signature) for signature in self.inputs
        ]
        method_codes.update(method_implementations)

    def get_output_type_function(
        self,
    ) -> Callable[[Iterable[JavaOperationElement], JavaApi], JavaType]:
        def output_type(
            _ignored: Iterable[JavaOperationElement], _java_api: JavaApi
        ) -> JavaType:
            return self.output_type

        return output_type

    def get_java_method_code(
        self, selected_signature: Sequence[Tuple[str, JavaType]]
    ) -> str:
        """Generate the Java code corresponding to this method's declaration."""
        inputs = [f"{_UDAF_TYPES[input[1]]} {input[0]}" for input in selected_signature]
        input_string = ",".join(inputs)
        return _METHOD_TEMPLATE.format(
            input_string=input_string,
            method_body=self.method_body,
            method_name=self.method_name,
            output_type=_UDAF_TYPES[self.output_type],
        )

    def get_java_source_code(
        self,
        *operation_elements: JavaOperationElement,
        java_api: JavaApi,  # pylint: disable=unused-argument
    ) -> str:
        can_call = is_signature_valid(self.signatures, operation_elements)
        if not can_call:
            raise ValueError(
                "Couldn't find any compatible signatures for this function."
            )
        operation_strings = [
            operation.get_java_source_code() for operation in operation_elements
        ]
        parameter_string = ",".join(operation_strings)
        return f"{self.method_name}({parameter_string})"


@keyword_only_dataclass
@dataclass(frozen=True)
class ExistingJavaFunction(JavaFunction):
    """Function used to call static Java methods.

    Args:
        method_call_string: The string to be used to call the method without the brackets. e.g: "Math.sum"
        import_package: Package to be imported to make the method accessible.
    """

    method_call_string: str
    import_package: Optional[str] = None

    def get_java_source_code(
        self, *operation_elements: JavaOperationElement, java_api: JavaApi
    ) -> str:
        signatures = self._get_signature_from_java(java_api)
        can_call = is_signature_valid(signatures, operation_elements)

        if not can_call:
            raise ValueError("No compatible signatures found for this method.")

        operation_strings = ",".join(
            operationElement.get_java_source_code()
            for operationElement in operation_elements
        )

        return f"{self.method_call_string}({operation_strings})"

    def _get_signature_from_java(
        self, java_api: JavaApi
    ) -> Sequence[Sequence[JavaType]]:
        """Get the method's signature from the JVM."""
        components = self.method_call_string.split(".")
        clazz = components[0]
        method_name = components[1]
        full_class = f"{self.import_package}.{clazz}"
        java_signatures: Any = (
            java_api.gateway.jvm.io.atoti.udaf.util.UdafCompiler.getMethodSignatures(
                full_class, method_name
            )
        )
        python_signatures = to_python_list(java_signatures)
        signatures: Sequence[Sequence[JavaType]] = [
            [parse_java_type(argument) for argument in to_python_list(signature)]
            for signature in python_signatures
        ]
        return signatures

    def _get_output_type_function(
        self,
    ) -> Callable[[Iterable[JavaOperationElement], JavaApi], JavaType]:
        components = self.method_call_string.split(".")
        clazz = components[0]
        java_method = components[1]
        java_class = f"{self.import_package}.{clazz}"

        def output_type_function(
            operation_elements: Iterable[JavaOperationElement], java_api: JavaApi
        ) -> JavaType:
            java_types = [
                _UDAF_TYPES[operation_element.output_type]
                for operation_element in operation_elements
            ]
            return get_output_type_from_java(
                java_class=java_class,
                java_method=java_method,
                types=java_types,
                java_api=java_api,
            )

        return output_type_function

    def get_output_type_function(
        self,
    ) -> Callable[[Iterable[JavaOperationElement], JavaApi], JavaType]:
        return self._get_output_type_function()

    def update_class_imports(self, additional_imports: Set[str]) -> None:
        if self.import_package:
            additional_imports.add(self.import_package)

    def add_method_source_codes(self, method_codes: Set[str]) -> None:
        pass


def is_signature_valid(
    signatures: Iterable[Collection[JavaType]],
    operation_elements: Collection[JavaOperationElement],
) -> bool:
    """Ensure that the operations' types are compatible with at least one signature."""
    for signature in signatures:
        if len(signature) != len(operation_elements):
            pass

        if all(
            operationElement.output_type in _TYPE_CONSTRAINTS.get(input_type, [])
            for operationElement, input_type in zip(operation_elements, signature)
        ):
            return True

    return False


def get_output_type_from_java(
    *, java_class: str, java_method: str, types: Iterable[str], java_api: JavaApi
) -> JavaType:
    java_types = ListConverter().convert(types, java_api.gateway._gateway_client)
    output_type: str = (
        java_api.gateway.jvm.io.atoti.udaf.util.UdafCompiler.getMethodOutputType(
            java_class, java_method, java_types
        )
    )
    return parse_java_type(output_type)
