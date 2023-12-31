import rclpy
from rclpy.node import Node
import ros2pkg
from geometry_msgs.msg import Twist,PoseStamped,Pose,TransformStamped
from sensor_msgs.msg import Imu,LaserScan
from std_msgs.msg import Float32, Int8MultiArray
from squaternion import Quaternion
from nav_msgs.msg import Odometry,Path,OccupancyGrid,MapMetaData
from math import pi,cos,sin,sqrt
import tf2_ros
import os
import ssak3.utils as utils
import numpy as np
import cv2
import time

from rclpy.qos import qos_profile_sensor_data, QoSProfile
# mapping node의 전체 로직 순서
# 1. publisher, subscriber, msg 생성
# 2. mapping 클래스 생성
# 3. 맵의 resolution, 중심좌표, occupancy에 대한 threshold 등의 설정 받기
# 4. laser scan 메시지 안의 ground truth pose 받기
# 5. lidar scan 결과 수신
# 6. map 업데이트 시작
# 7. pose 값을 받아서 좌표변환 행렬로 정의
# 8. laser scan 데이터 좌표 변환
# 9. pose와 laser의 grid map index 변환
# 10. laser scan 공간을 맵에 표시
# 11. 업데이트 중인 map publish
# 12. 맵 저장

params_map = {
    "MAP_RESOLUTION": 0.05,
    "OCCUPANCY_UP": 0.02,
    "OCCUPANCY_DOWN": 0.01,
    "MAP_CENTER": (-8.0, 10.0),
    "MAP_SIZE": (17.5, 17.5),
    "MAP_FILENAME": 'test.png',
    "MAPVIS_RESIZE_SCALE": 2.0
}


def createLineIterator(P1, P2, img):
    """
    Produces and array that consists of the coordinates and intensities of each pixel in a line between two points

    Parameters:
        -P1: a numpy array that consists of the coordinate of the first point (x,y)
        -P2: a numpy array that consists of the coordinate of the second point (x,y)
        -img: the image being processed

    Returns:
        -it: a numpy array that consists of the coordinates and intensities of each pixel in the radii (shape: [numPixels, 3], row = [x,y,intensity])
    """
    # 로직 순서
    # 1. 두 점을 있는 백터의 x, y 값과 크기 계산
    # 2. 직선을 그릴 grid map의 픽셀 좌표를 넣을 numpy array 를 predifine
    # 3. 직선 방향 체크
    # 4. 수직선의 픽셀 좌표 계산
    # 5. 수평선의 픽셀 좌표 계산
    # 6. 대각선의 픽셀 좌표 계산
    # 7. 맵 바깥 픽셀 좌표 삭제

   #define local variables for readability
    imageH = img.shape[0] #height
    imageW = img.shape[1] #width
    P1Y = P1[1] #시작점 y 픽셀 좌표
    P1X = P1[0] #시작점 x 픽셀 좌표
    P2X = P2[0] #끝점 y 픽셀 좌표
    P2Y = P2[1] #끝점 x 픽셀 좌표

    #difference and absolute difference between points
    #used to calculate slope and relative location between points
    dX = P2X - P1X
    dY = P2Y - P1Y
    dXa = np.abs(dX)
    dYa = np.abs(dY)

    #predefine numpy array for output based on distance between points
    itbuffer = np.empty(shape=(np.maximum(dYa,dXa),3),dtype=np.float32)
    itbuffer.fill(np.nan)

    #Obtain coordinates along the line using a form of Bresenham's algorithm
    negY = P1Y > P2Y
    negX = P1X > P2X
    if P1X == P2X: #vertical line segment
        itbuffer[:,0] = P1X
        if negY:
            itbuffer[:,1] = np.arange(P1Y - 1,P1Y - dYa - 1,-1)
        else:
            itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
    elif P1Y == P2Y: #horizontal line segment
        itbuffer[:,1] = P1Y
        if negX:
            itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
        else:
            itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
    else: #diagonal line segment
        steepSlope = dYa > dXa
        if steepSlope:
            slope = dX.astype(np.float32)/dY.astype(np.float32)
            if negY:
                itbuffer[:,1] = np.arange(P1Y-1,P1Y-dYa-1,-1)
            else:
                itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
            itbuffer[:,0] = (slope*(itbuffer[:,1]-P1Y)).astype(int) + P1X
        else:
            slope = dY.astype(np.float32)/dX.astype(np.float32)
            if negX:
                itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
            else:
                itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
            itbuffer[:,1] = (slope*(itbuffer[:,0]-P1X)).astype(int) + P1Y

    #Remove points outside of image
    colX = itbuffer[:,0]
    colY = itbuffer[:,1]
    itbuffer = itbuffer[(colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)]

    #Get intensities from img ndarray
    itbuffer[:,2] = img[itbuffer[:,1].astype(np.uint),itbuffer[:,0].astype(np.uint)]

    return itbuffer


