from interactions import Client, Intents


client = Client("TOKEN", intents=Intents.DEFAULT)

# Ext should be loaded first than your Extension!
client.load("interactions.ext.lavalink")
client.load("exts.music")

client.start()
