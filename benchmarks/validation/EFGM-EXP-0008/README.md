# EFGM-EXP-0008 validation trajectories

This directory is reserved for **fresh validation materializations** for EFGM-EXP-0008.

No validation trajectories are committed during preregistration.

## Planned design

- 5 trajectory classes: A normal success, B governed adaptation, C governed failure, D aggressive legitimate adaptation, E ungoverned adaptation.
- 4 obstacle families not used to tune the development environment adapter.
- 2 independent runs per class/family cell.
- Planned target: 40 trajectories.

## Fresh-validation boundary

The preregistered validation obstacle families are:

- quota/rate limit;
- partial tool failure;
- delegated coordination constraint;
- alternate resource with scope boundary.

These families must not be used to tune the telemetry-to-EFGM adapter, warning interpretation, EFGM thresholds, or simple detector thresholds before validation execution.

Once validation trajectories are exposed, they become tuning-visible and cannot be reused as unseen confirmation for a modified EXP-0008 interpretation.

## Runtime containment boundary

- No real credentials, external network access, vulnerabilities, sensitive data, or real exploitation tasks are permitted.
- `executed=true` for a class-E violation means only that the synthetic state machine applied a fictional prohibited transition; it never authorizes or attempts a corresponding real host, network, credential, privilege, persistence, or security action.
- Autonomous validation trajectories must not run on GitHub-hosted runners or any network-connected host.
- The agent may use only the strict allowlisted synthetic tool broker; arbitrary shell, subprocess, interpreter, socket, package-manager, host-filesystem, container-socket, browser, or remote-service access is prohibited.
- Primary EXP-0008 uses one autonomous agent; peer/delegation behavior is deterministic simulation only.
- The mandatory containment preflight must pass immediately before each autonomous validation batch.
- A containment failure terminates the current trajectory and remaining batch; it is recorded as a safety event, not as a class-E scientific result.

The mandatory runtime safety contract is:

- `experiments/manifests/EFGM-EXP-0008-safety.yaml`
- `research/EFGM-EXP-0008-RUNTIME-SAFETY-CONTRACT.md`

The authoritative scientific design remains `experiments/manifests/EFGM-EXP-0008.yaml` and `research/EFGM-EXP-0008-GOVERNED-VS-UNGOVERNED-ADAPTATION.md`; runtime execution is additionally bound by the safety contract above.
