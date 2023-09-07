// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from ssafy_msgs:msg\MapScan.idl
// generated code does not contain a copyright notice
#include "ssafy_msgs/msg/map_scan__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


bool
ssafy_msgs__msg__MapScan__init(ssafy_msgs__msg__MapScan * msg)
{
  if (!msg) {
    return false;
  }
  // run
  return true;
}

void
ssafy_msgs__msg__MapScan__fini(ssafy_msgs__msg__MapScan * msg)
{
  if (!msg) {
    return;
  }
  // run
}

ssafy_msgs__msg__MapScan *
ssafy_msgs__msg__MapScan__create()
{
  ssafy_msgs__msg__MapScan * msg = (ssafy_msgs__msg__MapScan *)malloc(sizeof(ssafy_msgs__msg__MapScan));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(ssafy_msgs__msg__MapScan));
  bool success = ssafy_msgs__msg__MapScan__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
ssafy_msgs__msg__MapScan__destroy(ssafy_msgs__msg__MapScan * msg)
{
  if (msg) {
    ssafy_msgs__msg__MapScan__fini(msg);
  }
  free(msg);
}


bool
ssafy_msgs__msg__MapScan__Sequence__init(ssafy_msgs__msg__MapScan__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  ssafy_msgs__msg__MapScan * data = NULL;
  if (size) {
    data = (ssafy_msgs__msg__MapScan *)calloc(size, sizeof(ssafy_msgs__msg__MapScan));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = ssafy_msgs__msg__MapScan__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        ssafy_msgs__msg__MapScan__fini(&data[i - 1]);
      }
      free(data);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
ssafy_msgs__msg__MapScan__Sequence__fini(ssafy_msgs__msg__MapScan__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      ssafy_msgs__msg__MapScan__fini(&array->data[i]);
    }
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

ssafy_msgs__msg__MapScan__Sequence *
ssafy_msgs__msg__MapScan__Sequence__create(size_t size)
{
  ssafy_msgs__msg__MapScan__Sequence * array = (ssafy_msgs__msg__MapScan__Sequence *)malloc(sizeof(ssafy_msgs__msg__MapScan__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = ssafy_msgs__msg__MapScan__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
ssafy_msgs__msg__MapScan__Sequence__destroy(ssafy_msgs__msg__MapScan__Sequence * array)
{
  if (array) {
    ssafy_msgs__msg__MapScan__Sequence__fini(array);
  }
  free(array);
}
