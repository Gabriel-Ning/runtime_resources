# marvin_rviz_marker_teleop

Local-PC UI for Marvin bimanual interactive-marker teleop:

```text
this machine                         peer CPU
─────────────                        ────────
2x RViz interactive marker  --DDS--> 2x EM -> 2x TSKPC -> hardware
(+ optional RViz2)
```

Owns only the high-level pose sources and visualization. Execution manager,
controllers, and hardware stay on the robot/CPU host via
`marvin_controller_bringup/controller_bringup.launch.py`.

## Distributed run

Both hosts must share the same `ROS_DOMAIN_ID`. For a dedicated LAN, copy
`.config/cyclonedds_template.xml`, fill `{{LOCAL_ADDRESS}}` /
`{{PEER_ADDRESS}}`, and export `CYCLONEDDS_URI` on each machine.

```bash
# CPU (robot host) — EM + TSKPC + hardware only
ros2 launch marvin_controller_bringup controller_bringup.launch.py

# Local PC — markers + RViz
ros2 launch marvin_rviz_marker_teleop rviz_marker_teleop.launch.py
```

Marker nodes wait on TF (`Base_L`/`flange_L`, `Base_R`/`flange_R`) from the
peer `robot_state_publisher`. When TF arrives, each marker seeds at the
current flange pose and streams:

- `/action_sources/marker_left/pose_target`
- `/action_sources/marker_right/pose_target`

Add InteractiveMarkers displays in RViz for namespaces `target_marker_left`
and `target_marker_right` if they are not already in the loaded config.

## Launch arguments

| Argument | Default | Description |
|---|---|---|
| `use_rviz` | `true` | Launch RViz2 with `marvin_description`'s `visualize_marvin.rviz` |

## Scope

- Pose sources + optional RViz only.
- Uses the pose topic contracts configured by
  `marvin_controller_bringup/controller_bringup.launch.py`.
- Does not start EM, `controller_manager`, or hardware.

## License

Apache-2.0. Composes `rviz_interactive_marker_teleop` and
`marvin_description`; see each for its own license text.
