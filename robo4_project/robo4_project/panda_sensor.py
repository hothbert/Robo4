import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range

class PandaSensor(Node):
    def __init__(self):
        super().__init__('panda_sensor')

        self.create_subscription(Range, 'Panda/panda_distance_sensor', self._distance_sensor_callback, 10)

    def _distance_sensor_callback(self, msg):
        distance = msg.range
        #self.get_logger().info(f"Distance: {distance}")
    
def main():
    rclpy.init()
    node = PandaSensor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
