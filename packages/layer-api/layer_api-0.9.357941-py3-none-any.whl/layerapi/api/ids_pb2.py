# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/ids.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from layerapi.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rapi/ids.proto\x12\x03\x61pi\x1a\x17validate/validate.proto\"$\n\tAccountId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"*\n\x0f\x43omputeFabricId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"$\n\tDatasetId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"+\n\x10\x44\x61tasetVersionId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\")\n\x0e\x44\x61tasetBuildId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"\"\n\x07GroupId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"\'\n\x0cLoggedDataId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"\"\n\x07ModelId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"\'\n\x0cModelTrainId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"(\n\rModelMetricId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\")\n\x0eModelVersionId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"1\n\x16HyperparameterTuningId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\")\n\x0eOrganizationId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"!\n\x06UserId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\" \n\x05RunId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"$\n\tProjectId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"!\n\x10StripeCustomerId\x12\r\n\x05value\x18\x01 \x01(\t\"$\n\x13StripeSetupIntentId\x12\r\n\x05value\x18\x01 \x01(\t\"&\n\x15StripePaymentMethodId\x12\r\n\x05value\x18\x01 \x01(\t\"%\n\x14\x43reditsAttributionId\x12\r\n\x05value\x18\x01 \x01(\t\"$\n\x13\x41uth0OrganizationId\x12\r\n\x05value\x18\x01 \x01(\t\"%\n\x14OrganizationInviteId\x12\r\n\x05value\x18\x01 \x01(\t\"\x17\n\x06RoleId\x12\r\n\x05value\x18\x01 \x01(\t\"\'\n\rAuth0ClientId\x12\x16\n\x05value\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\"&\n\x0c\x43onnectionId\x12\x16\n\x05value\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\"\x1c\n\x0b\x41uth0UserId\x12\r\n\x05value\x18\x01 \x01(\t\"\x1b\n\nPipelineId\x12\r\n\x05value\x18\x01 \x01(\t\"!\n\x06TierId\x12\x17\n\x05value\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\x42\x11\n\rcom.layer.apiP\x00\x62\x06proto3')



_ACCOUNTID = DESCRIPTOR.message_types_by_name['AccountId']
_COMPUTEFABRICID = DESCRIPTOR.message_types_by_name['ComputeFabricId']
_DATASETID = DESCRIPTOR.message_types_by_name['DatasetId']
_DATASETVERSIONID = DESCRIPTOR.message_types_by_name['DatasetVersionId']
_DATASETBUILDID = DESCRIPTOR.message_types_by_name['DatasetBuildId']
_GROUPID = DESCRIPTOR.message_types_by_name['GroupId']
_LOGGEDDATAID = DESCRIPTOR.message_types_by_name['LoggedDataId']
_MODELID = DESCRIPTOR.message_types_by_name['ModelId']
_MODELTRAINID = DESCRIPTOR.message_types_by_name['ModelTrainId']
_MODELMETRICID = DESCRIPTOR.message_types_by_name['ModelMetricId']
_MODELVERSIONID = DESCRIPTOR.message_types_by_name['ModelVersionId']
_HYPERPARAMETERTUNINGID = DESCRIPTOR.message_types_by_name['HyperparameterTuningId']
_ORGANIZATIONID = DESCRIPTOR.message_types_by_name['OrganizationId']
_USERID = DESCRIPTOR.message_types_by_name['UserId']
_RUNID = DESCRIPTOR.message_types_by_name['RunId']
_PROJECTID = DESCRIPTOR.message_types_by_name['ProjectId']
_STRIPECUSTOMERID = DESCRIPTOR.message_types_by_name['StripeCustomerId']
_STRIPESETUPINTENTID = DESCRIPTOR.message_types_by_name['StripeSetupIntentId']
_STRIPEPAYMENTMETHODID = DESCRIPTOR.message_types_by_name['StripePaymentMethodId']
_CREDITSATTRIBUTIONID = DESCRIPTOR.message_types_by_name['CreditsAttributionId']
_AUTH0ORGANIZATIONID = DESCRIPTOR.message_types_by_name['Auth0OrganizationId']
_ORGANIZATIONINVITEID = DESCRIPTOR.message_types_by_name['OrganizationInviteId']
_ROLEID = DESCRIPTOR.message_types_by_name['RoleId']
_AUTH0CLIENTID = DESCRIPTOR.message_types_by_name['Auth0ClientId']
_CONNECTIONID = DESCRIPTOR.message_types_by_name['ConnectionId']
_AUTH0USERID = DESCRIPTOR.message_types_by_name['Auth0UserId']
_PIPELINEID = DESCRIPTOR.message_types_by_name['PipelineId']
_TIERID = DESCRIPTOR.message_types_by_name['TierId']
AccountId = _reflection.GeneratedProtocolMessageType('AccountId', (_message.Message,), {
  'DESCRIPTOR' : _ACCOUNTID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.AccountId)
  })
