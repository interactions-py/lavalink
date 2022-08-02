import interactions

from interactions.ext.lavalink import LavalinkVoice


class Music(interactions.Extension):
    def __init__(self, client):
        self.client = client
        self.voice: LavalinkVoice = self.client.voice

    @interactions.extension_listener()
    async def on_start(self):
        self.voice.lavalink_client.add_node("127.0.0.1", 43421, "your_password", "eu")

    @interactions.extension_command()
    @interactions.option()
    async def play(self, ctx: interactions.CommandContext, query: str):
        author_voice = self.voice.get_user_voice_state(ctx.author.id)

        player = await self.voice.connect(ctx.guild_id, author_voice.channel_id)

        results = await player.node.get_tracks(f"ytsearch:{query}")
        player.add(requester=int(ctx.author.id), track=results["tracks"][0])
        await player.play()

    @interactions.extension_command()
    async def leave(self, ctx: interactions.CommandContext):
        await self.voice.disconnect(ctx.guild_id)


def setup(client):
    Music(client)
