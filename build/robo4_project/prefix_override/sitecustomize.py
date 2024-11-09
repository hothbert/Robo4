import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/thomas/UoA_Year4/CS4048/Robo4/install/robo4_project'
