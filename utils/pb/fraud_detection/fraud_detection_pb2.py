# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: utils/pb/fraud_detection/fraud_detection.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.utils/pb/fraud_detection/fraud_detection.proto\x12\x0f\x66raud_detection\"\'\n\x11\x46raudCheckRequest\x12\x12\n\norder_json\x18\x01 \x01(\t\"+\n\x12\x46raudCheckResponse\x12\x15\n\ris_fraudulent\x18\x01 \x01(\x08\x32n\n\x15\x46raudDetectionService\x12U\n\nCheckFraud\x12\".fraud_detection.FraudCheckRequest\x1a#.fraud_detection.FraudCheckResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'utils.pb.fraud_detection.fraud_detection_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FRAUDCHECKREQUEST']._serialized_start=67
  _globals['_FRAUDCHECKREQUEST']._serialized_end=106
  _globals['_FRAUDCHECKRESPONSE']._serialized_start=108
  _globals['_FRAUDCHECKRESPONSE']._serialized_end=151
  _globals['_FRAUDDETECTIONSERVICE']._serialized_start=153
  _globals['_FRAUDDETECTIONSERVICE']._serialized_end=263
# @@protoc_insertion_point(module_scope)
