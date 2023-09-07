// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from ssafy_msgs:msg\MapScan.idl
// generated code does not contain a copyright notice

#ifndef SSAFY_MSGS__MSG__MAP_SCAN__STRUCT_HPP_
#define SSAFY_MSGS__MSG__MAP_SCAN__STRUCT_HPP_

#include <rosidl_generator_cpp/bounded_vector.hpp>
#include <rosidl_generator_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__ssafy_msgs__msg__MapScan __attribute__((deprecated))
#else
# define DEPRECATED__ssafy_msgs__msg__MapScan __declspec(deprecated)
#endif

namespace ssafy_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MapScan_
{
  using Type = MapScan_<ContainerAllocator>;

  explicit MapScan_(rosidl_generator_cpp::MessageInitialization _init = rosidl_generator_cpp::MessageInitialization::ALL)
  {
    if (rosidl_generator_cpp::MessageInitialization::ALL == _init ||
      rosidl_generator_cpp::MessageInitialization::ZERO == _init)
    {
      this->run = 0l;
    }
  }

  explicit MapScan_(const ContainerAllocator & _alloc, rosidl_generator_cpp::MessageInitialization _init = rosidl_generator_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_generator_cpp::MessageInitialization::ALL == _init ||
      rosidl_generator_cpp::MessageInitialization::ZERO == _init)
    {
      this->run = 0l;
    }
  }

  // field types and members
  using _run_type =
    int32_t;
  _run_type run;

  // setters for named parameter idiom
  Type & set__run(
    const int32_t & _arg)
  {
    this->run = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ssafy_msgs::msg::MapScan_<ContainerAllocator> *;
  using ConstRawPtr =
    const ssafy_msgs::msg::MapScan_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ssafy_msgs::msg::MapScan_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ssafy_msgs::msg::MapScan_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ssafy_msgs::msg::MapScan_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ssafy_msgs::msg::MapScan_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ssafy_msgs::msg::MapScan_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ssafy_msgs::msg::MapScan_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ssafy_msgs::msg::MapScan_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ssafy_msgs::msg::MapScan_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ssafy_msgs__msg__MapScan
    std::shared_ptr<ssafy_msgs::msg::MapScan_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ssafy_msgs__msg__MapScan
    std::shared_ptr<ssafy_msgs::msg::MapScan_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MapScan_ & other) const
  {
    if (this->run != other.run) {
      return false;
    }
    return true;
  }
  bool operator!=(const MapScan_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MapScan_

// alias to use template instance with default allocator
using MapScan =
  ssafy_msgs::msg::MapScan_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace ssafy_msgs

#endif  // SSAFY_MSGS__MSG__MAP_SCAN__STRUCT_HPP_
