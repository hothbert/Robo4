import rclpy
from rclpy.node import Node
from controller import Supervisor
from webots_ros2_driver.webots_controller import WebotsController
from std_msgs.msg import String, Int32MultiArray
from robo4_project.sorted_box_queue import Queue
import random
import re

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

        # Arrays to store each colour box when spawned (Not sorted, will be sorted when rover arrives to increase efficiency).
        self.green_array = []
        self.cyan_array = []
        self.blue_array = []

        # Arrays that store each colour bax after being sorted into crates
        self.green_sorted = Queue()
        self.cyan_sorted = Queue()
        self.blue_sorted = Queue()

        self.gripper_left = self.__robot.getDevice('panda_finger::left')
        self.gripper_right = self.__robot.getDevice('panda_finger::right')
        self.joint_4 = self.__robot.getDevice('panda_joint4')
        self.joint_6 = self.__robot.getDevice('panda_joint6')
        self.joint_2 = self.__robot.getDevice('panda_joint2')
        self.joint_1 = self.__robot.getDevice('panda_joint1')

        self.node.create_subscription(String, '/gripper_command', self.gripper_command_callback, 10)
        self.node.create_subscription(String, '/move_command', self.grab_callback, 10)

        self.node.create_subscription(String, '/arrived', self.transfer_cargo, 10)
        self.cargo_publisher = self.node.create_publisher(Int32MultiArray, '/cargo', 10)

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
            blueBox = self.blue_array.pop(0)
            self.blue_sorted.add(blueBox)
            self.node.get_logger().info("Blue Box Sorted.")
            self.node.get_logger().info(f"Blue Box Q: {str(self.blue_sorted.queue)}")
        elif command == "turn_green":
            self.joint_1.setPosition(2.0)
            self.joint_2.setPosition(0)
            greenBox = self.green_array.pop(0)
            self.green_sorted.add(greenBox)
            self.node.get_logger().info("Green Box Sorted.")
            self.node.get_logger().info(f"Green Box Q: {str(self.green_sorted.queue)}")
        elif command == "turn_cyan":
            self.joint_1.setPosition(2.95)
            self.joint_2.setPosition(0)
            cyanBox = self.cyan_array.pop(0)
            self.cyan_sorted.add(cyanBox)
            self.node.get_logger().info("Cyan Box Sorted.")
            self.node.get_logger().info(f"Cyan Box Q: {str(self.cyan_sorted.queue)}")
        elif command == "turn_back":
            self.joint_1.setPosition(0)

    def transfer_cargo(self, msg):
        cargo = []

        if msg.data == "green":
            # Sorts the array with MergeSort, to get highest priority items
            self.green_sorted.queue = self.green_sorted.merge_sort(self.green_sorted.queue)
            # Transfers first three items from each colours queue to the cargo array.
            box = self.green_sorted.pop()
            cargo.append(box)
            self.node.get_logger().info("Green box transferred to rover.")

        if msg.data == "blue":
            self.blue_sorted.queue = self.blue_sorted.merge_sort(self.blue_sorted.queue)
            box = self.blue_sorted.pop()
            cargo.append(box)
            self.node.get_logger().info("Blue box transferred to rover.")

        if msg.data == "cyan":
            self.cyan_sorted.queue = self.cyan_sorted.merge_sort(self.cyan_sorted.queue)
            box = self.cyan_sorted.pop()
            cargo.append(box)
            self.node.get_logger().info("Cyan box transferred to rover.")

        self.node.get_logger().info(f"Cargo Q: {str(cargo)}")
        self.send_cargo(cargo)

    def send_cargo(self, cargo):
        msg = Int32MultiArray()
        msg.data = []

        for box in cargo:
            priority = box[0]
            box_name = box[1]
            box_num = self.get_box_number(box_name)
            
            msg.data.append(priority)
            msg.data.append(box_num)

        self.cargo_publisher.publish(msg)

    # Function that returns the number of the box e.g. greenBox(5) returns 5. This is to make it easy to publish a list of [priority, box_num, priority, box_num, ...]
    def get_box_number(self, box_name: str) -> int:
        match = re.search(r'\((\d+)\)', box_name)
        if match:
            return int(match.group(1))
        else:
            return 0

    def spawn_box(self):
        num = 1 # random.randint(1,3)
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
