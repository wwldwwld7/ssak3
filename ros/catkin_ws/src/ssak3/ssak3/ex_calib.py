import numpy as np
import cv2
import rclpy
import math

from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, LaserScan

params_lidar = {
    "Range" : 90,
    "CHANNEL" : int(1),
    "localIP": "127.0.0.1",
    "localPort": 9094,
    "Block_SIZE": int(1206),
    "X": 0,
    "Y": 0,
    "Z": 0.01,
    "YAW": 0,
    "PITCH": 0,
    "ROLL": 0
}

params_cam = {
    "WIDTH": 320, # image width
    "HEIGHT": 240, # image height
    "FOV": 90, # Field of view
    "localIP": "127.0.0.1",
    "localPort": 1232,
    "Block_SIZE": int(65000),
    "X": 0, # meter
    "Y": 0,
    "Z": 1,
    "YAW": 0, # deg
    "PITCH": 50,
    "ROLL": 0
}

def rotationMtx(yaw, pitch, roll):
    
    R_x = np.array([[1,         0,              0,                0],
                    [0,         math.cos(roll), -math.sin(roll) , 0],
                    [0,         math.sin(roll), math.cos(roll)  , 0],
                    [0,         0,              0,               1],
                    ])
                     
    R_y = np.array([[math.cos(pitch),    0,      math.sin(pitch) , 0],
                    [0,                  1,      0               , 0],
                    [-math.sin(pitch),   0,      math.cos(pitch) , 0],
                    [0,         0,              0,               1],
                    ])
    
    R_z = np.array([[math.cos(yaw),    -math.sin(yaw),    0,    0],
                    [math.sin(yaw),    math.cos(yaw),     0,    0],
                    [0,                0,                 1,    0],
                    [0,         0,              0,               1],
                    ])
                     
    R = np.matmul(R_x, np.matmul(R_y, R_z))
 
    return R

def translationMtx(x, y, z):
     
    M = np.array([[1,         0,              0,               x],
                  [0,         1,              0,               y],
                  [0,         0,              1,               z],
                  [0,         0,              0,               1],
                  ])
    
    return M

def transformMTX_lidar2cam(params_lidar, params_cam):

    lidar_yaw, lidar_pitch, lidar_roll = params_lidar.get("YAW"), params_lidar.get("PITCH"), params_lidar.get("ROLL")
    cam_yaw, cam_pitch, cam_roll = params_cam.get("YAW"), params_cam.get("PITCH"), params_cam.get("ROLL")

    lidar_pos = {"X": params_lidar.get("X"), "Y": params_lidar.get("Y"), "Z": params_lidar.get("Z")}
    cam_pos = {"X": params_cam.get("X"), "Y": params_cam.get("Y"), "Z": params_cam.get("Z")}

    Tmtx = translationMtx(-(cam_pos.get("X") - lidar_pos.get("X")), -(cam_pos.get("Y") - lidar_pos.get("Y")), -(cam_pos.get("Z") - lidar_pos.get("Z")))

    Rmtx = rotationMtx(math.pi/2, 0, math.pi/2)

    RT = np.matmul(Rmtx, Tmtx)

    return RT

def project2img_mtx(params_cam):

    tan_fov = math.tan(math.radians(params_cam['FOV'] / 2))
    fc_x = params_cam.get('HEIGHT') / (2 * tan_fov)
    fc_y = params_cam.get('HEIGHT') / (2 * tan_fov)

    cx = params_cam.get('WIDTH') / 2
    cy = params_cam.get('HEIGHT') / 2

    R_f = np.array([[fc_x, 0, cx],
                    [0, fc_y, cy]])

    return R_f



# # 라이다 포인트의 좌표를 라이다 좌표계에서 카메라 좌표계로 변환하기 위한...
# def transformMTX_lidar2cam(params_lidar, params_cam):

#     lidar_yaw, lidar_pitch, lidar_roll = [np.deg2rad(params_lidar.get(i)) for i in (["YAW","PITCH","ROLL"])]
#     cam_yaw, cam_pitch, cam_roll = [np.deg2rad(params_cam.get(i)) for i in (["YAW","PITCH","ROLL"])]
    
#     lidar_pos = [params_lidar.get(i) for i in (["X","Y","Z"])]
#     cam_pos = [params_cam.get(i) for i in (["X","Y","Z"])]

#     x_rel = cam_pos[0] - lidar_pos[0]
#     y_rel = cam_pos[1] - lidar_pos[1]
#     z_rel = cam_pos[2] - lidar_pos[2]

#     R_T = np.matmul(rotationMtx(lidar_yaw, lidar_pitch, lidar_roll).T, translationMtx(-x_rel, -y_rel, -z_rel).T)
#     R_T = np.matmul(R_T, rotationMtx(cam_yaw, cam_pitch, cam_roll))
#     R_T = np.matmul(R_T, rotationMtx(np.deg2rad(-90.), 0., 0.))
#     R_T = np.matmul(R_T, rotationMtx(0, 0., np.deg2rad(-90.)))

