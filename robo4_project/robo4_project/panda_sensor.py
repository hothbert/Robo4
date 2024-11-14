import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range

class PandaSensor(Node):
    def __init__(self):
        super().__init__('panda_sensor')

        self.create_subscription(Range, 'Panda/panda_distance_sensor', self._distance_sensor_callback, 10)
        self.detected_range_msg = None

        timer_period = 0.05
        self.publisher = self.create_publisher(Range, '/distance_msg', 10)
        self.create_timer(timer_period, self.publish_range)

    def _distance_sensor_callback(self, msg):
        self.detected_range_msg = msg.range
        #self.get_logger().info(f"Distance: {distance}")

    def publish_range(self):
        if self.detected_range_msg is not None:
            message = Range()
            message.range = self.detected_range_msg
            self.publisher.publish(message)

    
def main():
    rclpy.init()
    node = PandaSensor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
