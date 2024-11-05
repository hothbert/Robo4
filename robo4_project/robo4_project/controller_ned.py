#controller for robot ned to communicate with webots API

from webots_ros.srv import SetFloat, SetString
import rclpy
from rclpy.node import Node

class NedControl(Node):
    def __init__(self):
        super().__init__('controller_ned')
        #publishers etc...

    def control(self):
        while rclpy.ok():
            #sensor data and commands
            self.get_logger().info('ned doing something')

def main():
    rclpy.init()
    node = NedControl()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()