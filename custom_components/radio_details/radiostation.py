"""API to Radio stations."""
import logging

import aiohttp
from defusedxml.ElementTree import fromstring

from .const import (
    BASE_HOST_CIDADE_FM,
    BASE_HOST_M80,
    BASE_HOST_MEGAHITS,
    BASE_HOST_RADIO_COMERCIAL,
    BASE_HOST_RFM,
    RADIONAME_CIDADE_FM,
    RADIONAME_M80,
    RADIONAME_MEGA_HITS,
    RADIONAME_RADIO_COMERCIAL,
    RADIONAME_RFM,
)
from .radiostationdetails import RadioStationDetails

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class RadioStation:
    """Interfaces to Radio Stations."""

    def __init__(self, websession) -> None:
        """Radio Station initialization."""
        self.websession = websession

    async def get_station_details(self, radio_name: str) -> RadioStationDetails:
        """Issue get station details."""

        if radio_name == RADIONAME_RADIO_COMERCIAL:
            host = BASE_HOST_RADIO_COMERCIAL
        if radio_name == RADIONAME_CIDADE_FM:
            host = BASE_HOST_CIDADE_FM
        if radio_name == RADIONAME_M80:
            host = BASE_HOST_M80
        if radio_name == RADIONAME_RFM:
            host = BASE_HOST_RFM
        if radio_name == RADIONAME_MEGA_HITS:
            host = BASE_HOST_MEGAHITS

        if radio_name in (
            RADIONAME_RADIO_COMERCIAL,
            RADIONAME_CIDADE_FM,
            RADIONAME_M80,
        ):
            return await MediaCapitalStation(
                self.websession, host
            ).get_station_details()

        return await RenascencaStation(self.websession, host).get_station_details()


class MediaCapitalStation:
    """Interfaces to Media Capital stations."""

    def __init__(self, websession, base_host: str):
        """Media Capital station initizalition."""
        self.websession = websession
        self.base_host = base_host

    async def get_station_details(self):
        """Issue get station details."""
        try:
            _LOGGER.debug("Fetching details for station")
            async with self.websession.get(self.base_host) as res:
                if res.status == 200:
                    xml_text = await res.text()

                    root = fromstring(xml_text)

                    artist_value = await self.get_content_from_result(
                        root, "DB_LEAD_ARTIST_NAME"
                    )
                    radio_value = await self.get_content_from_result(
                        root, "DB_RADIO_NAME"
                    )
                    album_value = await self.get_content_from_result(
                        root, "DB_ALBUM_NAME"
                    )
                    claim_value = await self.get_content_from_result(root, "CLAIM")
                    song_value = await self.get_content_from_result(
                        root, "DB_SONG_NAME"
                    )
                    title_value = await self.get_content_from_result(
                        root, "DB_DALET_TITLE_NAME"
                    )
                    album_image_value = await self.get_content_from_result(
                        root, "DB_ALBUM_IMAGE"
                    )
                    alternative_image_value = await self.get_content_from_result(
                        root, "DB_ALT_COVER_IMAGE"
                    )

                    artist = artist_value if artist_value is not None else radio_value
                    album = album_value if album_value is not None else claim_value
                    music = song_value if song_value is not None else title_value
                    image = (
                        album_image_value
                        if album_image_value is not None
                        else (
                            alternative_image_value
                            if alternative_image_value is not None
                            else ""
                        )
                    )

                    radio_station = RadioStationDetails(
                        "Radio Comercial", artist, album, music, image
                    )

                    return radio_station
                # raise Exception("Could not retrieve details for statio")
        except aiohttp.ClientError as err:
            _LOGGER.error(err)

    async def get_content_from_result(self, radio_details, element_name: str):
        """Get element from xml."""

        for name in radio_details.iter(element_name):
            return name.text


class RenascencaStation:
    """Interfaces to Media Capital stations."""

    def __init__(self, websession, base_host: str):
        """Renascenca initialization."""
        self.websession = websession
        self.base_host = base_host

    async def get_station_details(self):
        """Issue get station details."""
        try:
            _LOGGER.debug("Fetching details for station")
            async with self.websession.get(self.base_host) as res:
                if res.status == 200:
                    xml_text = await res.text()

                    root = fromstring(xml_text)

                    album = ""
                    artist = await self.get_content_from_result(root, "artist")
                    music = await self.get_content_from_result(root, "name")
                    image = await self.get_content_from_result(root, "capa")

                    radio_station = RadioStationDetails(
                        "RFM", artist, album, music, image
                    )

                    return radio_station
        except aiohttp.ClientError as err:
            _LOGGER.error(err)

    async def get_content_from_result(self, radio_details, element_name: str):
        """Get element from xml."""

        for name in radio_details.iter(element_name):
            return name.text
