import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
import math
from tf_transformations import euler_from_quaternion
from std_msgs.msg import String
from robo4_project.linked_list import CircularLinkedList

class RoverMove(Node):
    def __init__(self):
        super().__init__('rover_move')
        self.get_logger().info("Rover move init.")
       
        #self.movement = self.create_publisher(Twist, 'cmd_vel', 10)
        #self.create_subscription(Pose, 'pose', self.pose_callback, 10)
        #self.rover = None
        
        # Circular LinkedList to cycle through each colour
        self.colour_linkedlist = CircularLinkedList()
        self.colour_linkedlist.insert("green")
        self.colour_linkedlist.insert("blue")
        self.colour_linkedlist.insert("cyan")
        self.colour_node = None
        
        self.colour_node = self.colour_linkedlist.next(self.colour_node)
        self.colour = self.colour_node.data
        
        self.arrived_publisher = self.create_publisher(String, '/arrived', 10)
        

    def pose_callback(self, msg):
        self.get_logger().info("Rover pose callback init.")
        self.get_logger().info(f"Pose received: {msg}")
        self.rover = msg
        self.calculate_trajectory()
        #self.add_on_set_parameters_callback
        return

    def calculate_trajectory(self):
        x, y = None, None
        at_crate = False

        if self.at_bin(): # rover wants to move from bin to one of the cr
            if self.colour == "green": # rover wants to go to green crate
                x, y = 0.78, -1.29
            if self.colour == "blue":
                x, y = 2, -1.25
            if self.colour == "cyan":
                x, y = 1.39, -1.66
            at_crate = True
        else: # rover wants to move from boxes to bin
            x, y = 1.16, -4.08
            self.get_logger().info("Rover x: {x} y: {y}")

        yaw =(
            self.rover.orientation.x,
            self.rover.orientation.y,
            self.rover.orientation.z,
            self.rover.orientation.w
        )
        theta = euler_from_quaternion(yaw)[2]
             
        distance = self.calculate_distance(x, y)
        angtogoal = self.angle_to_goal(x, y) - theta
        self.make_move(0.0, angtogoal) # rover turns to face the goal
        self.make_move(distance, 0.0) # rover moves to goal
        
        if not at_crate:
            colour = "moving"
        else:
            colour = self.colour
        self.publish_arrival(colour)
        #if at bin, perform action to deposit and spawn the cargo into the bin
        #otherwise, pick up the cargo


    def calculate_distance(self, x, y): # distance from rover to goal destination
        return math.sqrt((x-self.rover.position.x)**2 + (y-self.rover.position.y)**2)
    
    def angle_to_goal(self, x, y):
        return math.arctan2((y - self.rover.position.x),(x - self.rover.position.x))

    def at_bin(self): # is the rover already at the bin
        return self.rover.position.x == 1.16 and self.rover.position.y == -4.08

    def make_move(self, x, yaw):
        msg = Twist()
        msg.angular.z = yaw
        msg.linear.x = x
        self.movement.publish(msg)
        return

    def publish_arrival(self, colour):
        msg = String()
        msg.data = colour
        self.cargo = []
        self.arrived_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = RoverMove()
    rclpy.spin(node)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()