import rclpy
from rclpy.node import Node
from webots_ros2_driver.webots_controller import WebotsController
from std_msgs.msg import String

#this serves as an interface between ros2 nodes and the webots robot
#its soul purpose is to send positions to each joint
#it subscribes to robot movement commands and acts upon them
#lets not put any logic here, save that for the actual ros2 nodes

class PandaRobotDriver(WebotsController):
    def init(self, webots_node, properties):
        #creates a node so that rclpy features can be used, since PandaRobotDriver doesnt inherit from Node
        rclpy.init()
        self.node = Node('panda_driver')
        self.__robot=webots_node.robot 

        self.gripper_left = self.__robot.getDevice('panda_finger::left')
        self.gripper_right = self.__robot.getDevice('panda_finger::right')
        self.bend_down = self.__robot.getDevice('panda_joint1')

        self.node.create_subscription(String, '/gripper_command', self.gripper_command_callback, 10)

    #define functions that act on these commands and execute movement
    # good luck 
    def gripper_command_callback(self, msg):
        command = msg.data
        if command == "open":
            self.gripper_left.setPosition(0.04)  
            self.gripper_right.setPosition(0.04)
            self.node.get_logger().info("Gripper opened.")
            
        #elif command == "close":
            #self.gripper_left.setPosition(0.0)  
            #self.gripper_right.setPosition(0.0)
            #self.get_logger().info("Gripper closed.")


    def step(self):
        rclpy.spin_once(self.node, timeout_sec=0) #starts self.ynode so that subscription works
