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

    def _camera_callback(self, msg):
        pass
        #we need an additional dependency to interpret images, OpenC
        
        # Initialize CvBridge
        self.bridge = CvBridge()
        
        # Subscribe to the updated camera topic
        self.create_subscription(Image, 'Panda/panda_camera/image_color', self._camera_callback, 10)

    def _camera_callback(self, msg):
        self.get_logger().info("Received an image")  # Debug log to check if image is received
        
        # Convert the ROS Image message to an OpenCV image
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            self._detect_colors(frame)
        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def _detect_colors(self, frame):
        # Convert to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define color ranges
        colors = {
            'red': ((0, 120, 70), (10, 255, 255)),
            'green': ((36, 25, 25), (86, 255, 255)),
            'blue': ((94, 80, 2), (126, 255, 255))
        }

        detected_colors = []
        for color_name, (lower_bound, upper_bound) in colors.items():
            mask = cv2.inRange(hsv_frame, np.array(lower_bound), np.array(upper_bound))
            if cv2.countNonZero(mask) > 0:
                detected_colors.append(color_name)
        
        if detected_colors:
            self.get_logger().info(f"Detected colors: {', '.join(detected_colors)}")
        else:
            self.get_logger().info("No specific colors detected")

def main():
    rclpy.init()
    camera_node = PandaCamera()
    rclpy.spin(camera_node)
    camera_node.destroy_node()
    rclpy.shutdown()
