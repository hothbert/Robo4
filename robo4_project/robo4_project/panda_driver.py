import rclpy
from rclpy.node import Node
from webots_ros2_driver.webots_controller import WebotsController
from std_msgs.msg import String

class PandaRobotDriver(WebotsController, Node):
    def init(self, webots_node, properties):
        rclpy.init()
        self.node = Node('panda_driver') #creates a node to access ros2 functions
        self.__robot=webots_node.robot 
        

        self.gripper_left = self.__robot.getDevice('panda_finger::left')
        self.gripper_right = self.__robot.getDevice('panda_finger::right')
        self.bend_down = self.__robot.getDevice('panda_joint1')

        self.gripper_cmd_sub = self.node.create_subscription(String, '/gripper_command', self.gripper_command_callback, 10)

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
        else:
            self.node.get_logger().warn(f"Unknown gripper command: {command}")   

    def step(self):
        rclpy.spin_once(self.node, timeout_sec=0)


def main():
    rclpy.init()
    driver = PandaRobotDriver()
    rclpy.spin(driver)
    driver.destroy_node()
    rclpy.shutdown()

