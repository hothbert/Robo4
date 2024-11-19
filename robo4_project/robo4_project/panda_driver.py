import rclpy
from webots_ros2_driver.webots_controller import WebotsController

class PandaRobotDriver(WebotsController):
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot
        #define the gripper joints and all other relevant ones
        #panda_finger_joint1  etc...

        #subscribe to commands coming from panda sort

    #define functions that act on these commands and execute movement
    # good luck    

    def step(self):
        pass
    #control logic/sensor updates here

def main():
    rclpy.init()
    driver = PandaRobotDriver()
    rclpy.spin(driver)
    driver.destroy_node()
    rclpy.shutdown()