class Mapping:
    """
    Mapping Class
    """
    def __init__(self, params_map):
        self.odom_msg = Odometry()
        self.map_resolution = params_map["MAP_RESOLUTION"]
        self.map_size = np.array(params_map["MAP_SIZE"]) / self.map_resolution
        self.map_center = params_map["MAP_CENTER"]
        self.map = np.ones((self.map_size[0].astype(np.int), self.map_size[1].astype(np.int)))*0.5
        self.occu_up = params_map["OCCUPANCY_UP"]
        self.occu_down = params_map["OCCUPANCY_DOWN"]
        self.map_filename = params_map["MAP_FILENAME"]
        self.map_vis_resize_scale = params_map["MAPVIS_RESIZE_SCALE"]

        self.T_r_l = np.array([[0,-1,0],[1,0,0],[0,0,1]])


    def update(self, pose, laser): # pose에 현재 x, y, theta값이 들어있음
        n_points = laser.shape[1]
        pose_mat = utils.xyh2mat2D(pose) # util.py의 xyh2mat2D가 좌표변환 알고리즘
        # numpy method
        # matmul : 행렬 끼리의 곱연산
        # ones : tuple형으로 (행, 열) 입력해주면 행 * 열 사이즈의 1로 채워진 행렬 만들어줌
        pose_mat = np.matmul(pose_mat,self.T_r_l)
        laser_mat = np.ones((3, n_points))
        laser_mat[:2, :] = laser
        laser_global = np.matmul(pose_mat, laser_mat)
        # 지도를 범위내에 그리기 위해 x는 -3.0 y는 0에서 시작
        # 로봇의 위치로 시작을 하기 때문에 pose_x,pose_y의 경우 좌표를 변환할 필요가 없다.
        pose_x = (pose[0] - self.map_center[0] + (self.map_size[0]*self.map_resolution)/2) / self.map_resolution
        pose_y = (pose[1] - self.map_center[1] + (self.map_size[1]*self.map_resolution)/2) / self.map_resolution

        # 벽의 위치를 로봇 위치의 기준이 아닌 Map의 위치를 기준으로 좌표 변환을 진행해준다
        laser_global_x = (laser_global[0, :] - self.map_center[0] + (self.map_size[0]*self.map_resolution)/2) / self.map_resolution
        laser_global_y =  (laser_global[1, :] - self.map_center[1] + (self.map_size[1]*self.map_resolution)/2) / self.map_resolution

        ### Original Plot
        for i in range(laser_global.shape[1]):
            p1 = np.array([pose_x, pose_y]).reshape(-1).astype(np.int)
            p2 = np.array([laser_global_x[i], laser_global_y[i]]).astype(np.int)
            # print(p1)
            # print(p2)
            line_iter = createLineIterator(p1, p2, self.map)
        
            if (line_iter.shape[0] == 0):
                continue
        
            avail_x = line_iter[:, 0].astype(np.int)
            avail_y = line_iter[:, 1].astype(np.int)
        
            # Empty
            self.map[avail_y[:-1], avail_x[:-1]] = self.map[avail_y[:-1], avail_x[:-1]] + self.occu_down
        
            # Occupied
            self.map[avail_y[-1], avail_x[-1]] = self.map[avail_y[-1], avail_x[-1]] - self.occu_up

        self.show_pose_and_points(pose, laser_global)        

    def __del__(self):
        self.save_map(())

    def save_map(self):
        map_clone = self.map.copy()
        cv2.imwrite(self.map_filename, map_clone*255)

    def show_pose_and_points(self, pose, laser_global):
        tmp_map = self.map.astype(np.float32)
        map_bgr = cv2.cvtColor(tmp_map, cv2.COLOR_GRAY2BGR)

        pose_x = (pose[0] - self.map_center[0] + (self.map_size[0]*self.map_resolution)/2) / self.map_resolution
        pose_y = (pose[1] - self.map_center[1] + (self.map_size[1]*self.map_resolution)/2) / self.map_resolution

        laser_global_x = (laser_global[0, :] - self.map_center[0] + (self.map_size[0]*self.map_resolution)/2) / self.map_resolution
        laser_global_y =  (laser_global[1, :] - self.map_center[1] + (self.map_size[1]*self.map_resolution)/2) / self.map_resolution

        for i in range(laser_global.shape[1]):
            (l_x, l_y) = np.array([laser_global_x[i], laser_global_y[i]]).astype(np.int)
            center = (l_x, l_y)
            cv2.circle(map_bgr, center, 1, (0,255,0), -1)

        center = (pose_x.astype(np.int32)[0], pose_y.astype(np.int32)[0])
        
        cv2.circle(map_bgr, center, 2, (0,0,255), -1)

        map_bgr = cv2.resize(map_bgr, dsize=(0, 0), fx=self.map_vis_resize_scale, fy=self.map_vis_resize_scale)
        # cv2.imshow('Sample Map', map_bgr)
        # cv2.waitKey(1)



        
