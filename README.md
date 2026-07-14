# runtime_resources

**Example 1** packages for
[`physical_ai_runtime`](https://github.com/Gabriel-Ning/physical_ai_runtime):
Marvin apps and RViz marker teleop. Clone this repository under a workspace
`src/` tree; it is not a Pixi/colcon workspace by itself. Prefer `git clone`
(not a submodule). Marvin embodiment packages stay **external** under
`src/embodiments/robots/marvin/`.

The workspace also treats
[`manipulation_execution_manager`](https://github.com/Gabriel-Ning/manipulation_execution_manager)
and [`isaacteleop_toolbox`](https://github.com/Gabriel-Ning/isaacteleop_toolbox)
as **necessary** baseline packages (clone those from the runtime README first).

## Packages in this repository

| Path | Role |
|------|------|
| `apps/marvin_rviz_debug_bringup` | Example 1: RViz marker → EM → TSKPC (fake hardware first) |
| `apps/marvin_trajectory_jtc_test` | Example 1: trajectory / JTC chain |
| `toolbox/rviz_interactive_marker_teleop` | PoseStamped source for RViz markers |

## External packages used by Example 1

| Repository | Workspace path |
|------------|----------------|
| [`marvin_description`](https://github.com/Gabriel-Ning/marvin_description) | `src/embodiments/robots/marvin/marvin_description` |
| [`marvin_hardware_interface`](https://github.com/Gabriel-Ning/marvin_hardware_interface) | `src/embodiments/robots/marvin/marvin_hardware_interface` |
| [`manipulation_execution_manager`](https://github.com/Gabriel-Ning/manipulation_execution_manager) | `src/execution/manipulation_execution_manager` (necessary) |

## Assemble Example 1

From a `physical_ai_runtime` checkout (after the necessary EM / teleop clones):

```bash
mkdir -p src/embodiments/robots/marvin

git clone https://github.com/Gabriel-Ning/runtime_resources.git \
  src/runtime_resources
git clone https://github.com/Gabriel-Ning/marvin_description.git \
  src/embodiments/robots/marvin/marvin_description
git clone https://github.com/Gabriel-Ning/marvin_hardware_interface.git \
  src/embodiments/robots/marvin/marvin_hardware_interface

pixi run build
```

Then follow `apps/marvin_rviz_debug_bringup` (`use_fake_hardware:=true`).

`colcon` discovers packages recursively under `src/`.

## License

See each package for its own license text (Apache-2.0 unless noted).
