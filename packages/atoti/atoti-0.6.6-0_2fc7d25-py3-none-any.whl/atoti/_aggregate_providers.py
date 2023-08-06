from typing import Any, Callable, Dict, Mapping, Sequence

from ._aggregate_provider import AggregateProvider
from ._aggregate_provider_arguments import AggregateProviderArguments
from ._delegate_mutable_mapping import DelegateMutableMapping
from ._java_api import JavaApi


class AggregateProviders(DelegateMutableMapping[str, AggregateProvider]):
    def __init__(
        self,
        *,
        cube_name: str,
        get_aggregate_provider: Callable[
            [AggregateProviderArguments], AggregateProvider
        ],
        java_api: JavaApi,
    ):
        self._java_api = java_api
        self._cube_name = cube_name
        self._argument_to_provider = get_aggregate_provider

    def __delitem__(self, key: Any) -> None:
        raise NotImplementedError("Operation not supported")

    def _update(self, other: Mapping[str, AggregateProvider]) -> None:
        self._java_api.set_aggregate_providers(
            self._cube_name,
            providers_to_arguments(other),
        )
        self._java_api.refresh()

    def __setitem__(self, key: str, value: AggregateProvider) -> None:
        self._update({key: value})

    def _get_underlying(self) -> Dict[str, AggregateProvider]:
        return {
            provider_arguments.name: self._argument_to_provider(provider_arguments)
            for provider_arguments in self._java_api.get_aggregate_providers_attributes(
                self._cube_name
            )
        }


def providers_to_arguments(
    mapping: Mapping[str, AggregateProvider]
) -> Sequence[AggregateProviderArguments]:
    return [provider._to_arguments(name=name) for name, provider in mapping.items()]
