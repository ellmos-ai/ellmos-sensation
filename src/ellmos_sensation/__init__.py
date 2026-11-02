"""ellmos-sensation: Permission-gated device perception & Open-Compute presence gate."""

from .sensor_hub import (
    AmbientObservation,
    CameraPresenceSensor,
    MicrophoneAmbientSensor,
    OpenComputePresenceGate,
    PresenceObservation,
    SensationHub,
    SensationPermissions,
    SoundSynthesizer,
)

__all__ = [
    "AmbientObservation",
    "CameraPresenceSensor",
    "MicrophoneAmbientSensor",
    "OpenComputePresenceGate",
    "PresenceObservation",
    "SensationHub",
    "SensationPermissions",
    "SoundSynthesizer",
]

__version__ = "0.1.0"
