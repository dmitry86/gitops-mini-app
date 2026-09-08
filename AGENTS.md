# Project instructions

This is a learning GitOps project.

Architecture:
- frontend: nginx static app
- backend: Flask API
- database: PostgreSQL
- local development: Docker Compose
- Kubernetes packaging: Helm
- GitOps deployment: Argo CD
- ingress: Traefik
- container registry: GHCR
- CI: GitHub Actions

Rules:
- Explain proposed changes before making major architectural changes.
- Do not push to GitHub unless explicitly asked.
- Do not delete Kubernetes resources unless explicitly asked.
- Do not modify or commit secrets.
- Do not put passwords or tokens into Git.
- Prefer small, understandable changes over large refactors.
- Keep this project suitable for learning Kubernetes and GitOps concepts.
- Before modifying Helm templates, inspect chart/values.yaml and relevant templates.
- After Helm changes, validate with:
  docker run --rm -v "$PWD:/work" -w /work alpine/helm:3.17.3 template mini-app chart
- After code changes, show git diff and summarize what changed.
