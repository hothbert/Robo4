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
        self.joint_4 = self.__robot.getDevice('panda_joint4')
        self.joint_6 = self.__robot.getDevice('panda_joint6')
        self.joint_2 = self.__robot.getDevice('panda_joint2')
        self.joint_1 = self.__robot.getDevice('panda_joint1')

        self.node.create_subscription(String, '/gripper_command', self.gripper_command_callback, 10)
        self.node.create_subscription(String, '/move_command', self.grab_callback, 10)

    def gripper_command_callback(self, msg):
        command = msg.data
        if command == "open":
            self.gripper_left.setPosition(0.04)  
            self.gripper_right.setPosition(0.04)
            self.node.get_logger().info("Gripper opened.")           
        elif command == "close":
            self.gripper_left.setPosition(0.0)  
            self.gripper_right.setPosition(0.0)
            self.node.get_logger().info("Gripper closed.")

    #needs tidying up
    def grab_callback(self, msg):
        command = msg.data
        if command =="grab": #don't touch unless robot isnt picking up properly!
            self.joint_4.setPosition(-2.5)
            self.joint_6.setPosition(2.85)
            self.joint_2.setPosition(0.3)
        elif command =="stand":
            self.joint_4.setPosition(-1.77)
            self.joint_6.setPosition(1.6)
        elif command == "turn_blue":        # might want to play with these to get it to drop the block
            self.joint_1.setPosition(-2.0)  # gently, without coliding with other blocks on the conveyer belt
            self.joint_2.setPosition(0)
        elif command == "turn_green":
            self.joint_1.setPosition(2.0)
            self.joint_2.setPosition(0)
        elif command == "turn_cyan":
            self.joint_1.setPosition(2.95)
            self.joint_2.setPosition(0)
        elif command == "turn_back":
            self.joint_1.setPosition(0)
            


    def step(self):
        rclpy.spin_once(self.node, timeout_sec=0) #starts self.node so that subscription works
