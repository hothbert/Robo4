import rclpy

class NedRobotDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

def main():
    rclpy.init()
    driver = NedRobotDriver()
    rclpy.spin(driver)
    driver.destroy_node()
    rclpy.shutdown()