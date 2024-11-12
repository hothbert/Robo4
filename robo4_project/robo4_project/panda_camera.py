import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

class PandaCamera(Node):
    def __init__(self):
        super().__init__('panda_camera')

        self.create_subscription(Image, 'Panda/camera/image_color', self._camera_callback, 1)

    def _camera_callback(self, msg):
        pass
        #we need an additional dependency to interpret images, OpenCV
    
def main():
    rclpy.init()
    node = PandaCamera()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()