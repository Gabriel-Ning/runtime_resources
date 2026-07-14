# runtime_resources

Reusable ROS 2 packages for
[`physical_ai_runtime`](https://github.com/Gabriel-Ning/physical_ai_runtime)
workspaces. Clone this repository under a workspace `src/` tree; it is not a
Pixi/colcon workspace by itself. Prefer `git clone` (not a submodule of the
workspace template).

## Packages in this repository

| Path | Description |
|------|-------------|
| `apps/marvin_rviz_debug_bringup` | Marvin bimanual RViz marker → EM → TSKPC debug bringup |
| `apps/marvin_trajectory_jtc_test` | Marvin trajectory / JTC chain test bringup |
| `toolbox/rviz_interactive_marker_teleop` | RViz interactive-marker pose source |

## Related Marvin embodiment packages

These live in their own repositories. Clone them into the workspace ownership
path `src/embodiments/robots/marvin/` (not into this repository):

| Repository | Workspace path |
|------------|----------------|
| [`marvin_description`](https://github.com/Gabriel-Ning/marvin_description) | `src/embodiments/robots/marvin/marvin_description` |
| [`marvin_hardware_interface`](https://github.com/Gabriel-Ning/marvin_hardware_interface) | `src/embodiments/robots/marvin/marvin_hardware_interface` |

Marvin apps in this repository expect those packages (plus
`manipulation_execution_manager`) to be present in the same colcon workspace.

## Use with physical_ai_runtime

From a `physical_ai_runtime` checkout:

```bash
# Bringups / toolbox from this repo
git clone https://github.com/Gabriel-Ning/runtime_resources.git \
  src/runtime_resources

# Marvin embodiment (required by Marvin apps above)
mkdir -p src/embodiments/robots/marvin
git clone https://github.com/Gabriel-Ning/marvin_description.git \
  src/embodiments/robots/marvin/marvin_description
git clone https://github.com/Gabriel-Ning/marvin_hardware_interface.git \
  src/embodiments/robots/marvin/marvin_hardware_interface

pixi run build
```

`colcon` discovers packages recursively under `src/`.

## License

See each package for its own license text (Apache-2.0 unless noted).
