# runtime_resources

Example / tutorial ROS 2 packages for
[`physical_ai_runtime`](https://github.com/Gabriel-Ning/physical_ai_runtime).
Clone this repository under a workspace `src/` tree to practice Marvin-oriented
bringups; it is not a Pixi/colcon workspace by itself. Prefer `git clone` (not
a submodule of the workspace template). Embodiment and execution packages stay
**external** — clone them beside this tree under the workspace ownership paths.

## Packages in this repository

| Path | Role |
|------|------|
| `apps/marvin_rviz_debug_bringup` | Tutorial: RViz marker → EM → TSKPC (fake hardware first) |
| `apps/marvin_trajectory_jtc_test` | Tutorial: trajectory / JTC chain |
| `toolbox/rviz_interactive_marker_teleop` | Example PoseStamped source for RViz markers |

## External dependencies (clone beside this repo)

| Repository | Workspace path |
|------------|----------------|
| [`marvin_description`](https://github.com/Gabriel-Ning/marvin_description) | `src/embodiments/robots/marvin/marvin_description` |
| [`marvin_hardware_interface`](https://github.com/Gabriel-Ning/marvin_hardware_interface) | `src/embodiments/robots/marvin/marvin_hardware_interface` |
| [`manipulation_execution_manager`](https://github.com/Gabriel-Ning/manipulation_execution_manager) | `src/execution/manipulation_execution_manager` |

## Tutorial: assemble a Marvin debug workspace

From a `physical_ai_runtime` checkout:

```bash
mkdir -p src/embodiments/robots/marvin

git clone https://github.com/Gabriel-Ning/runtime_resources.git \
  src/runtime_resources
git clone https://github.com/Gabriel-Ning/marvin_description.git \
  src/embodiments/robots/marvin/marvin_description
git clone https://github.com/Gabriel-Ning/marvin_hardware_interface.git \
  src/embodiments/robots/marvin/marvin_hardware_interface
git clone https://github.com/Gabriel-Ning/manipulation_execution_manager.git \
  src/execution/manipulation_execution_manager

pixi run build
```

Then follow each app package README (start with
`apps/marvin_rviz_debug_bringup`, `use_fake_hardware:=true`).

`colcon` discovers packages recursively under `src/`.

## License

See each package for its own license text (Apache-2.0 unless noted).
