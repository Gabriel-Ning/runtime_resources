# runtime_resources

ROS 2 application packages for
[`physical_ai_runtime`](https://github.com/Gabriel-Ning/physical_ai_runtime).
The repository is intentionally flat so it can be imported once with
`vcstool` and discovered recursively by `colcon`.

## Packages

| Package | Purpose |
|---|---|
| `marvin_motion_planning_bringup` | Config-driven PyRoki setpoint, trajectory, and MPC demos |
| `marvin_rviz_debug_bringup` | Marvin RViz and execution-chain debugging |
| `marvin_trajectory_jtc_test` | EM-to-JTC trajectory-chain validation |

Reusable workspace-owned tools such as `rviz_interactive_marker_teleop` do not
live here. They are maintained directly under
`physical_ai_runtime/src/toolbox`.

## Import into physical_ai_runtime

`physical_ai_runtime/repos/necessary.repos` maps this repository to
`src/apps`:

```bash
vcs import src < repos/necessary.repos
vcs import src < repos/embodiment.repos
pixi run build
```

Do not copy individual packages or use the removed Example 1 fetch script.
Each directory at this repository root is an independent ROS package.

## License

See each package for its license declaration (Apache-2.0 unless noted).
