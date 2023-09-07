import rclpy
from rclpy.node import Node 

# 터틀봇 메시지 사용위함
from ssafy_msgs.msg import TurtlebotStatus
# 각변환
from squaternion import Quaternion
# 결과 변환
from nav_msgs.msg import Odometry
from math import pi, cos, sin
# tf2_ros에 broadcaster 사용 위함
import tf2_ros
# broadcast 할 메시지를 담고있는 geometry_msgs 사용위함
import geometry_msgs.msg 

class odom(Node):
    def __init__(self):
        super().__init__('odom')

        # 상태를 받아 내보냄
        self.status_sub = self.create_subscription(TurtlebotStatus, '/turtlebot_status', self.status_callback, 10)
        self.odom_publisher = self.create_publisher(Odometry, 'odom', 10)

        # 좌표계 상관관계 정의
        self.broadcaster = tf2_ros.StaticTransformBroadcaster(self)
        self.odom_msg = Odometry()
        self.base_link_transform = geometry_msgs.msg.TransformStamped()
        self.is_status = False
        self.is_calc_theta = False

        self.x = 0
        self.y = 0
        self.theta = 0
        self.prev_time = 0

        #좌표계 이름 넣고 베이스 넣어줌
        # map 좌표계 위에 odometry가 그려진다
        self.odom_msg.header.frame_id = 'map'
        self.odom_msg.child_frame_id = 'base_link'

        # map -> base_link 좌표계 이름 설정
        self.base_link_transform = geometry_msgs.msg.TransformStamped()
        self.base_link_transform.header.frame_id = 'map'
        self.base_link_transform.child_frame_id = 'base_link'
        
        # base_link -> laser 좌표계 이름 설정
        self.laser_transform = geometry_msgs.msg.TransformStamped()
        self.laser_transform.header.frame_id = 'base_link'
        self.laser_transform.child_frame_id = 'laser'
        # 매번 계산해줘서 바꿈
        # 바뀌지 않는 값은 설정
        self.laser_transform.transform.translation.x = 0.0
        self.laser_transform.transform.translation.y = 0.0
        self.laser_transform.transform.translation.z = 0.0
        self.laser_transform.transform.rotation.w = 1.0

    def status_callback(self, msg):
        if self.is_status == False :
            self.is_status = True
            # 적분을 하기 위함.
            self.prev_time = rclpy.clock.Clock().now()
        else :
            self.current_time = rclpy.clock.Clock().now()
            self.period = (self.current_time - self.prev_time).nanoseconds/1000000000
            
            # 각도 저장
            linear_x = msg.twist.linear.x
            angular_z = msg.twist.angular.z

            # 최종 좌표
            self.x += linear_x * cos(self.theta) * self.period
            self.y += linear_x * sin(self.theta) * self.period
            self.theta += angular_z * self.period

            # 오일러 -> 쿼터니언
            # ros 는 쿼터니언 사용
            q = Quaternion.from_euler(0, 0, self.theta)

            self.base_link_transform.header.stamp = rclpy.clock.Clock().now().to_msg()
            self.laser_transform.header.stamp = rclpy.clock.Clock().now().to_msg()
            self.base_link_transform.transform.translation.x = self.x
            self.base_link_transform.transform.translation.y = self.y
            self.base_link_transform.transform.rotation.x = q.x
            self.base_link_transform.transform.rotation.y = q.y
            self.base_link_transform.transform.rotation.z = q.z
            self.base_link_transform.transform.rotation.w = q.w

            self.odom_msg.pose.pose.position.x = self.x
            self.odom_msg.pose.pose.position.y = self.y
            self.odom_msg.pose.pose.orientation.x = q.x
            self.odom_msg.pose.pose.orientation.y = q.y
            self.odom_msg.pose.pose.orientation.z = q.z
            self.odom_msg.pose.pose.orientation.w = q.w
            self.odom_msg.twist.twist.linear.x = linear_x
            self.odom_msg.twist.twist.angular.x = angular_z

            self.broadcaster.sendTransform(self.base_link_transform)
            self.broadcaster.sendTransform(self.laser_transform)

            self.odom_publisher.publish(self.odom_msg)
            self.prev_time = self.current_time

def main(args=None) :
    rclpy.init(args=args)
    odom_path = odom()
    rclpy.spin(odom_path)
    odom_path.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()