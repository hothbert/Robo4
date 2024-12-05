from setuptools import find_packages, setup

package_name = 'robo4_project'
data_files = []
data_files.append(('share/ament_index/resource_index/packages', ['resource/' + package_name]))
data_files.append(('share/' + package_name + '/launch', ['launch/robo4_project_launch.py']))
data_files.append(('share/' + package_name + '/worlds', ['worlds/robo4_world.wbt']))
data_files.append(('share/' + package_name + '/resource', ['resource/panda.urdf']))
data_files.append(('share/' + package_name + '/resource', ['resource/rover.urdf']))
data_files.append(('share/' + package_name, ['package.xml']))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='thomas',
    maintainer_email='u05tp21@abdn.ac.uk',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'panda_driver = robo4_project.panda_driver:main',
            'panda_sensor = robo4_project.panda_sensor:main',
            'panda_camera = robo4_project.panda_camera:main',
            'panda_sort = robo4_project.panda_sort:main',
            'sorted_box_queue = robo4_project.sorted_box_queue:main',
            'rover_driver = robo4_project.rover_driver',
        ],
    },
)