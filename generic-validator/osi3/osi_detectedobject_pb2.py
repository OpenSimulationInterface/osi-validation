# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: osi3/osi_detectedobject.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from osi3 import osi_common_pb2 as osi3_dot_osi__common__pb2
from osi3 import osi_object_pb2 as osi3_dot_osi__object__pb2
from osi3 import osi_sensorspecific_pb2 as osi3_dot_osi__sensorspecific__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='osi3/osi_detectedobject.proto',
  package='osi3',
  syntax='proto2',
  serialized_options=_b('H\001'),
  serialized_pb=_b('\n\x1dosi3/osi_detectedobject.proto\x12\x04osi3\x1a\x15osi3/osi_common.proto\x1a\x15osi3/osi_object.proto\x1a\x1dosi3/osi_sensorspecific.proto\"\x8f\x03\n\x12\x44\x65tectedItemHeader\x12%\n\x0btracking_id\x18\x01 \x01(\x0b\x32\x10.osi3.Identifier\x12)\n\x0fground_truth_id\x18\x02 \x03(\x0b\x32\x10.osi3.Identifier\x12\x1d\n\x15\x65xistence_probability\x18\x03 \x01(\x01\x12\x0b\n\x03\x61ge\x18\x04 \x01(\x01\x12\x44\n\x11measurement_state\x18\x05 \x01(\x0e\x32).osi3.DetectedItemHeader.MeasurementState\x12#\n\tsensor_id\x18\x06 \x03(\x0b\x32\x10.osi3.Identifier\"\x8f\x01\n\x10MeasurementState\x12\x1d\n\x19MEASUREMENT_STATE_UNKNOWN\x10\x00\x12\x1b\n\x17MEASUREMENT_STATE_OTHER\x10\x01\x12\x1e\n\x1aMEASUREMENT_STATE_MEASURED\x10\x02\x12\x1f\n\x1bMEASUREMENT_STATE_PREDICTED\x10\x03\"\xcf\x02\n\x18\x44\x65tectedStationaryObject\x12(\n\x06header\x18\x01 \x01(\x0b\x32\x18.osi3.DetectedItemHeader\x12\"\n\x04\x62\x61se\x18\x02 \x01(\x0b\x32\x14.osi3.BaseStationary\x12\'\n\tbase_rmse\x18\x03 \x01(\x0b\x32\x14.osi3.BaseStationary\x12K\n\tcandidate\x18\x04 \x03(\x0b\x32\x38.osi3.DetectedStationaryObject.CandidateStationaryObject\x1ao\n\x19\x43\x61ndidateStationaryObject\x12\x13\n\x0bprobability\x18\x01 \x01(\x01\x12=\n\x0e\x63lassification\x18\x02 \x01(\x0b\x32%.osi3.StationaryObject.Classification\"\x84\x0b\n\x14\x44\x65tectedMovingObject\x12(\n\x06header\x18\x01 \x01(\x0b\x32\x18.osi3.DetectedItemHeader\x12\x1e\n\x04\x62\x61se\x18\x02 \x01(\x0b\x32\x10.osi3.BaseMoving\x12#\n\tbase_rmse\x18\x03 \x01(\x0b\x32\x10.osi3.BaseMoving\x12\x42\n\x0freference_point\x18\x04 \x01(\x0e\x32).osi3.DetectedMovingObject.ReferencePoint\x12@\n\x0emovement_state\x18\x05 \x01(\x0e\x32(.osi3.DetectedMovingObject.MovementState\x12!\n\x19percentage_side_lane_left\x18\x06 \x01(\x01\x12\"\n\x1apercentage_side_lane_right\x18\x07 \x01(\x01\x12\x43\n\tcandidate\x18\x08 \x03(\x0b\x32\x30.osi3.DetectedMovingObject.CandidateMovingObject\x12\x36\n\x0fradar_specifics\x18\x64 \x01(\x0b\x32\x1d.osi3.RadarSpecificObjectData\x12\x36\n\x0flidar_specifics\x18\x65 \x01(\x0b\x32\x1d.osi3.LidarSpecificObjectData\x12\x38\n\x10\x63\x61mera_specifics\x18\x66 \x01(\x0b\x32\x1e.osi3.CameraSpecificObjectData\x12@\n\x14ultrasonic_specifics\x18g \x01(\x0b\x32\".osi3.UltrasonicSpecificObjectData\x1a\xf3\x01\n\x15\x43\x61ndidateMovingObject\x12\x13\n\x0bprobability\x18\x01 \x01(\x01\x12%\n\x04type\x18\x02 \x01(\x0e\x32\x17.osi3.MovingObject.Type\x12H\n\x16vehicle_classification\x18\x03 \x01(\x0b\x32(.osi3.MovingObject.VehicleClassification\x12&\n\thead_pose\x18\x04 \x01(\x0b\x32\x13.osi3.Orientation3d\x12,\n\x0fupper_body_pose\x18\x05 \x01(\x0b\x32\x13.osi3.Orientation3d\"\xea\x02\n\x0eReferencePoint\x12\x1b\n\x17REFERENCE_POINT_UNKNOWN\x10\x00\x12\x19\n\x15REFERENCE_POINT_OTHER\x10\x01\x12\x1a\n\x16REFERENCE_POINT_CENTER\x10\x02\x12\x1f\n\x1bREFERENCE_POINT_MIDDLE_LEFT\x10\x03\x12 \n\x1cREFERENCE_POINT_MIDDLE_RIGHT\x10\x04\x12\x1f\n\x1bREFERENCE_POINT_REAR_MIDDLE\x10\x05\x12\x1d\n\x19REFERENCE_POINT_REAR_LEFT\x10\x06\x12\x1e\n\x1aREFERENCE_POINT_REAR_RIGHT\x10\x07\x12 \n\x1cREFERENCE_POINT_FRONT_MIDDLE\x10\x08\x12\x1e\n\x1aREFERENCE_POINT_FRONT_LEFT\x10\t\x12\x1f\n\x1bREFERENCE_POINT_FRONT_RIGHT\x10\n\"\x9b\x01\n\rMovementState\x12\x1a\n\x16MOVEMENT_STATE_UNKNOWN\x10\x00\x12\x18\n\x14MOVEMENT_STATE_OTHER\x10\x01\x12\x1d\n\x19MOVEMENT_STATE_STATIONARY\x10\x02\x12\x19\n\x15MOVEMENT_STATE_MOVING\x10\x03\x12\x1a\n\x16MOVEMENT_STATE_STOPPED\x10\x04\x42\x02H\x01')
  ,
  dependencies=[osi3_dot_osi__common__pb2.DESCRIPTOR,osi3_dot_osi__object__pb2.DESCRIPTOR,osi3_dot_osi__sensorspecific__pb2.DESCRIPTOR,])



