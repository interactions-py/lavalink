from interactions import Member
from .models import VoiceState


@property
def voice(self):
    """
    Returns member's voice state object.
    """
    return self._client.cache[VoiceState].get(self.id)


Member.voice = voice
