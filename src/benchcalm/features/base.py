"""Shared data types for independently implemented feature providers."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ControlReport:
    """Read-only snapshot of one configurable system control."""

    id: str
    name: str
    current: str | None
    available_values: tuple[str, ...]
    writable: bool
    status: str


@dataclass(frozen=True)
class FeatureReport:
    """Discovery result for a device feature such as CPU or GPU."""

    id: str
    name: str
    status: str
    risk: str
    controls: tuple[ControlReport, ...]
    details: str | None = None


class FeatureProvider(Protocol):
    """Contract implemented by each built-in feature provider."""

    def discover(self) -> FeatureReport:
        """Return the currently detectable state without changing the system."""