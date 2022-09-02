from typing import List, Optional

from interactions import Channel, Guild, Member

from .models import VoiceState


@property
def member_voice(self) -> Optional[VoiceState]:
    """
    Returns member's voice state object.
    """
    return self._client.cache[VoiceState].get(self.id)


Member.voice = member_voice


@property
def channel_voice_states(self) -> Optional[List[VoiceState]]:
    """
    Returns list of voice states of the voice channel.
    """
    return [
        voice_state
        for voice_state in self._client.cache[VoiceState].values.values()
        if voice_state.channel_id == self.id
    ]


Channel.voice_states = channel_voice_states


@property
def guild_voice_states(self) -> Optional[List[VoiceState]]:
    """
    Returns list of voice states of the guild.
    """
    return [
        voice_state
        for voice_state in self._client.cache[VoiceState].values.values()
        if voice_state.guild_id == self.id
    ]


Guild.voice_states = guild_voice_states
