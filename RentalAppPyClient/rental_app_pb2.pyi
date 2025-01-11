from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class birthdayMsg(_message.Message):
    __slots__ = ("birthday",)
    BIRTHDAY_FIELD_NUMBER: _ClassVar[int]
    birthday: int
    def __init__(self, birthday: _Optional[int] = ...) -> None: ...

class dinMsg(_message.Message):
    __slots__ = ("age", "height", "h_unit", "weight", "w_unit", "skier_type")
    AGE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    H_UNIT_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    W_UNIT_FIELD_NUMBER: _ClassVar[int]
    SKIER_TYPE_FIELD_NUMBER: _ClassVar[int]
    age: int
    height: int
    h_unit: int
    weight: int
    w_unit: int
    skier_type: int
    def __init__(self, age: _Optional[int] = ..., height: _Optional[int] = ..., h_unit: _Optional[int] = ..., weight: _Optional[int] = ..., w_unit: _Optional[int] = ..., skier_type: _Optional[int] = ...) -> None: ...

class totalMsg(_message.Message):
    __slots__ = ("eq_type", "lease_type", "pkg_type")
    EQ_TYPE_FIELD_NUMBER: _ClassVar[int]
    LEASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PKG_TYPE_FIELD_NUMBER: _ClassVar[int]
    eq_type: int
    lease_type: int
    pkg_type: int
    def __init__(self, eq_type: _Optional[int] = ..., lease_type: _Optional[int] = ..., pkg_type: _Optional[int] = ...) -> None: ...

class ageReply(_message.Message):
    __slots__ = ("age",)
    AGE_FIELD_NUMBER: _ClassVar[int]
    age: int
    def __init__(self, age: _Optional[int] = ...) -> None: ...

class dinReply(_message.Message):
    __slots__ = ("din",)
    DIN_FIELD_NUMBER: _ClassVar[int]
    din: float
    def __init__(self, din: _Optional[float] = ...) -> None: ...

class totalReply(_message.Message):
    __slots__ = ("total",)
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    total: float
    def __init__(self, total: _Optional[float] = ...) -> None: ...
