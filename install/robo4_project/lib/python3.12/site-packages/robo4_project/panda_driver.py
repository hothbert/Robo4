import rclpy
from webots_ros2_driver.webots_controller import WebotsController

class PandaRobotDriver(WebotsController):
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

    def step(self):
        pass
    #control logic/sensor updates here

def main():
    rclpy.init()
    driver = PandaRobotDriver()
    rclpy.spin(driver)
    driver.destroy_node()
    rclpy.shutdown()

