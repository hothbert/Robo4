import os
import pathlib
import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController


def generate_launch_description():
    package_dir = get_package_share_directory('robo4_project')
    robot_description_path = pathlib.Path(os.path.join(package_dir, 'resource', 'demo.urdf')).read_text()
    controller_path = os.path.join(package_dir, 'resource', 'panda_joints.yaml')

    webots = WebotsLauncher(
        world = os.path.join(package_dir, 'worlds','robo4_world.wbt')
    )

    ros2_control_node = Node(
        package = 'controller_manager',
        executable ='ros2_control_node',
        name = 'ros2_control_node',
        parameters=[{'robot_description': robot_description_path}, controller_path],
        output='screen'
    )

    panda_driver = WebotsController(
        robot_name='Panda',
        parameters=[
            {'robot_description': robot_description_path}
        ]
    )

    panda_sensor = Node(
        package='robo4_project',
        executable='panda_sensor'
    )

    panda_camera = Node(
        package='robo4_project',
        executable='panda_camera'
    )

    panda_sort = Node(
        package = 'robo4_project',
        executable = 'panda_sort'
    )

    return LaunchDescription([
        webots,
        panda_driver,
        ros2_control_node,
        panda_sensor,
        panda_camera,
        panda_sort,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )            
    ])

    