_sym_db.RegisterMessage(AccountId)

ComputeFabricId = _reflection.GeneratedProtocolMessageType('ComputeFabricId', (_message.Message,), {
  'DESCRIPTOR' : _COMPUTEFABRICID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.ComputeFabricId)
  })
_sym_db.RegisterMessage(ComputeFabricId)

DatasetId = _reflection.GeneratedProtocolMessageType('DatasetId', (_message.Message,), {
  'DESCRIPTOR' : _DATASETID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.DatasetId)
  })
_sym_db.RegisterMessage(DatasetId)

DatasetVersionId = _reflection.GeneratedProtocolMessageType('DatasetVersionId', (_message.Message,), {
  'DESCRIPTOR' : _DATASETVERSIONID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.DatasetVersionId)
  })
_sym_db.RegisterMessage(DatasetVersionId)

DatasetBuildId = _reflection.GeneratedProtocolMessageType('DatasetBuildId', (_message.Message,), {
  'DESCRIPTOR' : _DATASETBUILDID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.DatasetBuildId)
  })
_sym_db.RegisterMessage(DatasetBuildId)

GroupId = _reflection.GeneratedProtocolMessageType('GroupId', (_message.Message,), {
  'DESCRIPTOR' : _GROUPID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.GroupId)
  })
_sym_db.RegisterMessage(GroupId)

LoggedDataId = _reflection.GeneratedProtocolMessageType('LoggedDataId', (_message.Message,), {
  'DESCRIPTOR' : _LOGGEDDATAID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.LoggedDataId)
  })
_sym_db.RegisterMessage(LoggedDataId)

ModelId = _reflection.GeneratedProtocolMessageType('ModelId', (_message.Message,), {
  'DESCRIPTOR' : _MODELID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.ModelId)
  })
_sym_db.RegisterMessage(ModelId)

ModelTrainId = _reflection.GeneratedProtocolMessageType('ModelTrainId', (_message.Message,), {
  'DESCRIPTOR' : _MODELTRAINID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.ModelTrainId)
  })
_sym_db.RegisterMessage(ModelTrainId)

ModelMetricId = _reflection.GeneratedProtocolMessageType('ModelMetricId', (_message.Message,), {
  'DESCRIPTOR' : _MODELMETRICID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.ModelMetricId)
  })
_sym_db.RegisterMessage(ModelMetricId)

ModelVersionId = _reflection.GeneratedProtocolMessageType('ModelVersionId', (_message.Message,), {
  'DESCRIPTOR' : _MODELVERSIONID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.ModelVersionId)
  })
_sym_db.RegisterMessage(ModelVersionId)

HyperparameterTuningId = _reflection.GeneratedProtocolMessageType('HyperparameterTuningId', (_message.Message,), {
  'DESCRIPTOR' : _HYPERPARAMETERTUNINGID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.HyperparameterTuningId)
  })
_sym_db.RegisterMessage(HyperparameterTuningId)

OrganizationId = _reflection.GeneratedProtocolMessageType('OrganizationId', (_message.Message,), {
  'DESCRIPTOR' : _ORGANIZATIONID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.OrganizationId)
  })
_sym_db.RegisterMessage(OrganizationId)

UserId = _reflection.GeneratedProtocolMessageType('UserId', (_message.Message,), {
  'DESCRIPTOR' : _USERID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.UserId)
  })
_sym_db.RegisterMessage(UserId)

RunId = _reflection.GeneratedProtocolMessageType('RunId', (_message.Message,), {
  'DESCRIPTOR' : _RUNID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.RunId)
  })
