from interactions import Intents
from interactions.ext.lavalink import VoiceClient

client = VoiceClient("TOKEN", intents=Intents.DEFAULT)

client.load("exts.music")

client.start()