_DETECTEDITEMHEADER_MEASUREMENTSTATE = _descriptor.EnumDescriptor(
  name='MeasurementState',
  full_name='osi3.DetectedItemHeader.MeasurementState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MEASUREMENT_STATE_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MEASUREMENT_STATE_OTHER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MEASUREMENT_STATE_MEASURED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MEASUREMENT_STATE_PREDICTED', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=373,
  serialized_end=516,
)
_sym_db.RegisterEnumDescriptor(_DETECTEDITEMHEADER_MEASUREMENTSTATE)

_DETECTEDMOVINGOBJECT_REFERENCEPOINT = _descriptor.EnumDescriptor(
  name='ReferencePoint',
  full_name='osi3.DetectedMovingObject.ReferencePoint',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_OTHER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_CENTER', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_MIDDLE_LEFT', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_MIDDLE_RIGHT', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_REAR_MIDDLE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_REAR_LEFT', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_REAR_RIGHT', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_FRONT_MIDDLE', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_FRONT_LEFT', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_POINT_FRONT_RIGHT', index=10, number=10,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1749,
  serialized_end=2111,
)
_sym_db.RegisterEnumDescriptor(_DETECTEDMOVINGOBJECT_REFERENCEPOINT)

_DETECTEDMOVINGOBJECT_MOVEMENTSTATE = _descriptor.EnumDescriptor(
  name='MovementState',
  full_name='osi3.DetectedMovingObject.MovementState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MOVEMENT_STATE_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOVEMENT_STATE_OTHER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOVEMENT_STATE_STATIONARY', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOVEMENT_STATE_MOVING', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOVEMENT_STATE_STOPPED', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2114,
  serialized_end=2269,
)
_sym_db.RegisterEnumDescriptor(_DETECTEDMOVINGOBJECT_MOVEMENTSTATE)


