# Kvak

**Kvak** is a Dockerized application

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed
- [Docker Compose](https://docs.docker.com/compose/) installed (if not included with Docker)

### Running the Project

To start the application, simply run:

```bash
docker compose up
```

---

### Updating requirements using `pur`

- Setup a python virtual env with the same python version as the docker container

- run `pur -r requirements.txt` to update the file with all dependencies at their latest versions

- run `pip install -r requirements.txt` to install the new versions from the file
  - if there are conflicting dependencies, check the output and selectively downgrade specific dependencies to earlier versions until it successfully installs

- When it all succeeds rebuild the docker container and test the app
