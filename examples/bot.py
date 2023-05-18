from interactions import Client

client = Client()

client.load_extension("exts.music")
client.start("TOKEN")
