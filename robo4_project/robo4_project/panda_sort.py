import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Range

#this should serve as our node for moving things idk

class PandaSort(Node):
    def __init__(self):
        super().__init__('panda_sort')
        #subscribes to the nodes collecting sensor data.
        self.create_subscription(Range, '/distance_msg', self.get_distance, 10)
        self.create_subscription(String, '/colour_msg', self.move_block, 10)
        
        #publish commands or something here
        
    def move_block(self, msg):
        #i think idealy, we stop the conveyer belt from moving to make it easier to pick up
        #might need to re-align the sensors to make this easier and more precise
        colour_value = msg.data
        if colour_value in ('blue', 'green', 'cyan'):
            self.get_logger().info(f"{colour_value} block detected!")
            #send open gripper command
            #bend down and pick up block
            #close gripper
            #if its blue turn to left and drop that shit on the floor
            #right for cyan
            #a third direction for green
        else:
            self.get_logger().info("waiting for block...")

    def get_distance(self, msg):
        distance = msg.range
        self.get_logger().info(f"detected distance: {distance}")

def main():
    rclpy.init()
    node = PandaSort()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()