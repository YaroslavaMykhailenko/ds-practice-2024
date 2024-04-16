from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ProcessOrderRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ProcessOrderResponse(_message.Message):
    __slots__ = ("success", "order_json", "order_result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ORDER_JSON_FIELD_NUMBER: _ClassVar[int]
    ORDER_RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    order_json: str
    order_result: str
    def __init__(self, success: bool = ..., order_json: _Optional[str] = ..., order_result: _Optional[str] = ...) -> None: ...
