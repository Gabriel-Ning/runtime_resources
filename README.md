# runtime_resources

Example 1 packages for
[`physical_ai_runtime`](https://github.com/Gabriel-Ning/physical_ai_runtime).
This repository is only a small folder tree — not a Pixi/colcon workspace by
itself. Place packages into the matching workspace `src/` paths:

```text
runtime_resources/apps/      →  physical_ai_runtime/src/apps/
runtime_resources/toolbox/   →  physical_ai_runtime/src/toolbox/
```

Do **not** nest this whole repo as `src/runtime_resources/`.

## Packages (Example 1)

| Path in this repo | Place under workspace |
|-------------------|------------------------|
| `apps/marvin_rviz_debug_bringup` | `src/apps/marvin_rviz_debug_bringup` |
| `apps/marvin_trajectory_jtc_test` | `src/apps/marvin_trajectory_jtc_test` |
| `toolbox/rviz_interactive_marker_teleop` | `src/toolbox/rviz_interactive_marker_teleop` |

## External packages used by Example 1

| Repository | Workspace path |
|------------|----------------|
| [`marvin_description`](https://github.com/Gabriel-Ning/marvin_description) | `src/embodiments/robots/marvin/marvin_description` |
| [`marvin_hardware_interface`](https://github.com/Gabriel-Ning/marvin_hardware_interface) | `src/embodiments/robots/marvin/marvin_hardware_interface` |
| [`manipulation_execution_manager`](https://github.com/Gabriel-Ning/manipulation_execution_manager) | `src/execution/manipulation_execution_manager` (necessary) |

The workspace also treats
[`isaacteleop_toolbox`](https://github.com/Gabriel-Ning/isaacteleop_toolbox)
as necessary (`src/teleop/isaacteleop_toolbox`).

## Assemble Example 1

From a `physical_ai_runtime` checkout (after necessary EM / teleop clones):

```bash
git clone https://github.com/Gabriel-Ning/runtime_resources.git /tmp/runtime_resources
cp -a /tmp/runtime_resources/apps/marvin_rviz_debug_bringup \
      /tmp/runtime_resources/apps/marvin_trajectory_jtc_test \
      src/apps/
cp -a /tmp/runtime_resources/toolbox/rviz_interactive_marker_teleop \
      src/toolbox/

mkdir -p src/embodiments/robots/marvin
git clone https://github.com/Gabriel-Ning/marvin_description.git \
  src/embodiments/robots/marvin/marvin_description
git clone https://github.com/Gabriel-Ning/marvin_hardware_interface.git \
  src/embodiments/robots/marvin/marvin_hardware_interface

pixi run build
```

Then follow `src/apps/marvin_rviz_debug_bringup` (`use_fake_hardware:=true`).

`colcon` discovers packages recursively under `src/`.

## License

See each package for its own license text (Apache-2.0 unless noted).
