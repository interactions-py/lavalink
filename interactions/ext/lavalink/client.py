from typing import Dict, List, Union, Optional

from lavalink import Client as LavalinkClient
from lavalink import DefaultPlayer

from interactions import Client, Snowflake

from .models import VoiceState
from .websocket import VoiceWebSocketClient

__all__ = ["VoiceClient"]


class VoiceClient(Client):
    def __init__(self, token: str, **kwargs):
        super().__init__(token, **kwargs)

        self._websocket = VoiceWebSocketClient(token, self._intents)
        self.lavalink_client = LavalinkClient(int(self.me.id))

        self._websocket._dispatch.register(
            self.__raw_voice_state_update, "on_raw_voice_state_update"
        )
        self._websocket._dispatch.register(
            self.__raw_voice_server_update, "on_raw_voice_server_update"
        )

    async def __raw_voice_state_update(self, data: dict):
        lavalink_data = {"t": "VOICE_STATE_UPDATE", "d": data}
        await self.lavalink_client.voice_update_handler(lavalink_data)

    async def __raw_voice_server_update(self, data: dict):
        lavalink_data = {"t": "VOICE_SERVER_UPDATE", "d": data}
        await self.lavalink_client.voice_update_handler(lavalink_data)

    async def connect(
        self,
        guild_id: Union[Snowflake, int, str],
        channel_id: Union[Snowflake, int, str],
        self_deaf: bool = False,
        self_mute: bool = False,
    ) -> DefaultPlayer:
        """
        Connects to voice channel and creates player.

        :param guild_id: The guild id to connect.
        :type guild_id: Union[Snowflake, int, str]
        :param channel_id: The channel id to connect.
        :type channel_id: Union[Snowflake, int, str]
        :param self_deaf: Whether bot is self deafened
        :type self_deaf: bool
        :param self_mute: Whether bot is self muted
        :type self_mute: bool
        :return: Created guild player.
        :rtype: DefaultPlayer
        """
        await self._websocket.connect_voice_channel(guild_id, channel_id, self_deaf, self_mute)
        player = self.lavalink_client.player_manager.get(int(guild_id))
        if player is None:
            player = self.lavalink_client.player_manager.create(int(guild_id))
        return player

    async def disconnect(self, guild_id: Union[Snowflake, int]):
        await self._websocket.disconnect_voice_channel(int(guild_id))
        await self.lavalink_client.player_manager.destroy(int(guild_id))

    def get_player(self, guild_id: Union[Snowflake, int]) -> DefaultPlayer:
        return self.lavalink_client.player_manager.get(int(guild_id))

    @property
    def voice_states(self) -> Dict[Snowflake, VoiceState]:
        """Returns dict of cached voice states"""
        return self._http.cache[VoiceState].values

    def get_user_voice_state(self, user_id: Union[Snowflake, int]) -> Optional[VoiceState]:
        """
        Returns user voice state.

        :param user_id: The user id
        :type user_id: Union[Snowflake, int]
        :return: Founded user voice state else nothing
        :rtype: Optional[VoiceState]
        """

        _user_id = Snowflake(user_id) if isinstance(user_id, int) else user_id
        return self._http.cache[VoiceState].get(_user_id)

    def get_guild_voice_states(self, guild_id: Union[Snowflake, int]):
        """
        Returns channel voice states.

        :param guild_id: The channel id
        :type guild_id: Union[Snowflake, int]
        :return: Founded channel voice states else nothing
        :rtype: Optional[List[VoiceState]]
        """

        _guild_id = Snowflake(guild_id) if isinstance(guild_id, int) else guild_id
        return [
            voice_state
            for voice_state in self.voice_states.values()
            if voice_state.guild_id == _guild_id
        ]

    def get_channel_voice_states(self, channel_id: Union[Snowflake, int]) -> Optional[List[VoiceState]]:
        """
        Returns channel voice states.

        :param channel_id: The channel id
        :type channel_id: Union[Snowflake, int]
        :return: Founded channel voice states else nothing
        :rtype: Optional[List[VoiceState]]
        """

        _channel_id = Snowflake(channel_id) if isinstance(channel_id, int) else channel_id
        return [
            voice_state
            for voice_state in self.voice_states.values()
            if voice_state.channel_id == _channel_id
        ]
