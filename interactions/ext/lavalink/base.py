from interactions.ext.base import Base
from interactions.ext.version import Version, VersionAuthor

__all__ = ["version", "base"]
__version__ = "0.1.2"

version = Version(
    version=__version__, author=VersionAuthor(name="Damego", email="damego.dev@gmail.com")
)
base = Base(
    name="interactions-lavalink",
    version=version,
    link="https://github.com/interactions-py/interactions-lavalink",
    description="Lavalink and voice support for interactions.py",
    packages=["interactions.ext.lavalink"],
    requirements=["discord-py-interactions>=4.3.0", "lavalink"],
)
