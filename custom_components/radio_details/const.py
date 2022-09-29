"""Constants for the Portuguese Radio Details integration."""

DOMAIN = "radio_details"

DOMAIN_DATA_RADIO_NAME = "radio_name"

DEVICE_UNIQUE_ID = "7681a449-de10-407f-98f0-d0a6cd8a0468"
DEVICE_DEFAULT_NAME = "Radio Details"
DEVICE_MANUFACTURER = "Pedro Miguel Fernandes"
DEVICE_DEFAULT_MODEL = "Radios"
DEVICE_SW_VERSION = "1.0.0.0"

ENTITY_TYPE_MUSIC = "Music"
ENTITY_TYPE_ALBUM = "Album"
ENTITY_TYPE_ARTIST = "Artist"

RADIONAME_RADIO_COMERCIAL = "Rádio Comercial"
RADIONAME_CIDADE_FM = "Cidade FM"
RADIONAME_M80 = "M80"
RADIONAME_MEGA_HITS = "MegaHits"
RADIONAME_RFM = "RFM"

BASE_HOST_RADIO_COMERCIAL = "https://radiocomercial.iol.pt/nowplaying.xml"
BASE_HOST_CIDADE_FM = "https://cidade.iol.pt/nowplaying.xml"
BASE_HOST_M80 = "https://m80.iol.pt/nowplaying.xml"
BASE_HOST_RFM = "https://configsa01.blob.core.windows.net/rfm/rfmOnAir.xml"
BASE_HOST_MEGAHITS = "https://configsa01.blob.core.windows.net/megahits/megaOnAir.xml"

DEFAULT_IMAGE_RADIO_COMERCIAL = "https://www.mcradios.pt/facebook/RadioComercial/images/webradios/webradiosRC_EMDIRETO.jpg"
DEFAULT_IMAGE_CIDADE_FM = "https://cidade.iol.pt/images/logo_CIDADE_2020.png"
DEFAULT_IMAGE_M80 = "https://m80.iol.pt/upload/W/webradio-m80-fm1.jpg"
DEFAULT_IMAGE_RFM = (
    "https://cdnimages01.azureedge.net/rfm/default300x3002255339a_117162246.jpg"
)
DEFAULT_IMAGE_MEGAHITS = "https://cdnimages01.azureedge.net/megahits/mega_hits_default_1200x12002084df94_socialshare.jpg"
