"""Linux CPU frequency-control discovery."""

import os
from pathlib import Path

from benchcalm.features.base import ControlReport, FeatureReport


class CpuFeature:
    """Discover CPU frequency policies exposed through Linux cpufreq sysfs."""

    def __init__(self, sysfs_root: Path = Path("/sys/devices/system/cpu/cpufreq")) -> None:
        self.sysfs_root = sysfs_root

    def discover(self) -> FeatureReport:
        policies = sorted(self.sysfs_root.glob("policy[0-9]*"))
        if not policies:
            return FeatureReport(
                id="cpu",
                name="CPU frequency controls",
                status="unsupported",
                risk="context-dependent",
                controls=(),
                details="No cpufreq policy directories were found.",
            )

        controls: list[ControlReport] = []
        for policy in policies:
            controls.extend(self._discover_policy(policy))

        return FeatureReport(
            id="cpu",
            name="CPU frequency controls",
            status="supported",
            risk="context-dependent",
            controls=tuple(controls),
            details=f"Detected {len(policies)} cpufreq policy director{'y' if len(policies) == 1 else 'ies'}.",
        )

    def _discover_policy(self, policy: Path) -> list[ControlReport]:
        available_governors = self._read_tokens(policy / "scaling_available_governors")
        controls: list[ControlReport] = []
        for attribute, display_name, options in (
            ("scaling_governor", "Governor", available_governors),
            ("scaling_min_freq", "Minimum frequency (kHz)", ()),
            ("scaling_max_freq", "Maximum frequency (kHz)", ()),
        ):
            path = policy / attribute
            current = self._read_value(path)
            controls.append(
                ControlReport(
                    id=f"cpu.{policy.name}.{attribute.removeprefix('scaling_')}",
                    name=f"{policy.name} {display_name}",
                    current=current,
                    available_values=options,
                    writable=current is not None and os.access(path, os.W_OK),
                    status="available" if current is not None else "unavailable",
                )
            )
        return controls

    @staticmethod
    def _read_value(path: Path) -> str | None:
        try:
            return path.read_text(encoding="utf-8").strip()
        except OSError:
            return None

    @classmethod
    def _read_tokens(cls, path: Path) -> tuple[str, ...]:
        value = cls._read_value(path)
        return tuple(value.split()) if value else ()