_DETECTEDITEMHEADER = _descriptor.Descriptor(
  name='DetectedItemHeader',
  full_name='osi3.DetectedItemHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tracking_id', full_name='osi3.DetectedItemHeader.tracking_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ground_truth_id', full_name='osi3.DetectedItemHeader.ground_truth_id', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='existence_probability', full_name='osi3.DetectedItemHeader.existence_probability', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='age', full_name='osi3.DetectedItemHeader.age', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='measurement_state', full_name='osi3.DetectedItemHeader.measurement_state', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sensor_id', full_name='osi3.DetectedItemHeader.sensor_id', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DETECTEDITEMHEADER_MEASUREMENTSTATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=117,
  serialized_end=516,
)


_DETECTEDSTATIONARYOBJECT_CANDIDATESTATIONARYOBJECT = _descriptor.Descriptor(
  name='CandidateStationaryObject',
  full_name='osi3.DetectedStationaryObject.CandidateStationaryObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='probability', full_name='osi3.DetectedStationaryObject.CandidateStationaryObject.probability', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='classification', full_name='osi3.DetectedStationaryObject.CandidateStationaryObject.classification', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=743,
  serialized_end=854,
)

_DETECTEDSTATIONARYOBJECT = _descriptor.Descriptor(
  name='DetectedStationaryObject',
  full_name='osi3.DetectedStationaryObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='osi3.DetectedStationaryObject.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='base', full_name='osi3.DetectedStationaryObject.base', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='base_rmse', full_name='osi3.DetectedStationaryObject.base_rmse', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='candidate', full_name='osi3.DetectedStationaryObject.candidate', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_DETECTEDSTATIONARYOBJECT_CANDIDATESTATIONARYOBJECT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=519,
  serialized_end=854,
)


_DETECTEDMOVINGOBJECT_CANDIDATEMOVINGOBJECT = _descriptor.Descriptor(
  name='CandidateMovingObject',
  full_name='osi3.DetectedMovingObject.CandidateMovingObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='probability', full_name='osi3.DetectedMovingObject.CandidateMovingObject.probability', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='osi3.DetectedMovingObject.CandidateMovingObject.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vehicle_classification', full_name='osi3.DetectedMovingObject.CandidateMovingObject.vehicle_classification', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='head_pose', full_name='osi3.DetectedMovingObject.CandidateMovingObject.head_pose', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='upper_body_pose', full_name='osi3.DetectedMovingObject.CandidateMovingObject.upper_body_pose', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1503,
  serialized_end=1746,
)

_DETECTEDMOVINGOBJECT = _descriptor.Descriptor(
  name='DetectedMovingObject',
  full_name='osi3.DetectedMovingObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='osi3.DetectedMovingObject.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='base', full_name='osi3.DetectedMovingObject.base', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='base_rmse', full_name='osi3.DetectedMovingObject.base_rmse', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reference_point', full_name='osi3.DetectedMovingObject.reference_point', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='movement_state', full_name='osi3.DetectedMovingObject.movement_state', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='percentage_side_lane_left', full_name='osi3.DetectedMovingObject.percentage_side_lane_left', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='percentage_side_lane_right', full_name='osi3.DetectedMovingObject.percentage_side_lane_right', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='candidate', full_name='osi3.DetectedMovingObject.candidate', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='radar_specifics', full_name='osi3.DetectedMovingObject.radar_specifics', index=8,
      number=100, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lidar_specifics', full_name='osi3.DetectedMovingObject.lidar_specifics', index=9,
      number=101, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='camera_specifics', full_name='osi3.DetectedMovingObject.camera_specifics', index=10,
      number=102, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ultrasonic_specifics', full_name='osi3.DetectedMovingObject.ultrasonic_specifics', index=11,
      number=103, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_DETECTEDMOVINGOBJECT_CANDIDATEMOVINGOBJECT, ],
  enum_types=[
    _DETECTEDMOVINGOBJECT_REFERENCEPOINT,
    _DETECTEDMOVINGOBJECT_MOVEMENTSTATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=857,
  serialized_end=2269,
)

