"""Built-in device feature providers."""

from benchcalm.features.base import FeatureProvider
from benchcalm.features.cpu import CpuFeature


def get_feature_providers() -> tuple[FeatureProvider, ...]:
    """Return the built-in feature providers in stable display order."""

    return (CpuFeature(),)