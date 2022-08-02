from interactions.ext.base import Base
from interactions.ext.version import Version, VersionAuthor

__all__ = ["version", "base"]


version = Version(version="0.0.1", author=VersionAuthor(name="Damego"))

base = Base(
    name="interactions-lavalink",
    version=version,
    link="https://github.com/Damego/interactions-lavalink",
    description="Lavalink for interactions.py",
    packages=["interactions.ext.lavalink"],
    requirements=["discord-py-interactions>=4.3.0", "lavalink"],
)
