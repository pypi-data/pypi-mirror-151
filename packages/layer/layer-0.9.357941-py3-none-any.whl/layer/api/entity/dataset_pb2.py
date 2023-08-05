# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/entity/dataset.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from layer.api import ids_pb2 as api_dot_ids__pb2
from layer.api.value import python_dataset_pb2 as api_dot_value_dot_python__dataset__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18\x61pi/entity/dataset.proto\x12\x03\x61pi\x1a\rapi/ids.proto\x1a\x1e\x61pi/value/python_dataset.proto\"\xaf\x05\n\x07\x44\x61taset\x12\x1a\n\x02id\x18\x01 \x01(\x0b\x32\x0e.api.DatasetId\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0e\n\x06\x66ormat\x18\x04 \x01(\t\x12&\n\x06owners\x18\x05 \x01(\x0b\x32\x16.api.Dataset.OwnerList\x12\"\n\rcreated_by_id\x18\x06 \x01(\x0b\x32\x0b.api.UserId\x12\x19\n\x11\x63reated_timestamp\x18\x07 \x01(\x06\x12\x19\n\x11updated_timestamp\x18\x08 \x01(\x06\x12-\n\x10\x64\x65\x66\x61ult_build_id\x18\x0b \x01(\x0b\x32\x13.api.DatasetBuildId\x12,\n\x0forganization_id\x18\x0e \x01(\x0b\x32\x13.api.OrganizationId\x12&\n\x04type\x18\x0f \x01(\x0e\x32\x18.api.Dataset.DatasetType\x12,\n\x0epython_dataset\x18\x11 \x01(\x0b\x32\x12.api.PythonDatasetH\x00\x12\"\n\nproject_id\x18\x13 \x01(\x0b\x32\x0e.api.ProjectId\x12\x14\n\x0cproject_name\x18\x14 \x01(\t\x12\r\n\x05likes\x18\x15 \x01(\r\x12\x11\n\tdownloads\x18\x16 \x01(\r\x1aK\n\tOwnerList\x12\x1d\n\x08user_ids\x18\x01 \x03(\x0b\x32\x0b.api.UserId\x12\x1f\n\tgroup_ids\x18\x02 \x03(\x0b\x32\x0c.api.GroupId\"V\n\x0b\x44\x61tasetType\x12\x18\n\x14\x44\x41TASET_TYPE_INVALID\x10\x00\x12\x14\n\x10\x44\x41TASET_TYPE_RAW\x10\x01\x12\x17\n\x13\x44\x41TASET_TYPE_PYTHON\x10\x02\x42\x1f\n\x1d\x64\x65rived_dataset_build_detailsB\x11\n\rcom.layer.apiP\x01\x62\x06proto3')



_DATASET = DESCRIPTOR.message_types_by_name['Dataset']
_DATASET_OWNERLIST = _DATASET.nested_types_by_name['OwnerList']
_DATASET_DATASETTYPE = _DATASET.enum_types_by_name['DatasetType']
Dataset = _reflection.GeneratedProtocolMessageType('Dataset', (_message.Message,), {

  'OwnerList' : _reflection.GeneratedProtocolMessageType('OwnerList', (_message.Message,), {
    'DESCRIPTOR' : _DATASET_OWNERLIST,
    '__module__' : 'api.entity.dataset_pb2'
    # @@protoc_insertion_point(class_scope:api.Dataset.OwnerList)
    })
  ,
  'DESCRIPTOR' : _DATASET,
  '__module__' : 'api.entity.dataset_pb2'
  # @@protoc_insertion_point(class_scope:api.Dataset)
  })
_sym_db.RegisterMessage(Dataset)
_sym_db.RegisterMessage(Dataset.OwnerList)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\rcom.layer.apiP\001'
  _DATASET._serialized_start=81
  _DATASET._serialized_end=768
  _DATASET_OWNERLIST._serialized_start=572
  _DATASET_OWNERLIST._serialized_end=647
  _DATASET_DATASETTYPE._serialized_start=649
  _DATASET_DATASETTYPE._serialized_end=735
# @@protoc_insertion_point(module_scope)
