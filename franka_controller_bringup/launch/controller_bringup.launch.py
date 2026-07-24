# Copyright 2026
# SPDX-License-Identifier: Apache-2.0
"""Physical AI Runtime controller bringup for one Franka FR3 arm.

The vendor package owns robot description and ros2_control hardware startup.
This app adds the runtime execution manager and TSKPC composition.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    """Compose the vendor FR3 bringup with the Physical AI control path."""
    bringup_share = FindPackageShare('franka_controller_bringup')

    franka_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare('franka_bringup'),
                    'launch',
                    'franka.launch.py',
                ]
            )
        ),
        launch_arguments={
            'robot_type': 'fr3',
            'arm_prefix': '',
            'namespace': '',
            'robot_ip': LaunchConfiguration('robot_ip'),
            'load_gripper': 'false',
            'use_fake_hardware': LaunchConfiguration('use_fake_hardware'),
            'fake_sensor_commands': 'false',
            'joint_state_rate': '100',
            'load_franka_robot_state_broadcaster': LaunchConfiguration(
                'load_franka_robot_state_broadcaster'
            ),
            'controllers_yaml': LaunchConfiguration('controllers_yaml'),
        }.items(),
    )

    tskpc_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['task_space_kinematic_position_controller'],
        output='screen',
    )

    execution_manager = Node(
        package='manipulation_execution_manager',
        executable='execution_manager',
        name='execution_manager',
        output='screen',
        parameters=[LaunchConfiguration('execution_manager_yaml')],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'controllers_yaml',
                default_value=PathJoinSubstitution(
                    [bringup_share, 'config', 'controllers.yaml']
                ),
                description='controller_manager and TSKPC parameter file.',
            ),
            DeclareLaunchArgument(
                'execution_manager_yaml',
                default_value=PathJoinSubstitution(
                    [bringup_share, 'config', 'execution_manager.yaml']
                ),
                description='Execution-manager route profile.',
            ),
            DeclareLaunchArgument(
                'use_fake_hardware',
                default_value='true',
                description=(
                    'Use mock_components/GenericSystem. Set false only for a '
                    'present, powered, and safed FR3.'
                ),
            ),
            DeclareLaunchArgument(
                'robot_ip',
                default_value='192.168.2.101',
                description='FR3 hostname or IP; ignored by fake hardware.',
            ),
            DeclareLaunchArgument(
                'load_franka_robot_state_broadcaster',
                default_value='true',
                description=(
                    'Load the vendor robot-state broadcaster on real '
                    'hardware. The vendor bringup skips it automatically on '
                    'fake hardware.'
                ),
            ),
            franka_bringup,
            tskpc_spawner,
            execution_manager,
        ]
    )
