from typing import List

from lavalink import AudioTrack, DefaultPlayer


class Player(DefaultPlayer):
    async def search_youtube(self, query: str) -> List[AudioTrack]:
        res = await self.node.get_tracks(f"ytsearch: {query}")
        return res.tracks

    async def search_soundcloud(self, query: str) -> List[AudioTrack]:
        res = await self.node.get_tracks(f"scsearch: {query}")
        return res.tracks

    async def get_tracks(self, url: str) -> List[AudioTrack]:
        res = await self.node.get_tracks(url)
        return res.tracks
