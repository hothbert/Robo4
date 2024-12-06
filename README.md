# Robo4

Welcome to our project.

Our Project uses Webots with Ros2, so make sure you have both of these installed on your machine. 
<br>You will also need the webots_ros2_driver package:
* `sudo apt-get install ros-jazzy-webots-ros2`

A full tutorial for installing webots is available [here](https://docs.ros.org/en/jazzy/Tutorials/Advanced/Simulators/Webots/Installation-Ubuntu.html)

To run the project, simply open terminal and navigate to the directory Robo4/robo4_project.

Once in the directory, please source ROS with the command: `source /opt/ros/jazzy/setup.bash`

Then build the package with the command: `colcon build`

Then run the command: `source install/local_setup.bash`

Before finally running the command: `ros2 launch robo4_project robo4_project_launch.py`

This will open Webots and run the program.


