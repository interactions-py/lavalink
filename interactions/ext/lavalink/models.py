from datetime import datetime
from typing import TYPE_CHECKING, Optional

from interactions.utils.attrs_utils import ClientSerializerMixin, define, field

from interactions import Channel, Guild, LibraryException, Member, Snowflake

if TYPE_CHECKING:
    from .player import Player

__all__ = ["VoiceState", "VoiceServer"]


# Origin code for `VoiceState` taken from
# https://github.com/interactions-py/voice/blob/main/interactions/ext/voice/state.py
@define()
class VoiceState(ClientSerializerMixin):
    """
    A class object representing the gateway event ``VOICE_STATE_UPDATE``.
    This class creates an object every time the event ``VOICE_STATE_UPDATE`` is received from the discord API.
    It contains information about the user's update voice information.

    :ivar Member member: The member whose VoiceState was updated
    :ivar int user_id: The id of the user whose VoiceState was updated.
    :ivar bool suppress: Whether the user is muted by the current user(-> bot)
    :ivar int session_id: The id of the session
    :ivar bool self_video: Whether the user's camera is enabled.
    :ivar bool self_mute: Whether the user is muted by themselves
    :ivar bool self_deaf: Whether the user is deafened by themselves
    :ivar bool self_stream: Whether the user is streaming in the current channel
    :ivar datetime request_to_speak_timestamp: Only for stage-channels; when the user requested permissions to speak in the stage channel
    :ivar bool mute: Whether the user's microphone is muted by the server
    :ivar int guild_id: The id of the guild in what the update took action
    :ivar bool deaf: Whether the user is deafened by the guild
    :ivar int channel_id: The id of the channel the update took action
    """

    guild_id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    channel_id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    user_id: Snowflake = field(converter=Snowflake)
    member: Optional[Member] = field(converter=Member, default=None, add_client=True)
    session_id: str = field()
    deaf: bool = field()
    mute: bool = field()
    self_deaf: bool = field()
    self_mute: bool = field()
    self_stream: Optional[bool] = field(default=None)
    self_video: bool = field()
    suppress: bool = field()
    request_to_speak_timestamp: Optional[datetime] = field(
        converter=datetime.fromisoformat, default=None
    )

    @property
    def joined(self) -> bool:
        """
        Whether the user joined the channel.

        :rtype: bool
        """
        return self.channel_id is not None

    async def mute_member(self, reason: Optional[str] = None) -> Member:
        """
        Mutes the current member.

        :param reason: The reason of the muting, optional
        :type reason: str
        :return: The modified member object
        :rtype: Member
        """
        return await self.member.modify(guild_id=int(self.guild_id), mute=True, reason=reason)

    async def deafen_member(self, reason: Optional[str] = None) -> Member:
        """
        Deafens the current member.

        :param reason: The reason of the deafening, optional
        :type reason: str
        :return: The modified member object
        :rtype: Member
        """
        return await self.member.modify(guild_id=int(self.guild_id), deaf=True, reason=reason)

    async def move_member(self, channel_id: int, *, reason: Optional[str] = None) -> Member:
        """
        Moves the member to another channel.

        :param channel_id: The ID of the channel to move the user to
        :type channel_id: int
        :param reason: The reason of the move
        :type reason: str
        :return: The modified member object
        :rtype: Member
        """
        return await self.member.modify(
            guild_id=int(self.guild_id), channel_id=channel_id, reason=reason
        )

    async def get_channel(self) -> Channel:
        """
        Gets the channel in what the update took place.

        :rtype: Channel
        """
        channel = self._client.cache[Channel].get(self.channel_id)
        if channel is not None:
            return channel
        return Channel(**await self._client.get_channel(int(self.channel_id)), _client=self._client)

    async def get_guild(self) -> Guild:
        """
        Gets the guild in what the update took place.

        :rtype: Guild
        """
        guild = self._client.cache[Guild].get(self.guild_id)
        if guild is not None:
            return guild
        return Guild(**await self._client.get_guild(int(self.guild_id)), _client=self._client)

    async def connect(self, self_deaf: bool = False, self_mute: bool = False) -> "Player":
        if not self.channel_id:
            raise LibraryException(message="User not connected to the voice channel!")

        await self._client._bot_var._websocket.update_voice_state(
            self.guild_id, self.channel_id, self_deaf, self_mute
        )
        player = self._client._bot_var.lavalink_client.player_manager.get(int(self.guild_id))
        if player is None:
            player = self._client._bot_var.lavalink_client.player_manager.create(int(self.guild_id))
        return player


@define()
class VoiceServer(ClientSerializerMixin):
    """
    A class object representing the gateway event ``VOICE_SERVER_UPDATE``.

    :ivar str endpoint: Voice connection token
    :ivar Snowflake guild_id: Guild this voice server update is for
    :ivar str token: Voice server host
    """

    endpoint: str = field()
    guild_id: Snowflake = field(converter=Snowflake)
    token: str = field()

    async def get_guild(self) -> Guild:
        """
        Gets the guild in what the update took place.
        :rtype: Guild
        """
        guild = self._client.cache[Guild].get(self.guild_id)
        if guild is not None:
            return guild
        return Guild(**await self._client.get_guild(int(self.guild_id)), _client=self._client)
