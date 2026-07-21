# Copyright 2026
# SPDX-License-Identifier: Apache-2.0
"""Local-PC RViz interactive-marker UI for Marvin bimanual teleop.

    two rviz interactive markers (this machine)
      --DDS-->
    two execution managers + TSKPC + hardware (peer CPU)

Does not start EM, controllers, or hardware. Pair with
`marvin_controller_bringup` on the robot/CPU host:

  # CPU (robot host)
  ros2 launch marvin_controller_bringup controller_bringup.launch.py

  # Local PC (this package)
  ros2 launch marvin_rviz_marker_teleop rviz_marker_teleop.launch.py

Both hosts need the same ROS_DOMAIN_ID. For cross-machine DDS, set
CYCLONEDDS_URI from `.config/cyclonedds_template.xml` on each side.
"""
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
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
    marvin_share = get_package_share_directory("marvin_description")
    use_rviz = LaunchConfiguration("use_rviz")

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=[
            "--display-config",
            PathJoinSubstitution([marvin_share, "rviz", "visualize_marvin.rviz"]),
        ],
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_rviz",
                default_value="true",
                description="Launch RViz2 with Marvin visualization config.",
            ),
            _marker_node("left"),
            _marker_node("right"),
            rviz,
        ]
    )
