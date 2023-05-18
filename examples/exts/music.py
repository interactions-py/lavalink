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