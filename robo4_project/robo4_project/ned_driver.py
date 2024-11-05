import rclpy

class NedRobotDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot