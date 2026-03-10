# Fiche — docker

---

## Session — 2026-03-06
Docker fundamentals: images, containers, Dockerfile, and practical use in a CI/CD pipeline

### Image
A deterministic, read-only recipe listing all steps needed to run an application: OS, runtime, dependencies, source code, environment variables, and server. Because these steps are deterministic, Docker can capture them as a reusable artifact.

### Container
A running (or ready-to-run) instance of an image. The image is the recipe; the container is the dish.

### Daemon
The background process (Docker Engine) that manages containers. The Docker client sends commands to the daemon.

### Registry
A storage and distribution system for images. Can be public (Docker Hub) or private (e.g. Google Artifact Registry).

### Dockerfile placement
When a project contains a single image, the Dockerfile is placed at the root of the repository.

### Idempotence requirement
The containerized application must be stateless and idempotent — it must be able to restart from scratch without retaining local state, so it behaves consistently across deployments.

### Port
A numbered network entry point on a machine. A single IP address can host many services simultaneously because each one listens on a different port number. When a process declares a port (e.g. Flask on 8080), it means it accepts incoming network requests at that number. `EXPOSE` in a Dockerfile signals which port the container listens on. Services that use outbound polling (e.g. a Telegram bot) do not need to expose a port.

### Resource sharing and isolation
Containers running on the same host share the underlying OS kernel and hardware resources while remaining isolated from each other, which makes Docker an optimization tool as well as a packaging tool.

---

## Session — 2026-03-09
Docker concepts introduced in the context of containerising a Python/Poetry project

### Port
A numbered network entry point on a machine. A single IP address can host many services simultaneously, each listening on a distinct port number. When a process declares a port (e.g. `app.run(port=8080)`), it signals which numbered door incoming requests should target.

### EXPOSE instruction
`EXPOSE <port>` in a Dockerfile declares which port the container listens on, enabling Docker and orchestrators to route traffic to it. Services that only make outbound requests (e.g. a polling bot) do not need `EXPOSE`.

### Polling vs listening services
A service that polls an external API (e.g. a Telegram bot using long-polling) makes outbound requests on a schedule and never receives inbound connections, so it requires no exposed port. A web server (Flask, FastAPI) receives inbound HTTP requests and must expose a port.

### Poetry-based Dockerfile pattern
To install dependencies from `pyproject.toml` in a container: install Poetry inside the image first, then run `poetry install` to resolve and install all dependency groups. This avoids maintaining a separate `requirements.txt`.
