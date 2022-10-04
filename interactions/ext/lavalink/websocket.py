from typing import TYPE_CHECKING

from interactions import OpCodeType, Storage, WebSocketClient, HTTPClient

from .models import VoiceServer, VoiceState

if TYPE_CHECKING:
    from interactions import Client

__all__ = ["VoiceWebSocketClient"]


class VoiceWebSocketClient(WebSocketClient):
    def __init__(self, bot_var: Client, *args):
        self._bot_var: Client = bot_var
        super().__init__(*args)

    async def run(self) -> None:
        """
        Handles the client's connection with the Gateway.
        """

        if isinstance(self._http, str):
            self._http = HTTPClient(self._http)
            self._http._bot_var = self._bot_var

        await super().run()

    def _dispatch_event(self, event: str, data: dict) -> None:
        if event not in ("VOICE_STATE_UPDATE", "VOICE_SERVER_UPDATE"):
            return super()._dispatch_event(event, data)

        self._dispatch.dispatch(f"on_raw_{event.lower()}", data)
        _cache: Storage = self._http.cache[VoiceState]

        if event == "VOICE_SERVER_UPDATE":
            model = VoiceServer(**data, _client=self._http)
            self._dispatch.dispatch("on_voice_server_update", model)
        elif event == "VOICE_STATE_UPDATE":
            model = VoiceState(**data, _client=self._http)
            old = _cache.get(model.user_id)
            self._dispatch.dispatch("on_voice_state_update", old, model)
            _cache.add(model, model.user_id)

    async def update_voice_state(
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

        await self._send_packet(payload)
