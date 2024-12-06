import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
from std_msgs.msg import String

class PandaCamera(Node):
    def __init__(self):
        super().__init__('panda_camera')
        self.bridge = CvBridge()
        self.create_subscription(Image, 'Panda/camera/image_color', self.camera_callback, 10) # subscribes to the webots sensor
        self.detected_colour_msg = None

        timer_period = 0.25
        self.publisher = self.create_publisher(String, '/colour_msg', 10) # publishes the detected colour
        self.create_timer(timer_period, self.publish_colour)
        

    def camera_callback(self, msg):
        #converts the information recieved from the sensor to array of bgr values
        #uses OpenCV dependency to translate ros2 stuff because it doesnt direcctly give colour
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.detect_colours(frame)

    def detect_colours(self, frame):
        colours = {  # has to be in BGR order
            (255, 0, 0): 'blue', #these are all the possible colours of our boxes
            (0, 255, 0): 'green',
            (255, 255, 0): 'cyan'
        }

        self.detected_colour_msg = "No specific colors detected"
        for f in frame: #frame is a 3d array and pixel is numpy array
            for pixel in f:
                pixel = tuple(pixel)
                if pixel in colours:
                    self.detected_colour_msg = colours[pixel]
        
    def publish_colour(self):
        if self.detected_colour_msg is not None:
            message = String()
            message.data = self.detected_colour_msg
            self.publisher.publish(message)

def main():
    rclpy.init()
    camera_node = PandaCamera()
    rclpy.spin(camera_node)
    camera_node.destroy_node()
    rclpy.shutdown()
