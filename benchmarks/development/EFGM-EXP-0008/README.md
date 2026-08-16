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

The authoritative design is `experiments/manifests/EFGM-EXP-0008.yaml` and `research/EFGM-EXP-0008-GOVERNED-VS-UNGOVERNED-ADAPTATION.md`.
