# Copyright 2026
# SPDX-License-Identifier: Apache-2.0
"""First end-to-end debug pipeline for Marvin, bimanual.

    two rviz interactive markers (sources)
      -> two execution managers (validate / normalize / arbitrate, one per arm)
      -> two TaskSpaceKinematicPositionController instances (IK + joint position)
      -> ros2_control hardware (fake by default; real Marvin SDK opt-in)

Default is fake hardware (mock_components/GenericSystem): no real robot, no
vendor SDK, no CAN/network I/O. This is a source-only rehearsal of the
marker -> EM -> TSKPC chain, run independently for each arm
(Joint1_L..Joint7_L and Joint1_R..Joint7_R). RViz visualizes the hardware
state and hosts both markers.

Real hardware is opt-in via `use_fake_hardware:=false`. That loads
`marvin_hardware_interface/MarvinBimanualArmHardware`, which opens a TCP/IP
SDK connection to the Marvin controller at `robot_ip` and can command real
motor motion on both arms once their controllers are activated. Only pass
`use_fake_hardware:=false` with the real robot present, powered, and safed
per its own runbook -- never as a default or unattended launch.

Usage:
  ros2 launch marvin_rviz_debug_bringup rviz_debug_bringup.launch.py
  ros2 launch marvin_rviz_debug_bringup rviz_debug_bringup.launch.py use_rviz:=false
  ros2 launch marvin_rviz_debug_bringup rviz_debug_bringup.launch.py \
      use_fake_hardware:=false robot_ip:=10.19.0.191
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
import xacro


def _hardware_nodes(context: LaunchContext):
    marvin_share = get_package_share_directory("marvin_description")
    controllers_yaml = LaunchConfiguration("controllers_yaml")

    # get_package_share_directory() already returns a plain string, so build
    # this path with os.path.join rather than PathJoinSubstitution: xacro
    # needs a real path now, inside this OpaqueFunction, not a Substitution
    # that only resolves later.
    robot_description_xacro = os.path.join(marvin_share, "urdf", "marvin.urdf.xacro")
    robot_description = xacro.process_file(
        robot_description_xacro,
        mappings={
            "ros2_control": "true",
            "use_fake_hardware": context.perform_substitution(
                LaunchConfiguration("use_fake_hardware")
            ),
            "hardware_plugin": context.perform_substitution(
                LaunchConfiguration("hardware_plugin")
            ),
            "robot_ip": context.perform_substitution(LaunchConfiguration("robot_ip")),
        },
    ).toprettyxml(indent="  ")

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        name="controller_manager",
        output="screen",
        parameters=[{"robot_description": robot_description}, controllers_yaml],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    left_tskpc_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["left_task_space_kinematic_position_controller"],
        output="screen",
    )

    right_tskpc_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["right_task_space_kinematic_position_controller"],
        output="screen",
    )

    return [
        robot_state_publisher,
        controller_manager,
        joint_state_broadcaster_spawner,
        # Spawn both TSKPCs only after joint_state_broadcaster's spawner call
        # returns, instead of racing all three spawner processes against
        # controller_manager at once. Running them in parallel let two
        # spawner calls arrive after the target controller had already been
        # loaded/activated by a sibling spawner's call, so they died with
        # "can not be configured from 'active' state" even though the net
        # controller state was correct.
        RegisterEventHandler(
            OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[left_tskpc_spawner, right_tskpc_spawner],
            )
        ),
    ]


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


def _execution_manager_node(side: str) -> Node:
    """Execution manager instance for one arm.

    Instantiated directly (bypassing manipulation_execution_manager's own
    execution_manager.launch.py) so each side gets a distinct node name --
    that launch file hardcodes name="execution_manager" and has no
    per-instance name override, only a namespace argument that would leave
    the two instances' absolute topics/status keys unchanged anyway.
    """
    bringup_share = get_package_share_directory("marvin_rviz_debug_bringup")
    return Node(
        package="manipulation_execution_manager",
        executable="execution_manager",
        name=f"em_{side}",
        output="screen",
        parameters=[
            PathJoinSubstitution(
                [bringup_share, "config", f"execution_manager_{side}.yaml"]
            )
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
                "use_rviz", default_value="true", description="Launch RViz2."
            ),
            DeclareLaunchArgument(
                "controllers_yaml",
                default_value=PathJoinSubstitution(
                    [
                        get_package_share_directory("marvin_rviz_debug_bringup"),
                        "config",
                        "controllers.yaml",
                    ]
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
            OpaqueFunction(function=_hardware_nodes),
            _execution_manager_node("left"),
            _execution_manager_node("right"),
            _marker_node("left"),
            _marker_node("right"),
            rviz,
        ]
    )
