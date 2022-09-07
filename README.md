# interactions-lavalink

## Installation

1. Download Java if you don't have it
2. Download lavalink from [this repo](https://github.com/freyacodes/Lavalink)
3. Configure `application.yml` file like [here](https://github.com/freyacodes/Lavalink/blob/master/LavalinkServer/application.yml.example)
4. Download ext via `pip install interactions-lavalink`

## Usage

Run lavalink via `java -jar Lavalink.jar` in same folder with `application.yml` file.
Create bot like example and run it.

Main file:
```python
import interactions
from interactions.ext.lavalink import VoiceState, VoiceClient

client = VoiceClient(...)

client.load("exts.music")

client.start()
```

Extension file: `exts/music.py`
```python
import interactions
from interactions.ext.lavalink import VoiceClient, VoiceState, listener
import lavalink


class Music(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @listener()
    async def on_track_start(self, event: lavalink.TrackStartEvent):
        """
        Fires when track starts
        """
        print("STARTED", event.track)

    @interactions.extension_listener()
    async def on_start(self):
        self.client.lavalink_client.add_node("127.0.0.1", 43421, "your_password", "eu")

    @interactions.extension_listener()
    async def on_voice_state_update(self, before: VoiceState, after: VoiceState):
        """
        Disconnect if bot is alone
        """
        if before and not after.joined:
            voice_states = self.client.get_channel_voice_states(before.channel_id)
            if len(voice_states) == 1 and voice_states[0].user_id == self.client.me.id:
                await self.client.disconnect(before.guild_id)

    @interactions.extension_command()
    @interactions.option()
    async def play(self, ctx: interactions.CommandContext, query: str):
        await ctx.defer()

        # NOTE: ctx.author.voice can be None if you runned a bot after joining the voice channel
        voice = ctx.author.voice
        if not voice or not voice.joined:
            return await ctx.send("You're not connected to the voice channel!")

        player = await self.client.connect(voice.guild_id, voice.channel_id)
        tracks = await player.search_youtube(query)

        track = tracks[0]
        player.add(requester=int(ctx.author.id), track=track)
        await player.play()

        await ctx.send(f"Now playing: `{track.title}`")

    @interactions.extension_command()
    async def leave(self, ctx: interactions.CommandContext):
        await self.client.disconnect(ctx.guild_id)
```
## New methods/properties for interactions.py library

`Member.voice` - returns current member's `VoiceState`. It can be `None` if not cached.  
`Channel.voice_states` - returns a list of voice states of the voice channel. Can be empty if not cached.  
`Guild.voice_states` - returns a list of guild voice states. Can be empty if not cached.

## Documentation

[lavalink.py documentation](https://lavalink.readthedocs.io/en/master/)  
[lavalink.py repository](https://github.com/Devoxin/Lavalink.py)

## Credits

Thanks EdVraz for `VoiceState` from [voice ext](https://github.com/interactions-py/voice)