class Mapper(Node):

    def __init__(self):
        super().__init__('Mapper')
        
        # 로직 1 : publisher, subscriber, msg 생성
        self.subscription = self.create_subscription(LaserScan,'/scan',self.scan_callback,10)
        # self.subscription = self.create_subscription(LaserScan,'/scan',self.scan_callback,qos_profile=qos_profile_sensor_data)
        self.map_pub = self.create_publisher(OccupancyGrid, '/map', 1)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.imu_sub = self.create_subscription(Imu,'/imu', self.imu_callback, 10)


        self.map_msg=OccupancyGrid()
        self.map_msg.header.frame_id="map"
        self.map_size=int(params_map["MAP_SIZE"][0]\
            /params_map["MAP_RESOLUTION"]*params_map["MAP_SIZE"][1]/params_map["MAP_RESOLUTION"])
        
        m = MapMetaData()
        m.resolution = params_map["MAP_RESOLUTION"]
        m.width = int(params_map["MAP_SIZE"][0]/params_map["MAP_RESOLUTION"])
        m.height = int(params_map["MAP_SIZE"][1]/params_map["MAP_RESOLUTION"])
        quat = np.array([0, 0, 0, 1])
        m.origin = Pose()
        m.origin.position.x = params_map["MAP_CENTER"][0]-8.75
        m.origin.position.y = params_map["MAP_CENTER"][1]-8.75
        self.map_meta_data = m

        self.map_msg.info=self.map_meta_data

        # socket에서 받아온 맵 만들기 실행 여부 정보 받기
        # self.create_map_sub = self.create_subscription(MapScan, '/map_scan', self.map_scan_callback, 100)

        # is_map_create 변수가 True면 mapping 시작, std_msg에서 받아온 값으로 확인
        self.is_map_create = True
        # 로직 2 : mapping 클래스 생성
        self.mapping = Mapping(params_map)

        self.is_odom = False


    # def map_scan_callback(self, msg):
    #     # self.is_map_create = msg.map_scan
    #     print("runmapping의 데이터 값", msg)

    def imu_callback(self, msg):
        self.is_imu = True
        '''
        로직 3. IMU 에서 받은 quaternion을 euler angle로 변환해서 사용(라디안 단위)
        각도(도) = 라디안 * 180/π
        '''
        global robot_yaw
        imu_q= Quaternion(msg.orientation.w,msg.orientation.x,msg.orientation.y,msg.orientation.z)
        _,_,robot_yaw = imu_q.to_euler()
        # print(f"robot_yaw : {robot_yaw}")
    

    def odom_callback(self, msg): # 현재 좌표 x, y 와 회전각도 heading 갱신
        global robot_yaw   

        if self.is_imu:
        
            self.odom_pose_x = msg.pose.pose.position.x
            self.odom_pose_y = msg.pose.pose.position.y
            self.odom_heading = robot_yaw
            # self.odom_heading = msg.pose.pose.orientation.w

            self.is_odom = True
            


    def scan_callback(self, msg):
        # print("들어온다!!!000")
        # print(msg)
        # pose_x=msg.range_min
        # pose_y=msg.scan_time
        # heading=msg.time_increment

        if self.is_odom:
            # 현재 로봇의 x, y, theta 값
            pose_x = msg.range_min # ssafy_bridge/udp_to_laser pose_x 호출
            pose_y = msg.scan_time # ssafy_bridge/udp_to_laser pose_y 호출
            heading = msg.time_increment # ssafy_bridge/udp_to_laser heading 호출
            print("pose   ", pose_x, pose_y, heading)

            Distance = np.array(msg.ranges)
            # Distance[np.isinf(Distance)] = 0
            # print(Distance)
            x = Distance * np.cos(np.linspace(0, 2 * np.pi, 360))
            y = Distance * np.sin(np.linspace(0, 2 * np.pi, 360))
            laser = np.vstack((x.reshape((1, -1)), y.reshape((1, -1))))

            pose = np.array([[pose_x],[pose_y],[heading]])

            # 소켓에서 들어온 map_create 변수가 1일 경우에만 lidar 이용해 mapping시작         
            self.mapping.update(pose, laser)

            np_map_data=self.mapping.map.reshape(1,self.map_size) 
            list_map_data=np_map_data.tolist()
            for i in range(self.map_size):
                list_map_data[0][i]=100-int(list_map_data[0][i]*100)
                if list_map_data[0][i] >100 :
                    list_map_data[0][i]=100

                if list_map_data[0][i] <0 :
                    list_map_data[0][i]=0


            self.map_msg.header.stamp =rclpy.clock.Clock().now().to_msg()
            self.map_msg.data=list_map_data[0]
            self.map_pub.publish(self.map_msg)

def save_map(node):
    pkg_path = os.getcwd()
    folder_name = 'map'
    file_name = 'map.txt'
    full_path = os.path.join(pkg_path, folder_name, file_name)
    f=open(full_path,'w')
    data=''
    for pixel in node.map_msg.data :
        data+='{0} '.format(pixel)
    f.write(data) 
    f.close()

    # 맵을 저장한 이후 원래 변수 값을 초기화 시켜준다.
    

        
def main(args=None):    
    rclpy.init(args=args)
    
    try :    
        run_mapping = Mapper()
        rclpy.spin(run_mapping)
        run_mapping.destroy_node()
        rclpy.shutdown()

    except :
        print("save map")
        save_map(run_mapping)
 


if __name__ == '__main__':
    main()