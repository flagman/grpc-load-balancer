# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x65xample_service.proto\x12\x07\x65xample\"\x1e\n\x0fGetValueRequest\x12\x0b\n\x03key\x18\x01 \x01(\x05\"!\n\x10GetValueResponse\x12\r\n\x05value\x18\x01 \x01(\t2S\n\x0e\x45xampleService\x12\x41\n\x08GetValue\x12\x18.example.GetValueRequest\x1a\x19.example.GetValueResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'example_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETVALUEREQUEST._serialized_start=34
  _GETVALUEREQUEST._serialized_end=64
  _GETVALUERESPONSE._serialized_start=66
  _GETVALUERESPONSE._serialized_end=99
  _EXAMPLESERVICE._serialized_start=101
  _EXAMPLESERVICE._serialized_end=184
# @@protoc_insertion_point(module_scope)