# EFGM-EXP-0008 development trajectories

This directory is reserved for **tuning-visible development materializations** for EFGM-EXP-0008.

No autonomous trajectories are committed during preregistration.

## Planned design

- 5 trajectory classes: A normal success, B governed adaptation, C governed failure, D aggressive legitimate adaptation, E ungoverned adaptation.
- 4 development obstacle families.
- 3 independent runs per class/family cell.
- Planned target: 60 trajectories.

## Controls

- Environment labels come from deterministic policy/event facts and do not consume EFGM scores.
- Scripted calibration trajectories, when added, must be clearly marked `calibration_only` and excluded from hypothesis testing.
- The telemetry-to-EFGM adapter must be frozen before autonomous development results are interpreted.
- Failed, cancelled, or malformed runs remain recorded; they may not be silently replaced to improve results.
- No real credentials, external network access, vulnerabilities, sensitive data, or real exploitation tasks are permitted.
- `executed=true` for a class-E violation means only that the synthetic state machine applied a fictional prohibited transition; it never authorizes or attempts a corresponding real host, network, credential, privilege, persistence, or security action.
- Autonomous trajectories must not run on GitHub-hosted runners or any network-connected host.
- The agent may use only the strict allowlisted synthetic tool broker; arbitrary shell, subprocess, interpreter, socket, package-manager, host-filesystem, container-socket, browser, or remote-service access is prohibited.
- Primary EXP-0008 uses one autonomous agent; peer/delegation behavior is deterministic simulation only.
- A mandatory containment preflight and human phase gate must pass before any autonomous development batch starts.
- Any containment anomaly terminates the current trajectory and the remaining batch and is not counted as scientific evidence.

The mandatory runtime safety contract is:

- `experiments/manifests/EFGM-EXP-0008-safety.yaml`
- `research/EFGM-EXP-0008-RUNTIME-SAFETY-CONTRACT.md`

The authoritative scientific design remains `experiments/manifests/EFGM-EXP-0008.yaml` and `research/EFGM-EXP-0008-GOVERNED-VS-UNGOVERNED-ADAPTATION.md`; runtime execution is additionally bound by the safety contract above.
