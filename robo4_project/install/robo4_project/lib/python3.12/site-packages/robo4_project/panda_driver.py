import rclpy

class PandaRobotDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

def main():
    rclpy.init()
    driver = PandaRobotDriver()
    rclpy.spin(driver)
    driver.destroy_node()
    rclpy.shutdown()

    # WORLDS FILE
    #  endEffectorSlot [
    #DistanceSensor {
    #}
    #DEF GRIPPER PandaHand {
    #}
  #]