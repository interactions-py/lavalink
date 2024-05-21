import attrs
from interactions.api.events.base import BaseEvent
from lavalink.events import (
    Event,
    IncomingWebSocketMessage,
    NodeChangedEvent,
    NodeConnectedEvent,
    NodeReadyEvent,
    NodeDisconnectedEvent,
    PlayerUpdateEvent,
    QueueEndEvent,
    TrackEndEvent,
    TrackExceptionEvent,
    TrackLoadFailedEvent,
    TrackStartEvent,
    TrackStuckEvent,
    WebSocketClosedEvent,
)

__all__ = (
    "TrackStart",
    "TrackStuck",
    "TrackException",
    "TrackEnd",
    "TrackLoadFailed",
    "QueueEnd",
    "PlayerUpdate",
    "NodeConnected",
    "NodeDisconnected",
    "NodeChanged",
    "WebSocketClosed",
)


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class CursedLavalinkEvent(BaseEvent):
    lavalink_event: Event = attrs.field(repr=False)

    def __getattr__(self, name: str):
        return getattr(self.lavalink_event, name)

@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class IncomingWebSocketMessage(CursedLavalinkEvent, IncomingWebSocketMessage):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class TrackStart(CursedLavalinkEvent, TrackStartEvent):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class TrackStuck(CursedLavalinkEvent, TrackStuckEvent):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class TrackException(CursedLavalinkEvent, TrackExceptionEvent):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class TrackEnd(CursedLavalinkEvent, TrackEndEvent):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class TrackLoadFailed(CursedLavalinkEvent, TrackLoadFailedEvent):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class QueueEnd(CursedLavalinkEvent, QueueEndEvent):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class PlayerUpdate(CursedLavalinkEvent, PlayerUpdateEvent):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class NodeConnected(CursedLavalinkEvent, NodeConnectedEvent):
    ...

@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class NodeReady(CursedLavalinkEvent, NodeReadyEvent):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class NodeDisconnected(CursedLavalinkEvent, NodeDisconnectedEvent):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class NodeChanged(CursedLavalinkEvent, NodeChangedEvent):
    ...


@attrs.define(eq=False, order=False, hash=False, slots=False, kw_only=False)
class WebSocketClosed(CursedLavalinkEvent, WebSocketClosedEvent):
    ...
