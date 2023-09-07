// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from ssafy_msgs:msg\MapScan.idl
// generated code does not contain a copyright notice

#ifndef SSAFY_MSGS__MSG__MAP_SCAN__STRUCT_H_
#define SSAFY_MSGS__MSG__MAP_SCAN__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/MapScan in the package ssafy_msgs.
typedef struct ssafy_msgs__msg__MapScan
{
  int32_t run;
} ssafy_msgs__msg__MapScan;

// Struct for a sequence of ssafy_msgs__msg__MapScan.
typedef struct ssafy_msgs__msg__MapScan__Sequence
{
  ssafy_msgs__msg__MapScan * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ssafy_msgs__msg__MapScan__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SSAFY_MSGS__MSG__MAP_SCAN__STRUCT_H_
