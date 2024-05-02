from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Book(_message.Message):
    __slots__ = ("id", "title", "author", "description", "copies", "copiesAvailable", "category", "img", "price")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COPIES_FIELD_NUMBER: _ClassVar[int]
    COPIESAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    IMG_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    author: str
    description: str
    copies: int
    copiesAvailable: int
    category: str
    img: str
    price: float
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., author: _Optional[str] = ..., description: _Optional[str] = ..., copies: _Optional[int] = ..., copiesAvailable: _Optional[int] = ..., category: _Optional[str] = ..., img: _Optional[str] = ..., price: _Optional[float] = ...) -> None: ...

class WriteRequest(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: Book
    def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Book, _Mapping]] = ...) -> None: ...

class WriteResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class ReadRequest(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ("value", "clean", "found")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    CLEAN_FIELD_NUMBER: _ClassVar[int]
    FOUND_FIELD_NUMBER: _ClassVar[int]
    value: Book
    clean: bool
    found: bool
    def __init__(self, value: _Optional[_Union[Book, _Mapping]] = ..., clean: bool = ..., found: bool = ...) -> None: ...

class CleanVersionRequest(_message.Message):
    __slots__ = ("key", "version")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    key: str
    version: int
    def __init__(self, key: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class CleanVersionResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CheckStockRequest(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class CheckStockResponse(_message.Message):
    __slots__ = ("copiesAvailable", "success", "message")
    COPIESAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    copiesAvailable: int
    success: bool
    message: str
    def __init__(self, copiesAvailable: _Optional[int] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...

class StockUpdateRequest(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: int
    def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...

class StockUpdateResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

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
