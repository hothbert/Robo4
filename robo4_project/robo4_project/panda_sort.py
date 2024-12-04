import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Range
import time

#this should serve as our node for controlling moving things

class PandaSort(Node):
    def __init__(self):
        super().__init__('panda_sort')
        self.colour = None
        self.is_moving_block = False

        #subscribes to nodes publishing sensor messages
        self.create_subscription(Range, '/distance_msg', self.move_block, 10)
        self.create_subscription(String, '/colour_msg', self.get_colour, 10)
        #publishes actuator commands
        self.grip_publisher = self.create_publisher(String, '/gripper_command', 10)
        self.move_publisher = self.create_publisher(String, '/move_command', 10)

    def gripper(self, command):
        msg = String()
        msg.data = command
        self.grip_publisher.publish(msg)
        #self.get_logger().info("Gripper close command sent.")

    def move_joint(self, command):
        msg = String()
        msg.data = command
        self.move_publisher.publish(msg)
        
    def get_colour(self, msg):
        colour_value = msg.data
        if colour_value in ('blue', 'green', 'cyan'):
            self.colour = colour_value
            self.get_logger().info(f"{self.colour} block detected!")
        else:
            self.colour = None

    #we might want to change this to use a service rather than constantly doing time.sleep()
    #it would probably be better ros2 convention as well
    def move_block(self, msg):
        if self.is_moving_block:
            return #prevent further calls to this function until the block has been moved
        
        distance = msg.range
        #self.get_logger().info(f"detected distance: {distance}")

        if distance < 0.5:
            self.is_moving_block = True
            block_colour = self.colour

            self.gripper('open')
            self.move_joint('grab')
            time.sleep(0.5) #sleeping makes sure actions are done sequentially, and the block isnt thrown
            self.gripper('close')
            time.sleep(0.5)

            if block_colour is not None:
                if block_colour == 'blue':
                    self.move_joint('turn_blue')
                elif block_colour == 'cyan':
                    self.move_joint('turn_cyan')
                elif block_colour == 'green':
                    self.move_joint('turn_green')
            
            time.sleep(1.8)
            self.gripper('open')   #this drops the block, we might want a container for them to go into
            time.sleep(0.5)        #because currently they bounce, and it would look nicer too.
            self.gripper('close')
            self.move_joint('stand')
            time.sleep(0.5)
            self.move_joint('turn_back')
            time.sleep(1.0) #stops the function from continuing until robot is completely back in position
            self.is_moving_block = False #returned to position
        else:
            pass
            #self.get_logger().info("waiting for block...")

def main():
    rclpy.init()
    node = PandaSort()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()