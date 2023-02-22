from lavalink.events import (
    TrackStartEvent,
    TrackStuckEvent,
    TrackExceptionEvent,
    TrackEndEvent,
    TrackLoadFailedEvent,
    QueueEndEvent,
    PlayerUpdateEvent,
    NodeConnectedEvent,
    NodeDisconnectedEvent,
    NodeChangedEvent,
    WebSocketClosedEvent,
)
from interactions.api.events.base import BaseEvent

__all__ = ("TrackStart", "TrackStuck", "TrackException", "TrackEnd", "TrackLoadFailed", "QueueEnd", "PlayerUpdate", "NodeConnected", "NodeDisconnected", "NodeChanged", "WebSocketClosed")


class TrackStart(BaseEvent, TrackStartEvent):
    ...


class TrackStuck(BaseEvent, TrackStuckEvent):
    ...


class TrackException(BaseEvent, TrackExceptionEvent):
    ...


class TrackEnd(BaseEvent, TrackEndEvent):
    ...


class TrackLoadFailed(BaseEvent, TrackLoadFailedEvent):
    ...


class QueueEnd(BaseEvent, QueueEndEvent):
    ...


class PlayerUpdate(BaseEvent, PlayerUpdateEvent):
    ...


class NodeConnected(BaseEvent, NodeConnectedEvent):
    ...


class NodeDisconnected(BaseEvent, NodeDisconnectedEvent):
    ...


class NodeChanged(BaseEvent, NodeChangedEvent):
    ...


class WebSocketClosed(BaseEvent, WebSocketClosedEvent):
    ...

