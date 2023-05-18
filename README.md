# interactions-lavalink

## Installation

Download ext via `pip install --upgrade interactions-lavalink`

## Configuring own lavalink server

1. Download Java SE if you don't have it
2. Download lavalink from [this repo](https://github.com/freyacodes/Lavalink)
3. Configure `application.yml` file like [here](https://github.com/freyacodes/Lavalink/blob/master/LavalinkServer/application.yml.example)
4. Run lavalink server via `java -jar Lavalink.jar` in same folder with `application.yml` file.

## Usage

Create bot like example and run it.

Main file:
```python
from interactions import Client


# Creating bot variable
client = Client()

# Loading your extension
client.load("exts.music")

# Starting bot
client.start("TOKEN")
```

Extension file: `exts/music.py`
```python
from interactions import Extension, SlashContext, listen, slash_command, slash_option

from interactions_lavalink import Lavalink
from interactions_lavalink.events import TrackStart


class Music(Extension):
    def __init__(self, client):
        self.client = client
        self.lavalink: Lavalink | None = None

    @listen()
    async def on_startup(self):
        # Initializing lavalink instance on bot startup
        self.lavalink: Lavalink = Lavalink(self.client)

        # Connecting to local lavalink server
        self.lavalink.add_node("127.0.0.1", 43421, "your_password", "eu")

    @listen()
    async def on_track_start(self, event: TrackStart):
        print("Track started", event.track.title)

    @slash_command()
    @slash_option("query", "The search query or url", opt_type=3, required=True)
    async def play(self, ctx: SlashContext, query: str):
        await ctx.defer()

        # Getting user's voice state
        voice_state = ctx.author.voice
        if not voice_state or not voice_state.channel:
            return await ctx.send("You're not connected to the voice channel!")

        # Connecting to voice channel and getting player instance
        player = await self.lavalink.connect(voice_state.guild.id, voice_state.channel.id)
        # Getting tracks from youtube
        tracks = await player.search_youtube(query)
        track = tracks[0]
        # Adding track to the queue
        player.add(requester=int(ctx.author.id), track=track)

        # Check if player is already playing
        if player.is_playing:
            return await ctx.send(f"Added to queue: `{track.title}`")

        # Starting playing track
        await player.play()
        await ctx.send(f"Now playing: `{track.title}`")

    @slash_command()
    async def leave(self, ctx: SlashContext):
        # Disconnecting from voice channel
        await self.lavalink.disconnect(ctx.guild.id)

        await ctx.send("Disconnected", ephemeral=True)
```

## Events
To listen lavalink event you have to use `@listen` decorator.

```python
from interactions import Extension, listen
from interactions_lavalink import TrackStart, TrackEnd, QueueEnd

class MusicExt(Extension):
    ... # Some your cool music commands

    # There are many useful events for you. You can use other events if you want it.
    @listen()
    async def on_track_start(self, event: TrackStart):
        """Fires when track starts"""
        print(f"Track {event.track.title} started")

    @listen()
    async def on_track_end(self, event: TrackEnd):
        """Fires when track ends"""

    @listen()
    async def on_queue_end(self, event: QueueEnd):
        """Fires when queue ends"""

```

More events you could find in the `lavalink.py` documentation

## Documentation

[lavalink.py documentation](https://lavalink.readthedocs.io/en/master/) \
[lavalink.py repository](https://github.com/Devoxin/Lavalink.py)
