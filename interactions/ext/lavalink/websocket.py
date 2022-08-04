from interactions import OpCodeType, Storage, WebSocketClient

from .models import VoiceServer, VoiceState

__all__ = ["VoiceWebSocketClient"]


class VoiceWebSocketClient(WebSocketClient):
    def __init__(self, *args):
        super().__init__(*args)

    def _dispatch_event(self, event: str, data: dict) -> None:
        if event not in ("VOICE_STATE_UPDATE", "VOICE_SERVER_UPDATE"):
            return super()._dispatch_event(event, data)

        self._dispatch.dispatch(f"on_raw_{event.lower()}", data)
        _cache: Storage = self._http.cache[VoiceState]
        if event == "VOICE_STATE_UPDATE":
            model = VoiceState(**data, _client=self._http)
            old = _cache.get(model.user_id)
            self._dispatch.dispatch("on_voice_state_update", old, model)
            _cache.add(model, model.user_id)
        elif event == "VOICE_SERVER_UPDATE":
            model = VoiceServer(**data, _client=self._http)
            self._dispatch.dispatch("on_voice_server_update", model)

    async def connect_voice_channel(
        self, guild_id: int, channel_id: int, self_deaf: bool, self_mute: bool
    ):
        """
        Sends packet to websocket for connection to voice channel.

        :param guild_id: The guild id to connect.
        :type guild_id: int
        :param channel_id: The channel id to connect.
        :type channel_id: int
        :param self_deaf: Whether bot is self deafened
        :type self_deaf: bool
        :param self_mute: Whether bot is self muted
        :type self_mute: bool
        """
        payload = {
            "op": OpCodeType.VOICE_STATE,
            "d": {
                "channel_id": str(channel_id),
                "guild_id": str(guild_id),
                "self_deaf": self_deaf,
                "self_mute": self_mute,
            },
        }

        await self._send_packet(payload)

    async def disconnect_voice_channel(self, guild_id: int):
        """
        Sends packet to websocket for disconnecting from voice channel.

        :param guild_id: The guild id
        :type guild_id: int

        """
        payload = {
            "op": OpCodeType.VOICE_STATE,
            "d": {"channel_id": None, "guild_id": str(guild_id)},
        }

        await self._send_packet(payload)
