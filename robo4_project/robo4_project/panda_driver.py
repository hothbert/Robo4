import rclpy
from rclpy.node import Node
from webots_ros2_driver.webots_controller import WebotsController
from std_msgs.msg import String

class PandaRobotDriver(WebotsController):
    def init(self, webots_node, properties):
        super().init(webots_node.properties)
        self.__robot=webots_node.robot

        self.gripper_left = self.__robot.getDevice('panda_finger_joint1')  # Adjust with actual motor name
        self.gripper_right = self.__robot.getDevice('panda_finger_joint2')  # Adjust with actual motor name

        self.gripper_cmd_sub = self.create_subscription(
            String,  # Replace with your chosen message type
            '/gripper_command',  # Topic name
            self.gripper_command_callback,
            10
        )

        #define the gripper joints and all other relevant ones
        #panda_finger_joint1  etc...

        #subscribe to commands coming from panda sort

    #define functions that act on these commands and execute movement
    # good luck 
    def gripper_command_callback(self, msg):
        command = msg.data
        if command == "open":
            self.gripper_left.setPosition(0.04)  
            self.gripper_right.setPosition(0.04)
            self.get_logger().info("Gripper opened.")
        #elif command == "close":
            #self.gripper_left.setPosition(0.0)  
            #self.gripper_right.setPosition(0.0)
            #self.get_logger().info("Gripper closed.")
        else:
            self.get_logger().warn(f"Unknown gripper command: {command}")   

    def step(self):
        pass
    #control logic/sensor updates here

def main():
    rclpy.init()
    driver = PandaRobotDriver()
    rclpy.spin(driver)
    driver.destroy_node()
    rclpy.shutdown()

