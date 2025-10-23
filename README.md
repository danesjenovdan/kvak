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

### Seeding Course Data

To populate the application with sample course data, run the seed command:

```bash
# Create sample courses, exercises, and materials
docker compose exec app python manage.py seed_course

# Or to clear existing data and create fresh sample data
docker compose exec app python manage.py seed_course --clear
```

This will create:
- A complete course structure with categories
- 2 sample courses (Python for Beginners & JavaScript Web Development)
- Multiple exercises with realistic content
- Course materials with various question types (multiple choice, text answers, priority ordering)

After running the seed command, you can explore the hierarchical page structure in the Wagtail admin at `/admin/pages/`.

## 💻 Development

### Automatic formatting and checks when developing

This project check python formatting in a GitHub Action on push to `main`.

#### Manually running checks

- make sure you have `black` and `isort` installed (or install from `kvak/requirements.txt` in a virtual env)
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
