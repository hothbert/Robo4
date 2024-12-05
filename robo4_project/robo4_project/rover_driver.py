import rclpy
from rclpy.node import Node
from webots_ros2_driver.webots_controller import WebotsController
from geometry_msgs.msg import Twist

half_dist_wheels = 0.045
wheel_r = 0.025

class RoverDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        self.left_motor = self.__robot.getDevice('left wheel motor')
        self.right_motor = self.__robot.getDevice('right wheel motor')

        self.left_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0)

        self.right_motor.setPosition(float('inf'))
        self.right_motor.setVelocity(0)

        self.target_twist = Twist()

        rclpy.init(args=None)
        self.__node = rclpy.create_node('rover_driver')
        self.__node.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 1)

    def cmd_vel_callback(self, twist):
        self.target_twist = twist

    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)

        forward_speed = self.target_twist.linear.x
        angular_speed = self.target_twist.angular.z

        command_motor_left = (forward_speed - angular_speed * half_dist_wheels) / wheel_r
        command_motor_right = (forward_speed + angular_speed * half_dist_wheels) / wheel_r

        self.left_motor.setVelocity(command_motor_left)
        self.right_motor.setVelocity(command_motor_right)