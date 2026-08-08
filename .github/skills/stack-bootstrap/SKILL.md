---
name: stack-bootstrap
description: Bootstrap the smallest VenturaVision Python project structure for the approved MVP using only declared stack needs. Use when the repository is ready to move from incubation docs to executable code. Do not use when a functional project structure already exists or the task is only product scoping.
---

# Stack bootstrap

- Read `README.md` and confirm the chosen MVP before adding dependencies.
- Add only packages required by the first executable vision path.
- Separate application code tests and sample assets.
- Keep model downloads large media and generated artifacts out of Git.
- Add one deterministic smoke test using a small licensed or synthetic fixture.
- Add a local run command and document hardware assumptions.
- Reuse the repository CI standard rather than creating duplicate quality workflows.
