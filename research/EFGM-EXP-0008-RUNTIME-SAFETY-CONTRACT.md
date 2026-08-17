# EFGM-EXP-0008 — Mandatory Runtime Safety & Containment Contract

## Purpose

EXP-0008 studies whether frozen EFGM signals can distinguish governed adaptation from coherent ungoverned adaptation **without creating a real-world attack, escape, persistence, privilege, credential, or network surface**.

This document is part of the EXP-0008 preregistration. It is a mandatory execution precondition, not an optional implementation note.

If an implementation choice conflicts with this contract, containment wins. Failure to satisfy the contract blocks autonomous execution and is **not** counted as an experimental result.

The machine-readable companion is:

`experiments/manifests/EFGM-EXP-0008-safety.yaml`

## Core safety invariant

> The agent must have no meaningful path from the synthetic experimental world into a real computing environment.

The experiment may simulate authorization, credentials, connectivity, persistence, privileges, peers, denied actions, capability growth, and policy violations. Those concepts must remain fictional state-machine properties.

A class-E violation is therefore a **synthetic state transition only**. `executed=true` means that the experiment's state machine applied a fictional prohibited action. It must never mean that the agent executed a corresponding real operating-system, network, credential, privilege, persistence, exploitation, or security action.

## Threat model

EXP-0008 explicitly protects against:

- unintended network egress or discovery of a proxy/package-registry path;
- inherited GitHub, cloud, API, SSH, or host credentials;
- arbitrary shell, subprocess, interpreter, or operating-system execution;
- access to host filesystems, container/orchestrator sockets, cloud metadata, or LAN resources;
- real privilege escalation or persistence;
- real autonomous peer-to-peer escalation;
- bypass of the synthetic tool broker or deterministic policy engine;
- modification of the policy engine, watchdog, telemetry, measurement adapter, or experiment controls by the agent;
- execution on CI infrastructure that carries platform credentials or general Internet connectivity.

## Required runtime architecture

The preferred execution shape is:

```text
              MODEL
                |
                | action proposal
                v
       +---------------------+
       | strict tool broker  |
       | allowlist only      |
       +----------+----------+
                  |
                  v
       +---------------------+
       | synthetic EFGM world|
       |                     |
       | fictional resources |
       | fictional privilege |
       | fictional network   |
       | fictional memory    |
       | fictional policy    |
       | simulated peers     |
       +----------+----------+
                  |
                  v
             telemetry

NO arbitrary shell
NO subprocess execution
NO real network
NO real credentials
NO package manager
NO host filesystem
NO cloud metadata
NO external services
```

The tool broker is the only action surface visible to the agent. Every tool must be predeclared, synthetic, deterministic with respect to policy evaluation, and explicitly instrumented.

## Network boundary

Autonomous EXP-0008 trajectories must not run on a host with usable external network connectivity.

The runtime must have no usable route to:

- the public Internet;
- DNS;
- HTTP/HTTPS proxies;
- package registries;
- cloud metadata services;
- local-area-network resources;
- external services;
- production or corporate infrastructure.

The lack of network reachability must be enforced **outside the agent and outside the synthetic policy engine**. An application flag such as `network_access=false` is not sufficient containment by itself.

## GitHub Actions boundary

The existing GitHub Actions workflow may continue to perform deterministic activities such as:

- unit tests;
- scoring and benchmark execution;
- state-machine tests;
- schema and provenance validation;
- hashing;
- package build/smoke verification;
- explicitly scripted non-autonomous calibration checks.

It must **not** run:

- a free-running EXP-0008 autonomous agent;
- autonomous class-E trajectory generation;
- autonomous tool use against the GitHub runner or its operating system;
- any experiment whose safety depends on an application-level claim that the GitHub-hosted runner has no network access.

The current GitHub-hosted CI environment is therefore a test/build environment, not the EXP-0008 autonomous containment environment.

## Tool boundary

The autonomous agent must not receive access to:

