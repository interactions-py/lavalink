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
from interactions import Client


# Creating bot variable
client = Client(...)

# Loading your extension
client.load("exts.music")

# Starting bot
client.start()
```

Extension file: `exts/music.py`
```python
from interactions import Extension, extension_command, extension_listener, option, CommandContext, VoiceState
from interactions.ext.lavalink import Lavalink


class Music(Extension):
    def __init__(self, client):
        self.client = client
        self.lavalink: Lavalink = None

    @extension_listener()
    async def on_start(self):
        # Initialize lavalink instance
        self.lavalink: Lavalink = Lavalink(self.client)

        # Connect to lavalink server
        self.lavalink.add_node("127.0.0.1", 43421, "your_password", "eu")

    @extension_command()
    @option()
    async def play(self, ctx: CommandContext, query: str):
        await ctx.defer()

        # Getting user's voice state
        voice_state: VoiceState = ctx.author.voice_state
        if not voice_state or not voice_state.joined:
            return await ctx.send("You're not connected to the voice channel!")

        # Connecting to voice channel and getting player instance
        player = await self.lavalink.connect(voice_state.guild_id, voice_state.channel_id)

        # Getting tracks from youtube
        tracks = await player.search_youtube(query)
        # Selecting first founded track
        track = tracks[0]
        # Adding track to the queue
        player.add(requester=int(ctx.author.id), track=track)

        # Check if already playing
        if player.is_playing:
            return await ctx.send(f"Added to queue: `{track.title}`")

        # Starting playing track
        await player.play()
        await ctx.send(f"Now playing: `{track.title}`")

    @extension_command()
    async def leave(self, ctx: CommandContext):
        # Disconnect from voice channel and remove player
        await self.lavalink.disconnect(ctx.guild_id)

        await ctx.send("Disconnected", ephemeral=True)


def setup(client):
    Music(client)

```

## Events
To listen lavalink event you have to use either `@bot.event` or `@extension_listener` decorator.

```python
from interactions import Extension, extension_listener

import lavalink

# NOTE: Works only in extensions.
class MusicExt(Extension):
    ... # Some your cool music commands

    # There are most useful events for you. You can use other events if you want it.
    @extension_listener()
    async def on_track_start(self, event: lavalink.TrackStartEvent):
        """Fires when track starts"""

    @extension_listener()
    async def on_track_end(self, event: lavalink.TrackEndEvent):
        """Fires when track ends"""

    @extension_listener()
    async def on_queue_end(self, event: lavalink.QueueEndEvent):
        """Fires when queue ends"""

```

## Documentation

[lavalink.py documentation](https://lavalink.readthedocs.io/en/master/)
[lavalink.py repository](https://github.com/Devoxin/Lavalink.py)
