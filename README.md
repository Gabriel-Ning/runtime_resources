# runtime_resources

Reusable ROS 2 packages for
[`physical_ai_runtime`](https://github.com/Gabriel-Ning/physical_ai_runtime)
workspaces. This repository is meant to be checked out under a workspace
`src/` tree (for example as a Git submodule); it is not a Pixi/colcon
workspace by itself.

## Packages

| Path | Description |
|------|-------------|
| `apps/marvin_rviz_debug_bringup` | Marvin bimanual RViz marker → EM → TSKPC debug bringup |
| `apps/marvin_trajectory_jtc_test` | Marvin trajectory / JTC chain test bringup |
| `toolbox/rviz_interactive_marker_teleop` | RViz interactive-marker pose source |

## Use with physical_ai_runtime

From a `physical_ai_runtime` checkout:

```bash
git submodule add git@github.com:Gabriel-Ning/runtime_resources.git src/runtime_resources
# or: git clone git@github.com:Gabriel-Ning/runtime_resources.git src/runtime_resources
pixi run build
```

`colcon` discovers packages recursively under `src/`.

## License

See each package for its own license text (Apache-2.0 unless noted).