#     R_T = R_T.T 

#     return R_T


def make_distance_img(xi, yi, distance, img_w, img_h, dis_max, clr_map):

    point_np = np.zeros((img_h,img_w,1), dtype=np.uint8)
    point_binary = np.zeros((img_h,img_w,3), dtype=np.uint8)

    point_np[yi.astype(np.int), xi.astype(np.int), :] = (np.clip(distance,0,dis_max).reshape([-1,1,1])/(dis_max)*255).astype(np.uint8)
    point_binary[yi.astype(np.int), xi.astype(np.int), :] = 1

    point_np = cv2.applyColorMap(point_np, clr_map)

    point_np = cv2.dilate(point_np*point_binary, cv2.getStructuringElement(cv2.MORPH_CROSS,(5, 5)))

    return point_np

def make_intensity_img(xi, yi, intens, img_w, img_h):
    
    point_np = np.zeros((img_h, img_w, 3), dtype=np.uint8)

    #Object
    point_np[yi[intens>=250].astype(np.int),xi[intens>=250].astype(np.int),2] = 255
    
    return point_np




class LIDAR2CAMTransform:
    def __init__(self, params_cam, params_lidar):

        self.width = params_cam["WIDTH"]
        self.height = params_cam["HEIGHT"]

        self.n = float(params_cam["WIDTH"])
        self.m = float(params_cam["HEIGHT"])

        self.RT = transformMTX_lidar2cam(params_lidar, params_cam)

        self.proj_mtx = project2img_mtx(params_cam)

    def transform_lidar2cam(self, xyz_p):
        
        xyz_c = np.array([])

        for idx in range(len(xyz_p)):
            xyz1 = np.append(xyz_p[idx], 1)

            array = np.matmul(self.RT, xyz1)
            xyz_c = np.append(xyz_c, [[x] for x in array] )

        xyz_c = np.reshape(xyz_c, (-1, 4))

        return xyz_c

    # def transform_lidar2cam(self, xyz_p):
        
    #     xyz_c = np.matmul(np.concatenate([xyz_p, np.ones((xyz_p.shape[0], 1))], axis=1), self.RT.T)

    #     return xyz_c
    def project_pts2img(self, xyz_c, crop=True):

        #xyi=np.zeros((xyz_c.shape[0], 2))
        xyi = np.array([])

        """
        로직 3. RT로 좌표 변환된 포인트들의 normalizing plane 상의 위치를 계산.
        """
        for xyz1 in xyz_c:
            xn, yn = xyz1[0] / xyz1[2], xyz1[1] / xyz1[2]
            #print("xn , yn : ", xn, yn)
            #xn, yn = xyz_c[0] / xyz_c[2], xyz_c[1] / xyz_c[2]

            # 로직 4. normalizing plane 상의 라이다 포인트들에 proj_mtx를 곱해 픽셀 좌표값 계산.
            xy= np.matmul(self.proj_mtx, np.array([xn, yn, np.ones_like(xn)]))
            #print(xy)
            xyi = np.append(xyi, [[x] for x in xy])

        xyi = np.reshape(xyi, (-1, 2))
        
        #print(xyi)
        """
        로직 5. 이미지 프레임 밖을 벗어나는 포인트들을 crop.
        """
        if crop:
            xyi = self.crop_pts(xyi)
        else:
            pass
        return xyi




    # def project_pts2img(self, xyz_c, crop=True):

    #     xyz_c = xyz_c.T

    #     xc, yc, zc = xyz_c[0,:].reshape([1,-1]), xyz_c[1,:].reshape([1,-1]), xyz_c[2,:].reshape([1,-1])

    #     xn, yn = xc/(zc+0.0001), yc/(zc+0.0001)

    #     xyi = np.matmul(self.proj_mtx, np.concatenate([xn, yn, np.ones_like(xn)], axis=0))

    #     xyi = xyi[0:2,:].T

    #     if crop:
    #         xyi = self.crop_pts(xyi)
    #     else:
    #         pass
        
    #     return xyi

    def crop_pts(self, xyi):

        xyi = xyi[np.logical_and(xyi[:, 0]>=0, xyi[:, 0]<self.width), :]
        xyi = xyi[np.logical_and(xyi[:, 1]>=0, xyi[:, 1]<self.height), :]

        return xyi

    
def draw_pts_img(img, xi, yi):
    
    point_np = img

    #Left Lane
    for ctr in zip(xi, yi):
        point_np = cv2.circle(point_np, ctr, 2, (255,0,0),-1)

    return point_np


# class SensorCalib(Node):

#     def __init__(self):
#         super().__init__(node_name='ex_calib')

#         self.subs_scan = self.create_subscription(
#             LaserScan,
#             '/scan',
#             self.scan_callback, 10)

#         self.subs_img = self.create_subscription(
#             CompressedImage,
#             '/image_jpeg/compressed',
#             self.img_callback,
#             10)

#         self.l2c_trans = LIDAR2CAMTransform(params_cam, params_lidar)

#         self.timer_period = 0.1

