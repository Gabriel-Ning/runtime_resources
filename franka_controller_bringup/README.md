# franka_controller_bringup

Physical AI Runtime controller bringup for one Franka FR3 arm:

```text
pose source
  -> manipulation_execution_manager
  -> TaskSpaceKinematicPositionController
  -> ros2_control position command interfaces
  -> fake or real Franka hardware
```

This app owns the runtime composition and its parameters. The vendor
`franka_bringup` package remains responsible for the FR3 description,
`robot_state_publisher`, controller manager, joint-state publication, and
Franka hardware plugin.

## Launch modes

For a distributed robot/CPU service without UI:

```bash
ros2 launch franka_controller_bringup controller_bringup.launch.py
```

For an all-in-one local fake-hardware debug session:

```bash
ros2 launch franka_controller_bringup rviz_debug_bringup.launch.py
```

The debug entrypoint composes the same pure controller service with
`rviz_marker_teleop profile:=franka`. Both modes default to fake hardware.

## Unified joint-controller contract

The Franka ros2_control description exports these interfaces for each
`fr3_joint1` through `fr3_joint7`:

- command: `position`, `velocity`, `effort`
- state: `position`, `velocity`, `effort`

The task-space kinematic position controller claims only the standard
`<joint>/position` command interface and reads standard joint state
interfaces. No Franka-specific controller adapter is required.

## Fake-hardware gate

Fake hardware is the default and does not connect to a robot:

```bash
ros2 launch franka_controller_bringup controller_bringup.launch.py
```

Expected:

```bash
ros2 control list_controllers
```

reports both `joint_state_broadcaster` and
`task_space_kinematic_position_controller` as `active`. Also verify:

```bash
ros2 control list_hardware_interfaces
ros2 topic echo /joint_states --once
ros2 topic echo /execution_manager/status --once
```

The seven `fr3_joint*/position` command interfaces must be claimed by TSKPC.
The execution-manager status remains idle until a valid source message arrives.

The configured pose input is:

```text
/action_sources/marker/pose_target
```

with type `geometry_msgs/msg/PoseStamped`, expressed in `fr3_link0`.

## Real hardware

Only after the fake-hardware gate passes:

```bash
ros2 launch franka_controller_bringup controller_bringup.launch.py \
  use_fake_hardware:=false robot_ip:=192.168.2.101
```

This opens the Franka connection and activates a position-command controller.
A valid pose message can therefore cause real motion. Use this only with the
FR3 powered, unlocked, safed according to the site runbook, and with someone
at the emergency stop.

## Scope

- single FR3 arm
- no gripper
- no namespace or arm prefix
- `controller_bringup.launch.py` starts no RViz or interactive-marker process
- `rviz_debug_bringup.launch.py` composes the Franka marker/RViz profile
- fake hardware by default

Other Franka models and multi-arm/prefixed deployments need model-specific
joint names, frames, and joint-limit profiles and are intentionally deferred.
