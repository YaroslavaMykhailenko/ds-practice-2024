from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FraudCheckRequest(_message.Message):
    __slots__ = ("order_json", "vector_clock_json")
    ORDER_JSON_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_JSON_FIELD_NUMBER: _ClassVar[int]
    order_json: str
    vector_clock_json: str
    def __init__(self, order_json: _Optional[str] = ..., vector_clock_json: _Optional[str] = ...) -> None: ...

class FraudCheckResponse(_message.Message):
    __slots__ = ("response_json", "vector_clock_json")
    RESPONSE_JSON_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_JSON_FIELD_NUMBER: _ClassVar[int]
    response_json: str
    vector_clock_json: str
    def __init__(self, response_json: _Optional[str] = ..., vector_clock_json: _Optional[str] = ...) -> None: ...
