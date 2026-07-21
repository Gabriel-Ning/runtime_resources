# Copyright 2026
# SPDX-License-Identifier: Apache-2.0
"""Legacy all-in-one Marvin RViz debug launch.

Includes the marker-free controller bringup, then adds the two interactive
marker sources. Prefer controller_bringup.launch.py on a distributed CPU host.
"""
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def _marker_node(side: str) -> Node:
    """RViz interactive marker source for one arm.

    Instantiated directly (bypassing rviz_interactive_marker_teleop's own
    teleop.launch.py) so each side gets a distinct node name -- that launch
    file hardcodes name="target_marker_node" and has no namespace argument.
    """
    suffix = "L" if side == "left" else "R"
    return Node(
        package="rviz_interactive_marker_teleop",
        executable="target_marker_node.py",
        name=f"target_marker_{side}",
        output="screen",
        parameters=[
            {
                "base_frame": f"Base_{suffix}",
                "target_frame": f"flange_{suffix}",
                "pose_topic": f"/action_sources/marker_{side}/pose_target",
                "publish_frequency": 50.0,
                "server_namespace": f"target_marker_{side}",
                "marker_name": f"marvin_{side}_target",
                "marker_description": f"Marvin {side.title()} Target Pose",
            }
        ],
    )


def generate_launch_description() -> LaunchDescription:
    bringup_share = get_package_share_directory("marvin_controller_bringup")

    markers = GroupAction(
        condition=IfCondition(LaunchConfiguration("use_markers")),
        actions=[
            _marker_node("left"),
            _marker_node("right"),
        ],
    )

    controller_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [bringup_share, "launch", "controller_bringup.launch.py"]
            )
        ),
        launch_arguments={
            "use_rviz": LaunchConfiguration("use_rviz"),
            "controllers_yaml": LaunchConfiguration("controllers_yaml"),
            "use_fake_hardware": LaunchConfiguration("use_fake_hardware"),
            "hardware_plugin": LaunchConfiguration("hardware_plugin"),
            "robot_ip": LaunchConfiguration("robot_ip"),
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_rviz", default_value="true", description="Launch RViz2."
            ),
            DeclareLaunchArgument(
                "use_markers",
                default_value="true",
                description=(
                    "Launch both interactive-marker sources. Set false on the "
                    "CPU host when markers run via marvin_rviz_marker_teleop."
                ),
            ),
            DeclareLaunchArgument(
                "controllers_yaml",
                default_value=PathJoinSubstitution(
                    [bringup_share, "config", "controllers.yaml"]
                ),
                description="controller_manager + TSKPC parameter file (both arms).",
            ),
            DeclareLaunchArgument(
                "use_fake_hardware",
                default_value="true",
                description=(
                    "true: mock_components/GenericSystem (default, safe). "
                    "false: real Marvin SDK bridge -- only with the robot "
                    "present, powered, and safed."
                ),
            ),
            DeclareLaunchArgument(
                "hardware_plugin",
                default_value="marvin_hardware_interface/MarvinBimanualArmHardware",
                description="Real ros2_control hardware plugin (used when use_fake_hardware:=false).",
            ),
            DeclareLaunchArgument(
                "robot_ip",
                default_value="10.19.0.191",
                description="Marvin controller IP (used when use_fake_hardware:=false).",
            ),
            controller_bringup,
            markers,
        ]
    )
