import rclpy
from rclpy.node import Node
from controller import Supervisor
from webots_ros2_driver.webots_controller import WebotsController
from std_msgs.msg import String
from robo4_project.priority_queue import PriorityQueue
import random


#this serves as an interface between ros2 nodes and the webots robot
#its soul purpose is to send positions to each joint
#it subscribes to robot movement commands and acts upon them
#lets not put any logic here, save that for the actual ros2 nodes

class PandaRobotDriver(WebotsController):
    def init(self, webots_node, properties):
        #creates a node so that rclpy features can be used, since PandaRobotDriver doesnt inherit from Node
        rclpy.init()
        self.node = Node('panda_driver')
        self.__robot=webots_node.robot
        
        self.supervisor=Supervisor()

        # Counters for boxes
        self.green_count = 0
        self.cyan_count = 0
        self.blue_count = 0

        # Arrays to store each colour box when spawned (Not sorted)
        self.green_array = []
        self.cyan_array = []
        self.blue_array = []

        # Arrays that store each colour bax after being sorted (Priority Queues)
        self.green_sorted = PriorityQueue()
        self.cyan_sorted = PriorityQueue()
        self.blue_sorted = PriorityQueue()

        self.gripper_left = self.__robot.getDevice('panda_finger::left')
        self.gripper_right = self.__robot.getDevice('panda_finger::right')
        self.joint_4 = self.__robot.getDevice('panda_joint4')
        self.joint_6 = self.__robot.getDevice('panda_joint6')
        self.joint_2 = self.__robot.getDevice('panda_joint2')
        self.joint_1 = self.__robot.getDevice('panda_joint1')

        self.node.create_subscription(String, '/gripper_command', self.gripper_command_callback, 10)
        self.node.create_subscription(String, '/move_command', self.grab_callback, 10)

        self.timer = self.node.create_timer(10.0, self.spawn_box)

    def gripper_command_callback(self, msg):
        command = msg.data
        if command == "open":
            self.gripper_left.setPosition(0.04)  
            self.gripper_right.setPosition(0.04)
            self.node.get_logger().info("Gripper opened.")           
        elif command == "close":
            self.gripper_left.setPosition(0.0)  
            self.gripper_right.setPosition(0.0)
            self.node.get_logger().info("Gripper closed.")

    #needs tidying up
    def grab_callback(self, msg):
        command = msg.data
        if command =="grab": #don't touch unless robot isnt picking up properly!
            self.joint_4.setPosition(-2.5)
            self.joint_6.setPosition(2.85)
            self.joint_2.setPosition(0.3)
        elif command =="stand":
            self.joint_4.setPosition(-1.77)
            self.joint_6.setPosition(1.6)
        elif command == "turn_blue":        # might want to play with these to get it to drop the block
            self.joint_1.setPosition(-2.0)  # gently, without coliding with other blocks on the conveyer belt
            self.joint_2.setPosition(0)
        elif command == "turn_green":
            self.joint_1.setPosition(2.0)
            self.joint_2.setPosition(0)
        elif command == "turn_cyan":
            self.joint_1.setPosition(2.95)
            self.joint_2.setPosition(0)
        elif command == "turn_back":
            self.joint_1.setPosition(0)

    def spawn_box(self):
        num = random.randint(1,3)
        colour = ""

        if num == 1:
            new_box = '''
            SolidBox {
                name "greenBox"
                translation -2.4 0.0098 0.164785
                rotation -0.03435408067732627 -0.9981572723864834 -0.05001856378177188 0.027683970180604204
                size 0.07 0.07 0.07
                appearance Appearance {
                    material Material {
                    ambientIntensity 1
                    diffuseColor 0 1 0
                    emissiveColor 0 1 0
                    shininess 0
                    specularColor 0 1 0
                    }
                }
                physics Physics {
                }  
            }
            '''
            priority = random.randint(1,5)
            if self.green_count == 0:
                self.green_array.append((priority, "greenBox"))
                name = f"greenBox"
            else:
                self.green_array.append((priority, f"greenBox({self.green_count})"))
                name = f"greenBox({self.green_count})"
            self.green_count += 1

        if num == 2:
            new_box = '''
            SolidBox {
                name "cyanBox"
                translation -2.4 0.0098 0.164785
                rotation -0.03435408067732627 -0.9981572723864834 -0.05001856378177188 0.027683970180604204
                size 0.07 0.07 0.07
                appearance Appearance {
                    material Material {
                    ambientIntensity 1
                    diffuseColor 0 1 1
                    emissiveColor 0 1 1
                    shininess 0
                    specularColor 0 1 1
                    }
                }
                physics Physics {
                }
            }
            '''
            priority = random.randint(1,5)
            if self.cyan_count == 0:
                self.cyan_array.append((priority, "cyanBox"))
                name = "cyanBox"
            else:
                self.cyan_array.append((priority, f"cyanBox({self.cyan_count})"))
                name = f"cyanBox({self.cyan_count})"
            self.cyan_count += 1

        if num == 3:
            new_box = '''
            SolidBox {
                name "blueBox"
                translation -2.4 0.0098 0.164785
                rotation -0.03435408067732627 -0.9981572723864834 -0.05001856378177188 0.027683970180604204
                size 0.07 0.07 0.07
                appearance Appearance {
                    material Material {
                    ambientIntensity 1
                    diffuseColor 0 0 1
                    emissiveColor 0 0 1
                    shininess 0
                    specularColor 0 0 1
                    }
                }
                physics Physics {
                }
            }
            '''
            priority = random.randint(1,5)
            if self.blue_count == 0:
                self.blue_array.append((priority, "blueBox"))
                name = f"blueBox"
            else:
                self.blue_array.append((priority, f"blueBox({self.blue_count})"))
                name = f"blueBox({self.blue_count})"
            self.blue_count += 1

        root = self.supervisor.getRoot()
        children_field = root.getField('children')

        children_field.importMFNodeFromString(-1, new_box)
        self.node.get_logger().info(f"Box spawned - Name: {name} - Priority: {priority}")

        self.supervisor.step(int(self.supervisor.getBasicTimeStep()))

    def step(self):
        rclpy.spin_once(self.node, timeout_sec=0) #starts self.node so that subscription works
