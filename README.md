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

## 💻 Development

### Automatic formatting and checks when developing

This project check python formatting in a GitHub Action on push to `main`.

#### Manually running checks

- make sure you have `black` and `isort` installed (or install from requirements.txt in a virtual env)
- run `./check_formatting.sh` to run the checks
- you can run `./check_formatting.sh --fix` to automatically format files

#### Format on save in VSCode

- open the `code kvak.code-workspace` instead of the root directory (`code .`)
- install the recommended extensions
  - there should be a prompt to install recommended extensions or
  - open the command palette and type `Show Recommended Extensions`
- automatic format on save should now work

### Updating requirements using `pur`

- Setup a python virtual env with the same python version as the docker container
- run `pur -r requirements.txt` to update the file with all dependencies at their latest versions
- run `pip install -r requirements.txt` to install the new versions from the file
  - if there are conflicting dependencies, check the output and selectively downgrade specific dependencies to earlier versions until it successfully installs
- When it all succeeds rebuild the docker container and test the app
