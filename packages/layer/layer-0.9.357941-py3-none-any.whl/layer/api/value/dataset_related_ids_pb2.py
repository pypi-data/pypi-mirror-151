# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/value/dataset_related_ids.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from layer.api import ids_pb2 as api_dot_ids__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#api/value/dataset_related_ids.proto\x12\x03\x61pi\x1a\rapi/ids.proto\"\x92\x01\n\x11\x44\x61tasetRelatedIds\x12\"\n\ndataset_id\x18\x01 \x01(\x0b\x32\x0e.api.DatasetId\x12-\n\x10\x64\x61taset_build_id\x18\x02 \x01(\x0b\x32\x13.api.DatasetBuildId\x12\x14\n\x0c\x64\x61taset_name\x18\x03 \x01(\t\x12\x14\n\x0cproject_name\x18\x04 \x01(\tB\x11\n\rcom.layer.apiP\x01\x62\x06proto3')



_DATASETRELATEDIDS = DESCRIPTOR.message_types_by_name['DatasetRelatedIds']
DatasetRelatedIds = _reflection.GeneratedProtocolMessageType('DatasetRelatedIds', (_message.Message,), {
  'DESCRIPTOR' : _DATASETRELATEDIDS,
  '__module__' : 'api.value.dataset_related_ids_pb2'
  # @@protoc_insertion_point(class_scope:api.DatasetRelatedIds)
  })
_sym_db.RegisterMessage(DatasetRelatedIds)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\rcom.layer.apiP\001'
  _DATASETRELATEDIDS._serialized_start=60
  _DATASETRELATEDIDS._serialized_end=206
# @@protoc_insertion_point(module_scope)
