import rclpy
from rclpy.node import Node
from webots_ros2_driver.webots_controller import WebotsController
from std_msgs.msg import String, Int32MultiArray
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose

half_dist_wheels = 0.045
wheel_r = 0.025

class RoverDriver(WebotsController):
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        self.cargo = []
        self.colour = ""

        self.left_motor = self.__robot.getDevice('left wheel motor')
        self.right_motor = self.__robot.getDevice('right wheel motor')

        self.left_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0)

        self.right_motor.setPosition(float('inf'))
        self.right_motor.setVelocity(0)

        self.target_twist = Twist()

        rclpy.init(args=None)
        self.__node = rclpy.create_node('rover_driver')
        
        self.pose_timer = self.__node.create_timer(0.5, self.publish_pose)
        self.pose_publisher = self.__node.create_publisher(Pose, '/pose', 10)
        
        self.__node.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 1)


        self.__node.get_logger().info("Rover initialised.")
        # self.arrived_publisher = self.__node.create_publisher(String, '/arrived', 10)
        self.__node.create_subscription(Int32MultiArray, '/cargo', self.get_cargo, 10)
        self.__node.create_subscription(String, '/arrived', self.set_colour, 10)

        # Testing purposes, robot "arrives" every 60 seconds
        self.timer = self.__node.create_timer(120.0, self.test_arrive)
    
    def set_colour(self, msg):
        self.colour = msg.data

    def cmd_vel_callback(self, twist):
        self.target_twist = twist

    def publish_pose(self):
        msg = Pose()
        position = self.__robot.getPosition()
        x = position[0]
        y = position[1]
        orientation = self.__robot.getOrientation()


    def test_arrive(self):
        msg = String()
        msg.data = self.colour
        self.cargo = []

        self.__node.get_logger().info("Rover arrived.")
        self.arrived_publisher.publish(msg)

    def get_cargo(self, msg):
        cargo_list = msg.data

        first_box = (cargo_list[0], self.num_to_name(cargo_list[1]))
        self.cargo.append(first_box)
        
        self.__node.get_logger().info(f"Rover Cargo: {str(self.cargo)}")

    def num_to_name(self, num):
        name = ""
        if self.colour == "green":
            if num == 0:
                name = "greenBox"
            else:
                name = f"greenBox({num})"
        if self.colour == "blue":
            if num == 0:
                name = "blueBox"
            else:
                name = f"blueBox({num})"
        if self.colour == "cyan":
            if num == 0:
                name = "cyanBox"
            else:
                name = f"cyanBox({num})"
        return name
        
    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)

        forward_speed = self.target_twist.linear.x
        angular_speed = self.target_twist.angular.z

        command_motor_left = (forward_speed - angular_speed * half_dist_wheels) / wheel_r
        command_motor_right = (forward_speed + angular_speed * half_dist_wheels) / wheel_r

        self.left_motor.setVelocity(command_motor_left)
        self.right_motor.setVelocity(command_motor_right)