# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: utils/pb/suggestions/suggestions.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&utils/pb/suggestions/suggestions.proto\x12\x0bsuggestions\"(\n\x12SuggestionsRequest\x12\x12\n\norder_json\x18\x01 \x01(\t\"=\n\x13SuggestionsResponse\x12&\n\x0bsuggestions\x18\x01 \x03(\x0b\x32\x11.suggestions.Book\"\x9d\x01\n\x04\x42ook\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x0e\n\x06\x63opies\x18\x05 \x01(\x05\x12\x17\n\x0f\x63opiesAvailable\x18\x06 \x01(\x05\x12\x10\n\x08\x63\x61tegory\x18\x07 \x01(\t\x12\x0b\n\x03img\x18\x08 \x01(\t\x12\r\n\x05price\x18\t \x01(\x05\x32i\n\x12SuggestionsService\x12S\n\x0eGetSuggestions\x12\x1f.suggestions.SuggestionsRequest\x1a .suggestions.SuggestionsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'utils.pb.suggestions.suggestions_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SUGGESTIONSREQUEST']._serialized_start=55
  _globals['_SUGGESTIONSREQUEST']._serialized_end=95
  _globals['_SUGGESTIONSRESPONSE']._serialized_start=97
  _globals['_SUGGESTIONSRESPONSE']._serialized_end=158
  _globals['_BOOK']._serialized_start=161
  _globals['_BOOK']._serialized_end=318
  _globals['_SUGGESTIONSSERVICE']._serialized_start=320
  _globals['_SUGGESTIONSSERVICE']._serialized_end=425
# @@protoc_insertion_point(module_scope)
