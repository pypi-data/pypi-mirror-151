# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/value/credit_log_event.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from layerapi.api.entity import entity_pb2 as api_dot_entity_dot_entity__pb2
from layerapi.api import ids_pb2 as api_dot_ids__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n api/value/credit_log_event.proto\x12\x03\x61pi\x1a\x17\x61pi/entity/entity.proto\x1a\rapi/ids.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xc4\x02\n\x0e\x43reditLogEvent\x12(\n\x04time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12$\n\x0fperformed_by_id\x18\x02 \x01(\x0b\x32\x0b.api.UserId\x12\x1a\n\x12\x65ntity_description\x18\x03 \x01(\t\x12\x13\n\x0b\x65ntity_path\x18\x04 \x01(\t\x12\x1a\n\x12\x63redits_difference\x18\x05 \x01(\t\x12$\n\x0b\x65ntity_type\x18\x06 \x01(\x0e\x32\x0f.api.EntityType\x12\x13\n\x0b\x65ntity_name\x18\x07 \x01(\t\x12\x10\n\x08\x64uration\x18\x08 \x01(\t\x12\x0e\n\x06\x66\x61\x62ric\x18\t \x01(\t\x12\x14\n\x0cproject_name\x18\n \x01(\t\x12\"\n\naccount_id\x18\x0b \x01(\x0b\x32\x0e.api.AccountIdB\x11\n\rcom.layer.apiP\x01\x62\x06proto3')



_CREDITLOGEVENT = DESCRIPTOR.message_types_by_name['CreditLogEvent']
CreditLogEvent = _reflection.GeneratedProtocolMessageType('CreditLogEvent', (_message.Message,), {
  'DESCRIPTOR' : _CREDITLOGEVENT,
  '__module__' : 'api.value.credit_log_event_pb2'
  # @@protoc_insertion_point(class_scope:api.CreditLogEvent)
  })
_sym_db.RegisterMessage(CreditLogEvent)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\rcom.layer.apiP\001'
  _CREDITLOGEVENT._serialized_start=115
  _CREDITLOGEVENT._serialized_end=439
# @@protoc_insertion_point(module_scope)
