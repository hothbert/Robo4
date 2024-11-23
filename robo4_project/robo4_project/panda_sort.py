import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Range
#from robo4_project.msg import JointMove


#this should serve as our node for controlling moving things
#todo: bend down, close gripper, stand up, turn to direction, open gripper to release block

class PandaSort(Node):
    def __init__(self):
        super().__init__('panda_sort')
        #subscribes to the nodes collecting sensor data.
        self.colour = None
        self.create_subscription(Range, '/distance_msg', self.move_block, 10)
        self.create_subscription(String, '/colour_msg', self.get_colour, 10)

        #for other joints, we could create custom message to specify joint and how much it moves by
        self.publisher = self.create_publisher(String, '/gripper_command', 10)
        #self.joint_publisher = self.create_publisher(JointMove, '/joint_move', 10)   

    def open_gripper(self):
        msg = String()
        msg.data = 'open'
        self.publisher.publish(msg)
        self.get_logger().info("Gripper open command sent.")
        
    def get_colour(self, msg):
        colour_value = msg.data
        if colour_value in ('blue', 'green', 'cyan'):
            self.colour = colour_value
            self.get_logger().info(f"{self.colour} block detected!")
        else:
            self.colour = None

    def move_block(self, msg):
        #we may need to pause between movements so that the robot doesnt try and do all movements at once
        #or work out how the rclpy spin stuff works so that it does this once per detected block
        #might need to realign sensors or slow stuff down to make stuff more precise
        distance = msg.range
        self.get_logger().info(f"detected distance: {distance}")
        if distance < 0.5:
            self.open_gripper()
            block_colour = self.colour
            #bend down by [distance] meters
            #close gripper
            #stand up
            if block_colour is not None:
                if block_colour == 'blue':
                    self.get_logger().info("Moving block to the left.")
                    #move left
                    #open gripper
                    #move back
                elif block_colour == 'cyan':
                    self.get_logger().info("Moving block to the right.")
                    #same as above
                elif block_colour == 'green':
                    self.get_logger().info("Moving block forward.")
            #close gripper        
        else:
            self.get_logger().info("waiting for block...")

def main():
    rclpy.init()
    node = PandaSort()
    node.open_gripper() 
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()