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
    robot_description_path = pathlib.Path(os.path.join(package_dir, 'resource', 'panda.urdf')).read_text()

    webots = WebotsLauncher(
        world = os.path.join(package_dir, 'worlds','robo4_world.wbt')
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

    return LaunchDescription([
        webots,
        panda_driver,
        panda_sensor,
        panda_camera,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )            
    ])

    