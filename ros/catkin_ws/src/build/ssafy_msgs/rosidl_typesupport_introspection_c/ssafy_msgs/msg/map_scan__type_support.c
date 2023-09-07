// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from ssafy_msgs:msg\MapScan.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "ssafy_msgs/msg/map_scan__rosidl_typesupport_introspection_c.h"
#include "ssafy_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "ssafy_msgs/msg/map_scan__functions.h"
#include "ssafy_msgs/msg/map_scan__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void MapScan__rosidl_typesupport_introspection_c__MapScan_init_function(
  void * message_memory, enum rosidl_runtime_c_message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  ssafy_msgs__msg__MapScan__init(message_memory);
}

void MapScan__rosidl_typesupport_introspection_c__MapScan_fini_function(void * message_memory)
{
  ssafy_msgs__msg__MapScan__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember MapScan__rosidl_typesupport_introspection_c__MapScan_message_member_array[1] = {
  {
    "run",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ssafy_msgs__msg__MapScan, run),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers MapScan__rosidl_typesupport_introspection_c__MapScan_message_members = {
  "ssafy_msgs__msg",  // message namespace
  "MapScan",  // message name
  1,  // number of fields
  sizeof(ssafy_msgs__msg__MapScan),
  MapScan__rosidl_typesupport_introspection_c__MapScan_message_member_array,  // message members
  MapScan__rosidl_typesupport_introspection_c__MapScan_init_function,  // function to initialize message memory (memory has to be allocated)
  MapScan__rosidl_typesupport_introspection_c__MapScan_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t MapScan__rosidl_typesupport_introspection_c__MapScan_message_type_support_handle = {
  0,
  &MapScan__rosidl_typesupport_introspection_c__MapScan_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_ssafy_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ssafy_msgs, msg, MapScan)() {
  if (!MapScan__rosidl_typesupport_introspection_c__MapScan_message_type_support_handle.typesupport_identifier) {
    MapScan__rosidl_typesupport_introspection_c__MapScan_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &MapScan__rosidl_typesupport_introspection_c__MapScan_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
