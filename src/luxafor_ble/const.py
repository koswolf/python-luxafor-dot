"""BLE Constants.

UUIDs and other constants for communicating with Dot devices.
"""
from __future__ import annotations

import platform
import re
from enum import IntEnum
from functools import cached_property
from uuid import UUID

# Bluetooth names of supported devices. We only check the first 7 chars
LUXAFOR_BLUETOOTH_NAMES: tuple[str, ...] = ("lux dot",)

# Format for all Luxafor's BLE UUIDs
UUID_TEMPLATE = "0000{:0>4x}-0000-1000-8000-00805f9b34fb"
MAC_ADDRESS_REGEX = re.compile(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$")


# Placeholder value to fill in blank values
LUXAFOR_DONT_CARE = 0x00

IS_LINUX = platform.system() == "Linux"


class DotCharacteristic(IntEnum):
    """BLE Characteristics of Dot devices."""

    # Characteristic UUIDS (see luxafor_bt_control.xlsx)
    # Note error in R/W chararacteristic listed in doc
    SERVICE = 0x1234
    LED_COMMAND = 0x1235  # Used to set the color/pattern of the Dot device
    STATUS = 0x1236  # Reports back status of Dot.

    @cached_property
    def uuid(self) -> UUID:
        """Convert the short ID to a full UUID and caches value.

        Returns:
            UUID: UUID for BLE usage
        """
        return UUID(UUID_TEMPLATE.format(self.value))

    def __str__(self) -> str:
        """Get UUID as the string representation.

        Returns:
            str: UUID in string format
        """
        return str(self.uuid)


class LuxaforLED(IntEnum):
    """LEDs on the device."""

    LEFT = 1
    RIGHT = 2
    ALL = 255


class LuxaforCommand(IntEnum):
    """Acceptable commands for the device."""

    COLOR = 0xA1
    FADE = 0xA2
    STROBE = 0xA3
    WAVE = 0xA4
    PATTERN = 0xA6


class LuxaforWavePattern(IntEnum):
    """Available wave patterns for the device."""

    PATTERN_1 = 1
    PATTERN_2 = 2
    PATTERN_3 = 3
    PATTERN_4 = 4
    PATTERN_5 = 5


class LuxaforPattern(IntEnum):
    """Available patterns for the device."""

    PATTERN_POLICE = 5
    PATTERN_RAINBOW = 8
    PATTERN_STOPLIGHT = 1

    PATTERN_RANDOM1 = 2
    PATTERN_RANDOM2 = 3
    PATTERN_RANDOM3 = 4
    PATTERN_RANDOM4 = 6
    PATTERN_RANDOM5 = 7


class PushEvent(IntEnum):
    """Expected responses from the device."""

    MALFORMED = 0x30
    """Sent any time the device does not understand."""

    OKAY = 0x31
    """Sent when the command is accepted."""

    WAKEUP = 0x32
    """Sent when the device is asleep (flashing red) and wakes up."""

    HELLO = 0x33
    """Sent when the device is about to go to sleep, approx every 30 sec."""
