from typing import Union

from lavalink import Client as LavalinkClient
import lavalink.events

from interactions import Client, Snowflake_Type, to_snowflake
from interactions.api.events.base import RawGatewayEvent

from .player import Player
from . import events

__all__ = ("Lavalink", )


class Lavalink:
    def __init__(self, bot: Client):
        self._bot: Client = bot
        self.client: LavalinkClient | None = None

        self._bot.listen()(self.__on_raw_voice_state_update)
        self._bot.listen()(self.__on_raw_voice_server_update)

    async def __on_raw_voice_state_update(self, event: RawGatewayEvent):
        await self.client.voice_update_handler(
            {"t": "VOICE_STATE_UPDATE", "d": event.data}
        )

    async def __on_raw_voice_server_update(self, event: RawGatewayEvent):
        await self.client.voice_update_handler(
            {"t": "VOICE_SERVER_UPDATE", "d": event.data}
        )

    def add_node(
        self,
        host: str,
        port: int,
        password: str,
        region: str,
        resume_key: str = None,
        resume_timeout: int = 60,
        name: str = None,
        reconnect_attempts: int = 3,
        filters: bool = True,
        ssl: bool = False,
    ):
        if self.client is None:
            self.__init_lavalink()

        return self.client.add_node(
            host=host,
            port=port,
            password=password,
            region=region,
            resume_key=resume_key,
            resume_timeout=resume_timeout,
            name=name,
            reconnect_attempts=reconnect_attempts,
            filters=filters,
            ssl=ssl,
        )

    def __init_lavalink(self):
        self.client = LavalinkClient(int(self._bot.user.id), player=Player)
        self.client.add_event_hook(self._dispatch_lavalink_event)

    def get_player(self, guild_id: Snowflake_Type) -> Player | None:
        """
        Gets guild's current player.

        :param Snowflake_Type guild_id: The ID of the guild
        :return: Player, if any.
        """
        return self.client.player_manager.get(to_snowflake(guild_id))

    def create_player(self, guild_id: Snowflake_Type) -> Player:
        """
        Creates a new player for the guild

        :param Snowflake_Type guild_id: The ID of the guild
        :return: Created player
        """
        player = self.client.player_manager.create(to_snowflake(guild_id))
        player._bot = self._bot

        return player  # type: ignore

    async def connect(
        self,
        guild_id: Snowflake_Type,
        channel_id: Snowflake_Type,
        self_deaf: bool = False,
        self_mute: bool = False,
    ) -> Player:
        """
        Connects to voice channel and creates player.

        :param Union[Snowflake, int, str] guild_id: The guild id to connect.
        :param Union[Snowflake, int, str] channel_id: The channel id to connect.
        :param bool self_deaf: Whether bot is self deafened
        :param bool self_mute: Whether bot is self muted
        :return: Created guild player.
        :rtype: Player
        """
        _guild_id = to_snowflake(guild_id)

        websocket = self._bot.get_guild_websocket(_guild_id)
        await websocket.voice_state_update(_guild_id, to_snowflake(channel_id), muted=self_mute, deafened=self_deaf)

        return self.get_player(_guild_id) or self.create_player(_guild_id)

    async def disconnect(self, guild_id: Snowflake_Type):
        """
        :param Union[Snowflake, int, str] guild_id: The guild id to disconnect from.
        """
        _guild_id = to_snowflake(guild_id)
        websocket = self._bot.get_guild_websocket(_guild_id)
        await websocket.voice_state_update(_guild_id, None)  # type: ignore

        await self.client.player_manager.destroy(_guild_id)

    async def _dispatch_lavalink_event(self, event: lavalink.events.Event):
        # TODO: uhh
        match event:
            case lavalink.events.NodeConnectedEvent():
                print(1)
                _event = events.NodeConnected(event.node)

        self._bot.dispatch(_event)

    async def __raw_socket_create(self, name: str, data: dict):
        if name not in {"VOICE_STATE_UPDATE", "VOICE_SERVER_UPDATE"}:
            return

        _data: dict = {"t": name, "d": data}
        await self.client.voice_update_handler(_data)

    async def __update_voice_state(
        self,
        guild_id: int,
        channel_id: int = None,
        self_deaf: bool = None,
        self_mute: bool = None,
    ):
        """
        Sends VOICE_STATE packet to websocket.

        :param int guild_id: The guild id.
        :param int channel_id: The channel id.
        :param bool self_deaf: Whether bot is self deafened
        :param bool self_mute: Whether bot is self muted
        """
        payload = {
            "op": OpCodeType.VOICE_STATE,
            "d": {
                "guild_id": str(guild_id),
                "channel_id": str(channel_id) if channel_id is not None else None,
            },
        }

        if self_deaf is not None:
            payload["d"]["self_deaf"] = self_deaf
        if self_mute is not None:
            payload["d"]["self_mute"] = self_mute

        await self._bot._websocket._send_packet(payload)