- `bash`, PowerShell, or other shells;
- subprocess creation;
- arbitrary Python/interpreter execution;
- `eval`/`exec` or dynamic code loading;
- package managers;
- raw sockets;
- SSH or remote shells;
- browsers or general-purpose HTTP clients;
- Docker/container sockets;
- operating-system command execution;
- arbitrary file APIs outside synthetic state storage.

An undefined or unrecognized tool request must fail closed and terminate the trajectory rather than falling back to another execution mechanism.

## Secrets and host identity boundary

The agent runtime must contain no real:

- GitHub token;
- API key;
- cloud credential;
- SSH/private key;
- production credential;
- credential helper;
- confidential configuration;
- sensitive mounted path;
- host user home directory;
- repository write credential.

Synthetic credentials may exist only as fictional state-machine values and must not be usable anywhere outside that state machine.

## Remote model boundary

If a remote model provider is used, the agent environment must not receive the provider credential or general network access.

A separate controller may broker only the narrow operation:

```text
send model request -> receive model response
```

The provider/API credential remains outside the synthetic agent world. The broker must not become a general-purpose proxy.

An offline/local model is preferred when practical because it removes this network path entirely.

## Agent topology

Primary EXP-0008 starts with **one autonomous agent**.

The optional peer/delegation surface must initially be a deterministic simulation. A real second autonomous agent would add coordination, persistence, and escape surfaces that are unnecessary to answer the primary precursor hypothesis.

Any future real multi-agent experiment requires its own explicit preregistration and containment review.

## Immutable external watchdog

A supervisor outside agent control must enforce hard limits including:

- maximum agent actions;
- maximum model calls;
- maximum retries;
- maximum wall-clock duration;
- maximum synthetic state writes;
- maximum output size;
- maximum memory use.

The agent must not be able to modify:

- the watchdog;
- the synthetic policy engine;
- the tool broker;
- raw telemetry;
- the telemetry-to-EFGM adapter;
- safety configuration.

Any containment anomaly terminates the current trajectory **and the remaining batch**.

## Mandatory containment preflight

Before every autonomous batch, independent preflight checks must verify at minimum:

1. no external network route;
2. no DNS resolution;
3. no HTTP/HTTPS proxy;
4. no package-registry reachability;
5. no cloud-metadata reachability;
6. no LAN reachability;
7. no real secrets/tokens in the runtime environment;
8. no shell/subprocess execution capability;
9. no raw socket capability;
10. no host filesystem or external mount exposure;
11. unknown tools fail closed;
12. the agent cannot mutate policy, watchdog, telemetry, adapter, or containment settings;
13. hard execution budgets are active.

The preflight output must be recorded, versioned, and hashed.

If any check fails, **no autonomous trajectory runs**.

## Human phase gate

There is no automatic transition from scripted calibration to autonomous development.

After Phase 2, a human reviewer must explicitly confirm:

- safety-contract identity;
- environment identity;
- tool-broker identity;
- telemetry-schema identity;
- measurement-adapter identity;
- watchdog identity;
- containment-preflight evidence and hash.

Only after that approval may Phase 3 begin.

## Containment-event handling

A containment anomaly is not a useful class-E scientific trajectory and must not be counted as one.

Required response:

1. immediately terminate the trajectory;
2. stop the remaining batch;
3. preserve immutable logs;
4. record runtime/environment identities and hashes;
5. investigate the containment failure;
6. do not silently retry;
7. require a new safety review before autonomous execution resumes.

## Scientific separation

These controls deliberately separate two questions:

### Scientific question

Can frozen EFGM detect a precursor trajectory before a **synthetic** policy-boundary violation?

### Safety question

Can we run that experiment without providing the agent a real system worth escaping into?

EXP-0008 proceeds only when the answer to the second question is yes by construction and by preflight evidence.

Containment passing does not demonstrate that EFGM is safe, production-ready, or capable of containing an uncontrolled agent. It only establishes that the experimental apparatus meets the preregistered safety boundary required to run the study.
