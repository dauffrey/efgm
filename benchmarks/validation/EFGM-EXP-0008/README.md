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

No real credentials, external network access, vulnerabilities, sensitive data, or real exploitation tasks are permitted.

The authoritative design is `experiments/manifests/EFGM-EXP-0008.yaml` and `research/EFGM-EXP-0008-GOVERNED-VS-UNGOVERNED-ADAPTATION.md`.
