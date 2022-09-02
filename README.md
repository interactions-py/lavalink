# interactions-lavalink

## Installation

1. Download Java if you don't have it
2. Download lavalink from [this repo](https://github.com/freyacodes/Lavalink)
3. Configure `application.yml` file like [here](https://github.com/freyacodes/Lavalink/blob/master/LavalinkServer/application.yml.example)
4. Download ext via `pip install interactions-lavalink`

## Usage

Run lavalink via `java -jar Lavalink.jar` in same folder with `application.yml` file.
Create bot like example and run it.

```python
import interactions
from interactions.ext.lavalink import VoiceState, VoiceClient

client = VoiceClient(...)

@client.event()
async def on_start():
    client.lavalink_client.add_node("127.0.0.1", 43421, "your_password", "eu")  # Copy host, port and password from `application.yml`

@client.event()
async def on_voice_state_update(before: VoiceState, after: VoiceState):
    ...

@client.command()
@interactions.option()
async def play(ctx: interactions.CommandContext, query: str):
    await ctx.defer()
    # NOTE: ctx.author.voice can be None if you runned a bot after joining the voice channel
    player = await self.client.connect(ctx.author.voice.guild_id, ctx.author.voice.channel_id)

    results = await player.node.get_tracks(f"ytsearch:{query}")
    track = AudioTrack(results["tracks"][0], int(ctx.author.id))
    player.add(requester=int(ctx.author.id), track=track)
    await player.play()

    await ctx.send(f"Now playing: `{track.title}`")

client.start()
```

Example with using `Extension` [here](https://github.com/Damego/interactions-lavalink/tree/main/examples)

## Documentation

[lavalink.py documentation](https://lavalink.readthedocs.io/en/master/)
[lavalink.py repository](https://github.com/Devoxin/Lavalink.py)

## Credits

Thanks EdVraz for `VoiceState` from [voice ext](https://github.com/interactions-py/voice)
