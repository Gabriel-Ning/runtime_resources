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

From a `physical_ai_runtime` checkout (after `vcs import src < repos/necessary.repos`):

```bash
# Embodiment repos (vcs; re-runnable / updatable with vcs pull)
vcs import src < repos/example1.repos

# This repo's apps/ and toolbox/ → src/apps and src/toolbox (no /tmp)
mkdir -p src/apps src/toolbox
curl -fsSL https://github.com/Gabriel-Ning/runtime_resources/archive/refs/heads/main.tar.gz \
  | tar -xz --strip-components=2 -C src/apps runtime_resources-main/apps
curl -fsSL https://github.com/Gabriel-Ning/runtime_resources/archive/refs/heads/main.tar.gz \
  | tar -xz --strip-components=2 -C src/toolbox runtime_resources-main/toolbox

pixi run build
```

`vcs` is used for full Git repositories. Apps/toolbox live in this monorepo, so
they are unpacked with `curl|tar` directly into `src/apps` and `src/toolbox`
(safe to re-run).

Then follow `src/apps/marvin_rviz_debug_bringup` (`use_fake_hardware:=true`).

`colcon` discovers packages recursively under `src/`.

## License

See each package for its own license text (Apache-2.0 unless noted).
