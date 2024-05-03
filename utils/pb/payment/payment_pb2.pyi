from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PrepareRequest(_message.Message):
    __slots__ = ("order_id", "order_details_json", "message")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_DETAILS_JSON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    order_details_json: str
    message: str
    def __init__(self, order_id: _Optional[str] = ..., order_details_json: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class PrepareResponse(_message.Message):
    __slots__ = ("willCommit", "message")
    WILLCOMMIT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    willCommit: bool
    message: str
    def __init__(self, willCommit: bool = ..., message: _Optional[str] = ...) -> None: ...

class CommitRequest(_message.Message):
    __slots__ = ("order_id", "message")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    message: str
    def __init__(self, order_id: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class CommitResponse(_message.Message):
    __slots__ = ("success", "message", "order_details_json")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ORDER_DETAILS_JSON_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    order_details_json: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., order_details_json: _Optional[str] = ...) -> None: ...

class AbortRequest(_message.Message):
    __slots__ = ("order_id", "message")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    message: str
    def __init__(self, order_id: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class AbortResponse(_message.Message):
    __slots__ = ("success", "message", "order_details_json")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ORDER_DETAILS_JSON_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    order_details_json: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., order_details_json: _Optional[str] = ...) -> None: ...
