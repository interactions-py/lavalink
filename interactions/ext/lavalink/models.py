from datetime import datetime
from typing import Optional

from interactions.api.models.attrs_utils import ClientSerializerMixin, define, field

from interactions import Channel, Guild, Member, Snowflake

__all__ = ["VoiceState", "VoiceServer"]


# Origin code for `VoiceState` taken from
# https://github.com/interactions-py/voice/blob/main/interactions/ext/voice/state.py
@define()
class VoiceState(ClientSerializerMixin):
    """
    A class object representing the gateway event ``VOICE_STATE_UPDATE``.
    This class creates an object every time the event ``VOICE_STATE_UPDATE`` is received from the discord API.
    It contains information about the user's update voice information.
    Attributes:
    -----------
    _json : dict
        All data of the object stored as dictionary
    member : Member
        The member whose VoiceState was updated
    user_id : int
        The id of the user whose VoiceState was updated. This is technically the same as the "member id",
        but it is called `user_id` because of API terminology.
    suppress : bool
        Whether the user is muted by the current user(-> bot)
    session_id : int
        The id of the session
    self_video : bool
        Whether the user's camera is enabled.
    self_mute : bool
        Whether the user is muted by themselves
    self_deaf : bool
        Whether the user is deafened by themselves
    self_stream : bool
        Whether the user is streaming in the current channel
    request_to_speak_timestamp : datetime
        Only for stage-channels; when the user requested permissions to speak in the stage channel
    mute : bool
        Whether the user's microphone is muted by the server
    guild_id : int
        The id of the guild in what the update took action
    deaf : bool
        Whether the user is deafened by the guild
    channel_id : int
        The id of the channel the update took action
    """

    guild_id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    channel_id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    user_id: Snowflake = field(converter=Snowflake)
    member: Optional[Member] = field(converter=Member, default=None)
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

    async def mute_member(self, reason: Optional[str]) -> Member:
        """
        Mutes the current member.
        :param reason: The reason of the muting, optional
        :type reason: str
        :return: The modified member object
        :rtype: Member
        """
        return await self.member.modify(guild_id=int(self.guild_id), mute=True, reason=reason)

    async def deafen_member(self, reason: Optional[str]) -> Member:
        """
        Deafens the current member.
        :param reason: The reason of the deafening, optional
        :type reason: str
        :return: The modified member object
        :rtype: Member
        """
        return await self.member.modify(guild_id=int(self.guild_id), deaf=True, reason=reason)

    async def move_member(self, channel_id: int, *, reason: Optional[str]) -> Member:
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
        return Channel(**await self._client.get_channel(int(self.channel_id)), _client=self._client)

    async def get_guild(self) -> Guild:
        """
        Gets the guild in what the update took place.
        :rtype: Guild
        """
        return Guild(**await self._client.get_guild(int(self.channel_id)), _client=self._client)


@define()
class VoiceServer(ClientSerializerMixin):
    """
    A class object representing the gateway event ``VOICE_SERVER_UPDATE``.
    This class creates an object every time the event ``VOICE_SERVER_UPDATE`` is received from the discord API.
    """

    endpoint: str = field()
    guild_id: Snowflake = field(converter=Snowflake)
    token: str = field()

    async def get_guild(self) -> Guild:
        """
        Gets the guild in what the update took place.
        :rtype: Guild
        """
        return Guild(**await self._client.get_guild(int(self.channel_id)), _client=self._client)
