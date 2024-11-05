import os
import pathlib
import launch
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController


def generate_launch_description():
    package_dir = get_package_share_directory('robo4_project')
    robot_description_path = pathlib.Path(os.path.join(package_dir, 'resource', 'ned.urdf')).read_text()

    webots = WebotsLauncher(
        world = os.path.join(package_dir, 'worlds','robo4_world.wbt')
    )

    ned_driver = WebotsController(
        robot_name='ned',
        parameters=[
            {'robot_description': robot_description_path}
        ]
    )

    return LaunchDescription([
        webots,
        ned_driver,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )            
    ])

    