#         self.timer = self.create_timer(self.timer_period, self.timer_callback)

#         self.xyz, self.R, self.intens = None, None, None
#         self.img = None

#     def img_callback(self, msg):

#         np_arr = np.frombuffer(msg.data, np.uint8)

#         self.img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#     def scan_callback(self, msg):

#         self.R = np.array(msg.ranges)
#         self.intens = np.array(msg.intensities)

#         x = self.R*np.cos(np.linspace(0, 2*np.pi, 360))
#         y = self.R*np.sin(np.linspace(0, 2*np.pi, 360))
#         z = np.zeros_like(x)

#         self.xyz = np.concatenate([
#             x.reshape([-1, 1]),
#             y.reshape([-1, 1]),
#             z.reshape([-1, 1])
#         ], axis=1)

#     def timer_callback(self):

#         if self.xyz is not None and self.img is not None :
            
#             xyz_p = self.xyz[np.where(self.xyz[:, 0]>=0)]


#             intens_p = self.intens.reshape([-1,1])
#             intens_p = intens_p[np.where(self.xyz[:, 0]>=0)]

#             xyz_c = self.l2c_trans.transform_lidar2cam(xyz_p)

#             xy_i = self.l2c_trans.project_pts2img(xyz_c, crop=True)

#             img_l2c = draw_pts_img(self.img, xy_i[:, 0].astype(np.int32),
#                                             xy_i[:, 1].astype(np.int32))
                                                
#             cv2.imshow("Lidar2Cam", img_l2c)
#             cv2.waitKey(1)

#         else:
#             pass

class SensorCalib(Node):

    def __init__(self):
        super().__init__(node_name='ex_calib')

        # 로직 1. 노드에 필요한 라이다와 카메라 topic의 subscriber 생성

        self.subs_scan = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback, 10)

        self.subs_img = self.create_subscription(
            CompressedImage,
            '/image_jpeg/compressed',
            self.img_callback,
            10)

        # 로직 2. Params를 받아서 라이다 포인트를 카메라 이미지에 projection 하는
        # transformation class 정의하기

        self.l2c_trans = LIDAR2CAMTransform(params_cam, params_lidar)

        self.timer_period = 0.1

        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        self.xyz, self.R, self.intens = None, None, None
        self.img = None

    def img_callback(self, msg):
        """
        로직 3. 카메라 콜백함수에서 이미지를 클래스 내 변수로 저장.
        """
        np_arr = np.frombuffer(msg.data, dtype=np.uint8)

        self.img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    def scan_callback(self, msg):
        """
        로직 4. 라이다 2d scan data(거리와 각도)를 가지고 x,y 좌표계로 변환
        """
        self.R = msg.ranges

        x = np.array([self.R[theta] * math.cos(math.radians(theta))  for theta in range(360)])
        #print("x : ", x)
        y = np.array([self.R[theta] * math.sin(math.radians(theta))  for theta in range(360)])
        #print("y : ", y)
        z = np.array([0.4] * 360)

        self.xyz = np.concatenate([
            x.reshape([-1, 1]),
            y.reshape([-1, 1]),
            z.reshape([-1, 1])
        ], axis=1)
        #print("------ xyz ------")
        #print(self.xyz)
        

    def timer_callback(self):

        if self.xyz is not None and self.img is not None :

            """
            로직 5. 라이다 x,y 좌표 데이터 중 정면 부분만 crop
            """
            # xyz_p = self.l2c_trans.crop_pts(self.xyz)
            a = self.xyz[:90]
            b = self.xyz[270:]

            xyz_p = np.concatenate([a, b])  
            # print("xyz_p : ", xyz_p)

            """
            로직 6. transformation class 의 transform_lidar2cam 로 카메라 3d 좌표 변환
            """
            xyz_c = self.l2c_trans.transform_lidar2cam(xyz_p)
            # print("xyz_c : ", xyz_c)
            """
            로직 7. transformation class 의 project_pts2img로 카메라 프레임으로 정사영
            """
            xy_i = self.l2c_trans.project_pts2img(xyz_c)
            # print("xy_i : ", xy_i)
            """
            로직 8. draw_pts_img()로 카메라 이미지에 라이다 포인트를 draw 하고 show
            """
            x_i = [int(xy[0]) for xy in xy_i]
            # print("x_i : ", x_i)
            y_i = [int(xy[1]) for xy in xy_i]
            # print("y_i : ", y_i)

            # print("len(xyz) : ", len(self.xyz))
            # print("len(xyz_p) : ", len(xyz_p))
            # print("len(xyz_c) : ", len(xyz_c))
            # print("len(xy_i) : ", len(xy_i))

            img_l2c = draw_pts_img(self.img, x_i, y_i)

            cv2.imshow("Lidar2Cam", img_l2c)
            cv2.waitKey(1)

        else:

            print("waiting for msg")
            pass



def main(args=None):

    rclpy.init(args=args)

    calibrator = SensorCalib()

    rclpy.spin(calibrator)


if __name__ == '__main__':

    main()