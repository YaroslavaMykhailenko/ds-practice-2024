from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Order(_message.Message):
    __slots__ = ("id", "order_json", "priority")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_JSON_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    order_json: str
    priority: int
    def __init__(self, id: _Optional[str] = ..., order_json: _Optional[str] = ..., priority: _Optional[int] = ...) -> None: ...

class EnqueueResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class DequeueRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