_sym_db.RegisterMessage(RunId)

ProjectId = _reflection.GeneratedProtocolMessageType('ProjectId', (_message.Message,), {
  'DESCRIPTOR' : _PROJECTID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.ProjectId)
  })
_sym_db.RegisterMessage(ProjectId)

StripeCustomerId = _reflection.GeneratedProtocolMessageType('StripeCustomerId', (_message.Message,), {
  'DESCRIPTOR' : _STRIPECUSTOMERID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.StripeCustomerId)
  })
_sym_db.RegisterMessage(StripeCustomerId)

StripeSetupIntentId = _reflection.GeneratedProtocolMessageType('StripeSetupIntentId', (_message.Message,), {
  'DESCRIPTOR' : _STRIPESETUPINTENTID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.StripeSetupIntentId)
  })
_sym_db.RegisterMessage(StripeSetupIntentId)

StripePaymentMethodId = _reflection.GeneratedProtocolMessageType('StripePaymentMethodId', (_message.Message,), {
  'DESCRIPTOR' : _STRIPEPAYMENTMETHODID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.StripePaymentMethodId)
  })
_sym_db.RegisterMessage(StripePaymentMethodId)

CreditsAttributionId = _reflection.GeneratedProtocolMessageType('CreditsAttributionId', (_message.Message,), {
  'DESCRIPTOR' : _CREDITSATTRIBUTIONID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.CreditsAttributionId)
  })
_sym_db.RegisterMessage(CreditsAttributionId)

Auth0OrganizationId = _reflection.GeneratedProtocolMessageType('Auth0OrganizationId', (_message.Message,), {
  'DESCRIPTOR' : _AUTH0ORGANIZATIONID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.Auth0OrganizationId)
  })
_sym_db.RegisterMessage(Auth0OrganizationId)

OrganizationInviteId = _reflection.GeneratedProtocolMessageType('OrganizationInviteId', (_message.Message,), {
  'DESCRIPTOR' : _ORGANIZATIONINVITEID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.OrganizationInviteId)
  })
_sym_db.RegisterMessage(OrganizationInviteId)

RoleId = _reflection.GeneratedProtocolMessageType('RoleId', (_message.Message,), {
  'DESCRIPTOR' : _ROLEID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.RoleId)
  })
_sym_db.RegisterMessage(RoleId)

Auth0ClientId = _reflection.GeneratedProtocolMessageType('Auth0ClientId', (_message.Message,), {
  'DESCRIPTOR' : _AUTH0CLIENTID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.Auth0ClientId)
  })
_sym_db.RegisterMessage(Auth0ClientId)

ConnectionId = _reflection.GeneratedProtocolMessageType('ConnectionId', (_message.Message,), {
  'DESCRIPTOR' : _CONNECTIONID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.ConnectionId)
  })
_sym_db.RegisterMessage(ConnectionId)

Auth0UserId = _reflection.GeneratedProtocolMessageType('Auth0UserId', (_message.Message,), {
  'DESCRIPTOR' : _AUTH0USERID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.Auth0UserId)
  })
_sym_db.RegisterMessage(Auth0UserId)

PipelineId = _reflection.GeneratedProtocolMessageType('PipelineId', (_message.Message,), {
  'DESCRIPTOR' : _PIPELINEID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.PipelineId)
  })
_sym_db.RegisterMessage(PipelineId)

TierId = _reflection.GeneratedProtocolMessageType('TierId', (_message.Message,), {
  'DESCRIPTOR' : _TIERID,
  '__module__' : 'api.ids_pb2'
  # @@protoc_insertion_point(class_scope:api.TierId)
  })