_DETECTEDITEMHEADER.fields_by_name['tracking_id'].message_type = osi3_dot_osi__common__pb2._IDENTIFIER
_DETECTEDITEMHEADER.fields_by_name['ground_truth_id'].message_type = osi3_dot_osi__common__pb2._IDENTIFIER
_DETECTEDITEMHEADER.fields_by_name['measurement_state'].enum_type = _DETECTEDITEMHEADER_MEASUREMENTSTATE
_DETECTEDITEMHEADER.fields_by_name['sensor_id'].message_type = osi3_dot_osi__common__pb2._IDENTIFIER
_DETECTEDITEMHEADER_MEASUREMENTSTATE.containing_type = _DETECTEDITEMHEADER
_DETECTEDSTATIONARYOBJECT_CANDIDATESTATIONARYOBJECT.fields_by_name['classification'].message_type = osi3_dot_osi__object__pb2._STATIONARYOBJECT_CLASSIFICATION
_DETECTEDSTATIONARYOBJECT_CANDIDATESTATIONARYOBJECT.containing_type = _DETECTEDSTATIONARYOBJECT
_DETECTEDSTATIONARYOBJECT.fields_by_name['header'].message_type = _DETECTEDITEMHEADER
_DETECTEDSTATIONARYOBJECT.fields_by_name['base'].message_type = osi3_dot_osi__common__pb2._BASESTATIONARY
_DETECTEDSTATIONARYOBJECT.fields_by_name['base_rmse'].message_type = osi3_dot_osi__common__pb2._BASESTATIONARY
_DETECTEDSTATIONARYOBJECT.fields_by_name['candidate'].message_type = _DETECTEDSTATIONARYOBJECT_CANDIDATESTATIONARYOBJECT
_DETECTEDMOVINGOBJECT_CANDIDATEMOVINGOBJECT.fields_by_name['type'].enum_type = osi3_dot_osi__object__pb2._MOVINGOBJECT_TYPE
_DETECTEDMOVINGOBJECT_CANDIDATEMOVINGOBJECT.fields_by_name['vehicle_classification'].message_type = osi3_dot_osi__object__pb2._MOVINGOBJECT_VEHICLECLASSIFICATION
_DETECTEDMOVINGOBJECT_CANDIDATEMOVINGOBJECT.fields_by_name['head_pose'].message_type = osi3_dot_osi__common__pb2._ORIENTATION3D
_DETECTEDMOVINGOBJECT_CANDIDATEMOVINGOBJECT.fields_by_name['upper_body_pose'].message_type = osi3_dot_osi__common__pb2._ORIENTATION3D
_DETECTEDMOVINGOBJECT_CANDIDATEMOVINGOBJECT.containing_type = _DETECTEDMOVINGOBJECT
_DETECTEDMOVINGOBJECT.fields_by_name['header'].message_type = _DETECTEDITEMHEADER
_DETECTEDMOVINGOBJECT.fields_by_name['base'].message_type = osi3_dot_osi__common__pb2._BASEMOVING
_DETECTEDMOVINGOBJECT.fields_by_name['base_rmse'].message_type = osi3_dot_osi__common__pb2._BASEMOVING
_DETECTEDMOVINGOBJECT.fields_by_name['reference_point'].enum_type = _DETECTEDMOVINGOBJECT_REFERENCEPOINT
_DETECTEDMOVINGOBJECT.fields_by_name['movement_state'].enum_type = _DETECTEDMOVINGOBJECT_MOVEMENTSTATE
_DETECTEDMOVINGOBJECT.fields_by_name['candidate'].message_type = _DETECTEDMOVINGOBJECT_CANDIDATEMOVINGOBJECT
_DETECTEDMOVINGOBJECT.fields_by_name['radar_specifics'].message_type = osi3_dot_osi__sensorspecific__pb2._RADARSPECIFICOBJECTDATA
_DETECTEDMOVINGOBJECT.fields_by_name['lidar_specifics'].message_type = osi3_dot_osi__sensorspecific__pb2._LIDARSPECIFICOBJECTDATA
_DETECTEDMOVINGOBJECT.fields_by_name['camera_specifics'].message_type = osi3_dot_osi__sensorspecific__pb2._CAMERASPECIFICOBJECTDATA
_DETECTEDMOVINGOBJECT.fields_by_name['ultrasonic_specifics'].message_type = osi3_dot_osi__sensorspecific__pb2._ULTRASONICSPECIFICOBJECTDATA
_DETECTEDMOVINGOBJECT_REFERENCEPOINT.containing_type = _DETECTEDMOVINGOBJECT
_DETECTEDMOVINGOBJECT_MOVEMENTSTATE.containing_type = _DETECTEDMOVINGOBJECT
DESCRIPTOR.message_types_by_name['DetectedItemHeader'] = _DETECTEDITEMHEADER
DESCRIPTOR.message_types_by_name['DetectedStationaryObject'] = _DETECTEDSTATIONARYOBJECT
DESCRIPTOR.message_types_by_name['DetectedMovingObject'] = _DETECTEDMOVINGOBJECT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DetectedItemHeader = _reflection.GeneratedProtocolMessageType('DetectedItemHeader', (_message.Message,), dict(
  DESCRIPTOR = _DETECTEDITEMHEADER,
  __module__ = 'osi3.osi_detectedobject_pb2'
  # @@protoc_insertion_point(class_scope:osi3.DetectedItemHeader)
  ))
