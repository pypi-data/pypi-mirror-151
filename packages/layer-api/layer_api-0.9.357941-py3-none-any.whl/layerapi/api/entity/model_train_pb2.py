# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/entity/model_train.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from layerapi.api.entity import model_train_status_pb2 as api_dot_entity_dot_model__train__status__pb2
from layerapi.api import ids_pb2 as api_dot_ids__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1c\x61pi/entity/model_train.proto\x12\x03\x61pi\x1a#api/entity/model_train_status.proto\x1a\rapi/ids.proto\"\xa2\x04\n\nModelTrain\x12\x1d\n\x02id\x18\x01 \x01(\x0b\x32\x11.api.ModelTrainId\x12-\n\x10model_version_id\x18\x02 \x01(\x0b\x32\x13.api.ModelVersionId\x12\r\n\x05index\x18\x03 \x01(\x03\x12\x0b\n\x03uri\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\"\n\rcreated_by_id\x18\x06 \x01(\x0b\x32\x0b.api.UserId\x12\x17\n\x0fstart_timestamp\x18\x07 \x01(\x03\x12\x15\n\rend_timestamp\x18\x08 \x01(\x03\x12-\n\ntrain_type\x18\x0b \x01(\x0e\x32\x19.api.ModelTrain.TrainType\x12,\n\x0forganization_id\x18\r \x01(\x0b\x32\x13.api.OrganizationId\x12\"\n\nproject_id\x18\x0e \x01(\x0b\x32\x0e.api.ProjectId\x12=\n\x18hyperparameter_tuning_id\x18\x10 \x01(\x0b\x32\x1b.api.HyperparameterTuningId\x12+\n\x0ctrain_status\x18\x11 \x01(\x0b\x32\x15.api.ModelTrainStatus\"T\n\tTrainType\x12\x16\n\x12TRAIN_TYPE_INVALID\x10\x00\x12\x15\n\x11TRAIN_TYPE_AD_HOC\x10\x01\x12\x18\n\x14TRAIN_TYPE_SCHEDULED\x10\x02\x42\x11\n\rcom.layer.apiP\x01\x62\x06proto3')



_MODELTRAIN = DESCRIPTOR.message_types_by_name['ModelTrain']
_MODELTRAIN_TRAINTYPE = _MODELTRAIN.enum_types_by_name['TrainType']
ModelTrain = _reflection.GeneratedProtocolMessageType('ModelTrain', (_message.Message,), {
  'DESCRIPTOR' : _MODELTRAIN,
  '__module__' : 'api.entity.model_train_pb2'
  # @@protoc_insertion_point(class_scope:api.ModelTrain)
  })
_sym_db.RegisterMessage(ModelTrain)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\rcom.layer.apiP\001'
  _MODELTRAIN._serialized_start=90
  _MODELTRAIN._serialized_end=636
  _MODELTRAIN_TRAINTYPE._serialized_start=552
  _MODELTRAIN_TRAINTYPE._serialized_end=636
# @@protoc_insertion_point(module_scope)
