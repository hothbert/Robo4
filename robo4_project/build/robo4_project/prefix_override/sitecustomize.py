import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/holly/ros2_ws/src/Robo4/robo4_project/install/robo4_project'
