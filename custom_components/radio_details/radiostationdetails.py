"""Represents a Radio Station Details."""


class RadioStationDetails:
    """Represents a Radio Station Details."""

    def __init__(
        self, name: str, artist: str, album: str, music: str, image: str
    ) -> None:
        """Radio Station details initialization."""
        self.name = name
        self.artist = artist
        self.album = album
        self.music = music
        self.image = image
