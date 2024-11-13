import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class PandaCamera(Node):
    def __init__(self):
        super().__init__('panda_camera')
        self.create_subscription(Image, 'Panda/camera/image_color', self._camera_callback, 1)
        self.bridge = CvBridge()

    def _camera_callback(self, msg):
        #converts the information recieved from the sensor to array of bgr values
        #uses OpenCV dependency to translate ros2 stuff because it doesnt direcctly give colour
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self._detect_colours(frame)

    def _detect_colours(self, frame):
        colours = {
            (255, 0, 0): 'blue', #these are all the possible colours of our boxes
            (0, 255, 0): 'green',
            (0, 0, 255): 'red'
        }

        detected = "No specific colors detected"
        for f in frame: #frame is a 3d array and pixel is numpy array
            for pixel in f:
                pixel = tuple(pixel)
                if pixel in colours:
                    detected = colours[pixel]

        #self.get_logger().info(f"detected: {detected}")

def main():
    rclpy.init()
    camera_node = PandaCamera()
    rclpy.spin(camera_node)
    camera_node.destroy_node()
    rclpy.shutdown()
