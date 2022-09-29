"""Platform for sensor integration."""

from __future__ import annotations

from datetime import timedelta
import logging

import aiohttp

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN
from .const import (
    DEVICE_DEFAULT_MODEL,
    DEVICE_MANUFACTURER,
    DEVICE_SW_VERSION,
    DEVICE_UNIQUE_ID,
    DOMAIN_DATA_RADIO_NAME,
    ENTITY_TYPE_ALBUM,
    ENTITY_TYPE_ARTIST,
    ENTITY_TYPE_MUSIC,
)
from .radiostation import RadioStation

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

# Time between updating data from API
SCAN_INTERVAL = timedelta(seconds=5)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    radio_name = hass.data[DOMAIN][DOMAIN_DATA_RADIO_NAME]

    session = async_get_clientsession(hass, True)
    radio_station = RadioStation(session)
    radio_station_details = await radio_station.get_station_details(radio_name)

    async_add_entities(
        [
            BaseSensor(
                hass=hass,
                station=radio_station,
                unique_id="radio_music",
                name="Music",
                entity_type=ENTITY_TYPE_MUSIC,
                icon="mdi:speaker",
                state=radio_station_details.music,
            ),
            BaseSensor(
                hass=hass,
                station=radio_station,
                unique_id="radio_album",
                name="Album",
                entity_type=ENTITY_TYPE_ALBUM,
                icon="mdi:file-music",
                state=radio_station_details.album,
            ),
            BaseSensor(
                hass=hass,
                station=radio_station,
                unique_id="radio_artist",
                name="Artist",
                entity_type=ENTITY_TYPE_ARTIST,
                icon="mdi:account",
                state=radio_station_details.artist,
            ),
        ]
    )


class BaseSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        station: RadioStation,
        unique_id: str,
        name: str,
        entity_type: str,
        icon: str,
        state: str,
    ) -> None:
        """Initialize the sensor."""
        self._hass = hass
        self._station = station
        # self._state = state
        self._available = True
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._attr_icon = icon
        self._attr_native_value = state
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, DEVICE_UNIQUE_ID)},
            name=name,
            manufacturer=DEVICE_MANUFACTURER,
            default_model=DEVICE_DEFAULT_MODEL,
            sw_version=DEVICE_SW_VERSION,
        )
        self._entity_type = entity_type

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def entity_type(self) -> str:
        """Return True if entity is available."""
        return self._entity_type

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            station = self._station

            radio_name = self._hass.data[DOMAIN][DOMAIN_DATA_RADIO_NAME]

            radio_comercial = await station.get_station_details(radio_name)
            if radio_comercial:
                if self.entity_type == ENTITY_TYPE_MUSIC:
                    self._attr_native_value = radio_comercial.music
                if self.entity_type == ENTITY_TYPE_ALBUM:
                    self._attr_native_value = radio_comercial.album
                if self.entity_type == ENTITY_TYPE_ARTIST:
                    self._attr_native_value = radio_comercial.artist
        except aiohttp.ClientError as err:
            self._available = False
            _LOGGER.exception("Error updating data from Station. %s", err)