_sym_db.RegisterMessage(DetectedItemHeader)

DetectedStationaryObject = _reflection.GeneratedProtocolMessageType('DetectedStationaryObject', (_message.Message,), dict(

  CandidateStationaryObject = _reflection.GeneratedProtocolMessageType('CandidateStationaryObject', (_message.Message,), dict(
    DESCRIPTOR = _DETECTEDSTATIONARYOBJECT_CANDIDATESTATIONARYOBJECT,
    __module__ = 'osi3.osi_detectedobject_pb2'
    # @@protoc_insertion_point(class_scope:osi3.DetectedStationaryObject.CandidateStationaryObject)
    ))
  ,
  DESCRIPTOR = _DETECTEDSTATIONARYOBJECT,
  __module__ = 'osi3.osi_detectedobject_pb2'
  # @@protoc_insertion_point(class_scope:osi3.DetectedStationaryObject)
  ))
_sym_db.RegisterMessage(DetectedStationaryObject)
_sym_db.RegisterMessage(DetectedStationaryObject.CandidateStationaryObject)

DetectedMovingObject = _reflection.GeneratedProtocolMessageType('DetectedMovingObject', (_message.Message,), dict(

  CandidateMovingObject = _reflection.GeneratedProtocolMessageType('CandidateMovingObject', (_message.Message,), dict(
    DESCRIPTOR = _DETECTEDMOVINGOBJECT_CANDIDATEMOVINGOBJECT,
    __module__ = 'osi3.osi_detectedobject_pb2'
    # @@protoc_insertion_point(class_scope:osi3.DetectedMovingObject.CandidateMovingObject)
    ))
  ,
  DESCRIPTOR = _DETECTEDMOVINGOBJECT,
  __module__ = 'osi3.osi_detectedobject_pb2'
  # @@protoc_insertion_point(class_scope:osi3.DetectedMovingObject)
  ))
_sym_db.RegisterMessage(DetectedMovingObject)
_sym_db.RegisterMessage(DetectedMovingObject.CandidateMovingObject)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
