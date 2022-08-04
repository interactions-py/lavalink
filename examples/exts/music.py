import interactions

from interactions.ext.lavalink import VoiceState, VoiceClient


class Music(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

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
        author_voice = self.client.get_user_voice_state(ctx.author.id)

        player = await self.client.connect(ctx.guild_id, author_voice.channel_id)

        results = await player.node.get_tracks(f"ytsearch:{query}")
        player.add(requester=int(ctx.author.id), track=results["tracks"][0])
        await player.play()

    @interactions.extension_command()
    async def leave(self, ctx: interactions.CommandContext):
        await self.client.disconnect(ctx.guild_id)

    @interactions.extension_command()
    @interactions.option(channel_types=[interactions.ChannelType.GUILD_VOICE])
    async def move_to(self, ctx: interactions.CommandContext, channel: interactions.Channel):
        await self.client.connect(ctx.guild_id, channel.id)


def setup(client):
    Music(client)
