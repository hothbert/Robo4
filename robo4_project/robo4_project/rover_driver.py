import rclpy
from rclpy.node import Node
from webots_ros2_driver.webots_controller import WebotsController
from std_msgs.msg import String, Int32MultiArray
from robo4_project.linked_list import CircularLinkedList
import time

half_dist_wheels = 0.045
wheel_r = 0.025

class RoverDriver(WebotsController):
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        #self.gps = self.__robot.getDevice('gps')
        #self.gps.enable(1)
        
        self.cargo = []
        self.sleep = 0
        # Circular LinkedList to cycle through each colour
        self.colour_linkedlist = CircularLinkedList()
        self.colour_linkedlist.insert("green")
        self.colour_linkedlist.insert("blue")
        self.colour_linkedlist.insert("cyan")
        self.colour_node = None
        
        self.colour_node = self.colour_linkedlist.next(self.colour_node)
        self.colour = self.colour_node.data

        rclpy.init(args=None)
        self.__node = rclpy.create_node('rover_driver')
        
        #self.pose_timer = self.__node.create_timer(0.5, self.publish_pose)
        #self.pose_publisher = self.__node.create_publisher(Pose, '/pose', 10)
        #self.__node.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 1)

        self.__node.get_logger().info("Rover initialised.")
        self.__node.create_subscription(Int32MultiArray, '/cargo', self.get_cargo, 10)
        self.arrived_publisher = self.__node.create_publisher(String, '/arrived', 10)

        self.timer = self.__node.create_timer(40.0, self.test_arrive) # Testing purposes, robot "arrives" every 30 seconds.

    def test_arrive(self):
        self.sleep = 1
        msg = String()
        msg.data = self.colour
        self.cargo = []
        self.__node.get_logger().info(f"Rover is travelling...")
        self.__node.get_logger().info(f"Rover arrived. ({self.colour})")
        self.arrived_publisher.publish(msg)

    def get_cargo(self, msg):
        cargo_list = msg.data

        first_box = (cargo_list[0], self.num_to_name(cargo_list[1]))
        self.cargo.append(first_box)
        
        if self.cargo[0][0] == 0:
            self.__node.get_logger().info(f"Rover Cargo: None")
        else:
            self.__node.get_logger().info(f"Rover Cargo: {str(self.cargo)}")
        
        self.colour_node = self.colour_linkedlist.next(self.colour_node)
        self.colour = self.colour_node.data
        self.__node.get_logger().info(f"Rover is travelling...")
        self.__node.get_logger().info(f"Rover returned to base.")

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
    
    #def publish_pose(self):
        #msg = Pose()
        #position = self.gps.getValues()
        #x = position[0]
        #y = position[1]
        #yaw = position[2]   


    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)