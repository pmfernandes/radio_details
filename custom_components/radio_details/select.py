"""Select entities for the Portuguese Radio Details integration."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN
from .const import (
    DEVICE_DEFAULT_MODEL,
    DEVICE_DEFAULT_NAME,
    DEVICE_MANUFACTURER,
    DEVICE_SW_VERSION,
    DEVICE_UNIQUE_ID,
    DOMAIN_DATA_RADIO_NAME,
    RADIONAME_CIDADE_FM,
    RADIONAME_M80,
    RADIONAME_MEGA_HITS,
    RADIONAME_RADIO_COMERCIAL,
    RADIONAME_RFM,
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the radio Select entity."""
    async_add_entities(
        [
            RadioSelect(
                hass=hass,
                unique_id="radio",
                name="Radio",
                icon="mdi:radio",
                current_option="Rádio Comercial",
                options=[
                    RADIONAME_RADIO_COMERCIAL,
                    RADIONAME_CIDADE_FM,
                    RADIONAME_M80,
                    RADIONAME_MEGA_HITS,
                    RADIONAME_RFM,
                ],
            ),
        ]
    )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Radio config entry."""

    await async_setup_platform(hass, {}, async_add_entities)


class RadioSelect(SelectEntity):
    """Representation of a radio select entity."""

    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        unique_id: str,
        name: str,
        icon: str,
        current_option: str | None,
        options: list[str],
    ) -> None:
        """Initialize the radio select entity."""
        self._hass = hass
        self._attr_unique_id = unique_id
        self._attr_name = name or DEVICE_DEFAULT_NAME
        self._attr_current_option = current_option
        self._attr_icon = icon
        self._attr_options = options
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, DEVICE_UNIQUE_ID)},
            name=name,
            manufacturer=DEVICE_MANUFACTURER,
            default_model=DEVICE_DEFAULT_MODEL,
            sw_version=DEVICE_SW_VERSION,
        )

        self._hass.data[DOMAIN][DOMAIN_DATA_RADIO_NAME] = current_option

    async def async_select_option(self, option: str) -> None:
        """Update the current selected option."""
        self._attr_current_option = option
        self._hass.data[DOMAIN][DOMAIN_DATA_RADIO_NAME] = option
        self.async_write_ha_state()