_sym_db.RegisterMessage(TierId)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\rcom.layer.apiP\000'
  _ACCOUNTID.fields_by_name['value']._options = None
  _ACCOUNTID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _COMPUTEFABRICID.fields_by_name['value']._options = None
  _COMPUTEFABRICID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _DATASETID.fields_by_name['value']._options = None
  _DATASETID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _DATASETVERSIONID.fields_by_name['value']._options = None
  _DATASETVERSIONID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _DATASETBUILDID.fields_by_name['value']._options = None
  _DATASETBUILDID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _GROUPID.fields_by_name['value']._options = None
  _GROUPID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _LOGGEDDATAID.fields_by_name['value']._options = None
  _LOGGEDDATAID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _MODELID.fields_by_name['value']._options = None
  _MODELID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _MODELTRAINID.fields_by_name['value']._options = None
  _MODELTRAINID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _MODELMETRICID.fields_by_name['value']._options = None
  _MODELMETRICID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _MODELVERSIONID.fields_by_name['value']._options = None
  _MODELVERSIONID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _HYPERPARAMETERTUNINGID.fields_by_name['value']._options = None
  _HYPERPARAMETERTUNINGID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _ORGANIZATIONID.fields_by_name['value']._options = None
  _ORGANIZATIONID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _USERID.fields_by_name['value']._options = None
  _USERID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _RUNID.fields_by_name['value']._options = None
  _RUNID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _PROJECTID.fields_by_name['value']._options = None
  _PROJECTID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _AUTH0CLIENTID.fields_by_name['value']._options = None
  _AUTH0CLIENTID.fields_by_name['value']._serialized_options = b'\372B\004r\002\020\001'
  _CONNECTIONID.fields_by_name['value']._options = None
  _CONNECTIONID.fields_by_name['value']._serialized_options = b'\372B\004r\002\020\001'
  _TIERID.fields_by_name['value']._options = None
  _TIERID.fields_by_name['value']._serialized_options = b'\372B\005r\003\260\001\001'
  _ACCOUNTID._serialized_start=47
  _ACCOUNTID._serialized_end=83
  _COMPUTEFABRICID._serialized_start=85
  _COMPUTEFABRICID._serialized_end=127
  _DATASETID._serialized_start=129
  _DATASETID._serialized_end=165
  _DATASETVERSIONID._serialized_start=167
  _DATASETVERSIONID._serialized_end=210
  _DATASETBUILDID._serialized_start=212
  _DATASETBUILDID._serialized_end=253
  _GROUPID._serialized_start=255
  _GROUPID._serialized_end=289
  _LOGGEDDATAID._serialized_start=291
  _LOGGEDDATAID._serialized_end=330
  _MODELID._serialized_start=332
  _MODELID._serialized_end=366
  _MODELTRAINID._serialized_start=368
  _MODELTRAINID._serialized_end=407
  _MODELMETRICID._serialized_start=409
  _MODELMETRICID._serialized_end=449
  _MODELVERSIONID._serialized_start=451
  _MODELVERSIONID._serialized_end=492
  _HYPERPARAMETERTUNINGID._serialized_start=494
  _HYPERPARAMETERTUNINGID._serialized_end=543
  _ORGANIZATIONID._serialized_start=545
  _ORGANIZATIONID._serialized_end=586
  _USERID._serialized_start=588
  _USERID._serialized_end=621
  _RUNID._serialized_start=623
  _RUNID._serialized_end=655
  _PROJECTID._serialized_start=657
  _PROJECTID._serialized_end=693
  _STRIPECUSTOMERID._serialized_start=695
  _STRIPECUSTOMERID._serialized_end=728
  _STRIPESETUPINTENTID._serialized_start=730
  _STRIPESETUPINTENTID._serialized_end=766
  _STRIPEPAYMENTMETHODID._serialized_start=768
  _STRIPEPAYMENTMETHODID._serialized_end=806
  _CREDITSATTRIBUTIONID._serialized_start=808
  _CREDITSATTRIBUTIONID._serialized_end=845
  _AUTH0ORGANIZATIONID._serialized_start=847
  _AUTH0ORGANIZATIONID._serialized_end=883
  _ORGANIZATIONINVITEID._serialized_start=885
  _ORGANIZATIONINVITEID._serialized_end=922
  _ROLEID._serialized_start=924
  _ROLEID._serialized_end=947
  _AUTH0CLIENTID._serialized_start=949
  _AUTH0CLIENTID._serialized_end=988
  _CONNECTIONID._serialized_start=990
  _CONNECTIONID._serialized_end=1028
  _AUTH0USERID._serialized_start=1030
  _AUTH0USERID._serialized_end=1058
  _PIPELINEID._serialized_start=1060
  _PIPELINEID._serialized_end=1087
  _TIERID._serialized_start=1089
  _TIERID._serialized_end=1122
# @@protoc_insertion_point(module_scope)
