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
        #converts the information recieved from the sensor to rgb values
        #uses OpenCV dependency to translate ros2 stuff because it doesnt direcctly give colour
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self._detect_colours(frame)

    def _detect_colours(self, frame):
        # Convert to HSV color space
        #hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define color ranges
        colours = {
            'red': [255, 0, 0],
            'green': [0, 255, 0],
            'blue': [0, 0, 255]
        }

        detected_colours = []
        for colour in colours:
            #mask = cv2.inRange(hsv_frame, np.array(lower_bound), np.array(upper_bound))
            #if cv2.countNonZero(mask) > 0:
                #detected_colors.append(color_name)
            if colour in frame:
                detected_colours.append(colour)
        
        if detected_colours:
            self.get_logger().info(f"Detected colors: {', '.join(detected_colors)}")
        else:
            self.get_logger().info("No specific colors detected")

def main():
    rclpy.init()
    camera_node = PandaCamera()
    rclpy.spin(camera_node)
    camera_node.destroy_node()
    rclpy.shutdown()
