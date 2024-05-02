# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: utils/pb/book_storage/book_storage.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(utils/pb/book_storage/book_storage.proto\x12\x0c\x62ook_storage\"\x9d\x01\n\x04\x42ook\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x0e\n\x06\x63opies\x18\x05 \x01(\x05\x12\x17\n\x0f\x63opiesAvailable\x18\x06 \x01(\x05\x12\x10\n\x08\x63\x61tegory\x18\x07 \x01(\t\x12\x0b\n\x03img\x18\x08 \x01(\t\x12\r\n\x05price\x18\t \x01(\x02\">\n\x0cWriteRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12!\n\x05value\x18\x02 \x01(\x0b\x32\x12.book_storage.Book\" \n\rWriteResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x1a\n\x0bReadRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"O\n\x0cReadResponse\x12!\n\x05value\x18\x01 \x01(\x0b\x32\x12.book_storage.Book\x12\r\n\x05\x63lean\x18\x02 \x01(\x08\x12\r\n\x05\x66ound\x18\x03 \x01(\x08\"3\n\x13\x43leanVersionRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05\"\'\n\x14\x43leanVersionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\" \n\x11\x43heckStockRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"O\n\x12\x43heckStockResponse\x12\x17\n\x0f\x63opiesAvailable\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x0f\n\x07message\x18\x03 \x01(\t\"0\n\x12StockUpdateRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05\"&\n\x13StockUpdateResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"O\n\x0ePrepareRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x1a\n\x12order_details_json\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"6\n\x0fPrepareResponse\x12\x12\n\nwillCommit\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"2\n\rCommitRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"N\n\x0e\x43ommitResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x1a\n\x12order_details_json\x18\x03 \x01(\t\"1\n\x0c\x41\x62ortRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"M\n\rAbortResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x1a\n\x12order_details_json\x18\x03 \x01(\t2\xb3\x05\n\x0b\x42ookStorage\x12@\n\x05Write\x12\x1a.book_storage.WriteRequest\x1a\x1b.book_storage.WriteResponse\x12=\n\x04Read\x12\x19.book_storage.ReadRequest\x1a\x1a.book_storage.ReadResponse\x12U\n\x0c\x43leanVersion\x12!.book_storage.CleanVersionRequest\x1a\".book_storage.CleanVersionResponse\x12O\n\nCheckStock\x12\x1f.book_storage.CheckStockRequest\x1a .book_storage.CheckStockResponse\x12U\n\x0e\x44\x65\x63rementStock\x12 .book_storage.StockUpdateRequest\x1a!.book_storage.StockUpdateResponse\x12U\n\x0eIncrementStock\x12 .book_storage.StockUpdateRequest\x1a!.book_storage.StockUpdateResponse\x12\x46\n\x07Prepare\x12\x1c.book_storage.PrepareRequest\x1a\x1d.book_storage.PrepareResponse\x12\x43\n\x06\x43ommit\x12\x1b.book_storage.CommitRequest\x1a\x1c.book_storage.CommitResponse\x12@\n\x05\x41\x62ort\x12\x1a.book_storage.AbortRequest\x1a\x1b.book_storage.AbortResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'utils.pb.book_storage.book_storage_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BOOK']._serialized_start=59
  _globals['_BOOK']._serialized_end=216
  _globals['_WRITEREQUEST']._serialized_start=218
  _globals['_WRITEREQUEST']._serialized_end=280
  _globals['_WRITERESPONSE']._serialized_start=282
  _globals['_WRITERESPONSE']._serialized_end=314
  _globals['_READREQUEST']._serialized_start=316
  _globals['_READREQUEST']._serialized_end=342
  _globals['_READRESPONSE']._serialized_start=344
  _globals['_READRESPONSE']._serialized_end=423
  _globals['_CLEANVERSIONREQUEST']._serialized_start=425
  _globals['_CLEANVERSIONREQUEST']._serialized_end=476
  _globals['_CLEANVERSIONRESPONSE']._serialized_start=478
  _globals['_CLEANVERSIONRESPONSE']._serialized_end=517
  _globals['_CHECKSTOCKREQUEST']._serialized_start=519
  _globals['_CHECKSTOCKREQUEST']._serialized_end=551
  _globals['_CHECKSTOCKRESPONSE']._serialized_start=553
  _globals['_CHECKSTOCKRESPONSE']._serialized_end=632
  _globals['_STOCKUPDATEREQUEST']._serialized_start=634
  _globals['_STOCKUPDATEREQUEST']._serialized_end=682
  _globals['_STOCKUPDATERESPONSE']._serialized_start=684
  _globals['_STOCKUPDATERESPONSE']._serialized_end=722
  _globals['_PREPAREREQUEST']._serialized_start=724
  _globals['_PREPAREREQUEST']._serialized_end=803
  _globals['_PREPARERESPONSE']._serialized_start=805
  _globals['_PREPARERESPONSE']._serialized_end=859
  _globals['_COMMITREQUEST']._serialized_start=861
  _globals['_COMMITREQUEST']._serialized_end=911
  _globals['_COMMITRESPONSE']._serialized_start=913
  _globals['_COMMITRESPONSE']._serialized_end=991
  _globals['_ABORTREQUEST']._serialized_start=993
  _globals['_ABORTREQUEST']._serialized_end=1042
  _globals['_ABORTRESPONSE']._serialized_start=1044
  _globals['_ABORTRESPONSE']._serialized_end=1121
  _globals['_BOOKSTORAGE']._serialized_start=1124
  _globals['_BOOKSTORAGE']._serialized_end=1815
# @@protoc_insertion_point(module_scope)
