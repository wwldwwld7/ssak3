import rclpy
import numpy as np
from rclpy.node import Node

import os
from geometry_msgs.msg import Pose
from squaternion import Quaternion
from nav_msgs.msg import Odometry,OccupancyGrid,MapMetaData
from math import pi

# load_map 노드는 맵 데이터를 읽어서, 맵 상에서 점유영역(장애물) 근처에 로봇이 움직일 수 없는 영역을 설정하고 맵 데이터로 publish 해주는 노드입니다.
# 추 후 a_star 알고리즘에서 맵 데이터를 subscribe 해서 사용합니다.

# map.txt는 SMARTHOME1의 occupancy grid map 입니다.
# 그 값에 따라서 FREE SPACE 인지 OCCUPIED 영역인지를 나타냅니다.
# 숫자의 범위는 0~100까지인데 값이 높을수록 장애물이 있을 확률이 높다

# 노드 로직 순서
# 1. 맵 파라미터 설정
# 2. 맵 데이터 읽고, 2차원 행렬로 변환
# 3. 점유영역 근처 필터처리

class loadMap(Node):

    def __init__(self):
        super().__init__('load_map')
        self.map_pub = self.create_publisher(OccupancyGrid, 'map', 1)
        
        time_period=1  
        self.timer = self.create_timer(time_period, self.timer_callback)
       
        # 로직 1. 맵 파라미터 설정
        # 제공한 맵 데이터의 파라미터입니다. size_x,y는 x,y 방향으로 grid의 개수이고, resolution은 grid 하나당 0.05m라는 것을 의미합니다.
        # offset_x,y 의 -8, -4 는 맵 데이터가 기준 좌표계(map)로 부터 떨어진 거리를 의미합니다. 
        # 각 항에 -8.75를 뺀이유는 ros에서 occupancygrid의 offset이라는 데이터는 맵의 중앙에서 기준좌표계까지 거리가 아니라 맵의 우측하단에서 부터 기준좌표계까지의 거리를 의미합니다.
        # 따라서 (350*0.05)/2를 해준 값을 빼줍니다.

        # 참고로 350*0.05 는 17.5다.
        # 0.05m 즉 5cm
        # 정사각형 맵이라고 생각한다.
        self.map_msg=OccupancyGrid()
        self.map_size_x=350 
        self.map_size_y=350
        self.map_resolution=0.05
        self.map_offset_x=-8-8.75-3.58
        self.map_offset_y=-4-8.75
        self.map_data = [0 for i in range(self.map_size_x*self.map_size_y)]
        
        # 2차원 행렬로 만드는 과정인 것 같다.
        # [[],
        #  [],
        #  []]
        grid=np.array(self.map_data)
        grid=np.reshape(grid,(350, 350))

        self.map_msg.header.frame_id="map"

        # 맵에 대한 정보를 넣는 과정같다.
        m = MapMetaData()
        m.resolution = self.map_resolution
        m.width = self.map_size_x
        m.height = self.map_size_y
        m.origin = Pose()
        m.origin.position.x = self.map_offset_x
        m.origin.position.y = self.map_offset_y

        self.map_meta_data = m
        self.map_msg.info=self.map_meta_data

        '''
        로직 2. 맵 데이터 읽고, 2차원 행렬로 변환
        '''
        pkg_path = os.getcwd()
        folder_name = 'map'
        file_name = 'map.txt'
        full_path = os.path.join(pkg_path, folder_name, file_name)

        self.f = open(full_path, 'r')

        line = self.f.readline()
        line_data = line.split()

        for num, data in enumerate(line_data):
            self.map_data[num] = int(data)

        # 350 X 350 행렬로 만들기
        map_to_grid = np.array(self.map_data)
        grid = np.reshape(map_to_grid, (350, 350))
        

        # 로직 3. 점유영역 근처 필터처리
        for x in range(350):
            for y in range(350):
                # grid 영역이 100이면 장애물이 있다.
                if grid[x][y] == 100:
                    # 장애물에서 좀 더 떨어진 공간은 회색으로
                    for box_x in range(-5, 6):
                        for box_y in range(-5, 6):
                            if 0 < x+box_x < 350 and 0 < y+box_y < 350 and grid[x+box_x][y+box_y] < 80:
                                grid[x+box_x][y+box_y] = 70
                    # 장애물에 아주 가까운 공간은 초록색으로 
                    for box_x in range(-2, 3):
                        for box_y in range(-2, 3):
                            if 0 < x+box_x < 350 and 0 < y+box_y < 350 and grid[x+box_x][y+box_y] < 80:
                                grid[x+box_x][y+box_y] = 127

        
        # 350X350 행렬을 array([[, , , ,]]) 형태로 만들어준다.
        np_map_data=grid.reshape(1,350*350)
        # [[, , , , ,]] 형태로 만들어준다.
        list_map_data=np_map_data.tolist()

        self.f.close()
        # [[, , , , ,]] 형태에서 [] 벗겨내기
        self.map_msg.data=list_map_data[0]


    def timer_callback(self):
        self.map_msg.header.stamp =rclpy.clock.Clock().now().to_msg()
        self.map_pub.publish(self.map_msg)

       
def main(args=None):
    rclpy.init(args=args)
    load_map = loadMap()
    rclpy.spin(load_map)
    load_map.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()