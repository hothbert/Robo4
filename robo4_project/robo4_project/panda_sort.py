import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Range
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

#this should serve as our controller node

class PandaSort(Node):
    def __init__(self):
        super().__init__('panda_sort')

        self.create_subscription(Range, '/distance_msg', self.get_distance, 10)
        self.create_subscription(String, '/colour_msg', self.move_block, 10)

        self.publisher = self.create_publisher(JointTrajectory, '/panda/joint_trajectory_controller/command', 10)
        
    def move_block(self, msg):
        colour_value = msg.data
        if colour_value in ('blue', 'green', 'cyan'):
            self.get_logger().info(f"{colour_value} block detected!")
            
            movement = JointTrajectory()
            movement.joint_names = ['panda_joint1', 'panda_joint2']
            point = JointTrajectoryPoint()
            point.positions = [0.6, 0.6]
            movement.points.append(point)
            self.publisher.publish(movement)

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