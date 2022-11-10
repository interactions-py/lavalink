from typing import List

from lavalink import AudioTrack, DefaultPlayer

from interactions import Client

__all__ = ("Player",)


class Player(DefaultPlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._bot: Client = None

    async def search_youtube(self, query: str) -> List[AudioTrack]:
        res = await self.node.get_tracks(f"ytsearch: {query}")
        return res.tracks

    async def search_soundcloud(self, query: str) -> List[AudioTrack]:
        res = await self.node.get_tracks(f"scsearch: {query}")
        return res.tracks

    async def get_tracks(self, url: str) -> List[AudioTrack]:
        res = await self.node.get_tracks(url)
        return res.tracks
