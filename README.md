# ACEest Fitness & Gym — DevOps Assignment 1

## 1. Project Overview

ACEest Fitness & Gym is a fitness-management application developed as part of the DevOps Assignment 1. The project demonstrates a complete development and CI workflow using Git/GitHub, Pytest, Docker, Jenkins, and GitHub Actions.

The supplied ACEest baseline application was a desktop Tkinter application. For this assignment, the core fitness-program and calorie-estimation concepts were adapted into a lightweight Flask web application so that the application can be tested, containerized, and integrated with CI tools.

The project focuses on:

- Fitness program management
- Calorie estimation
- Client profile validation
- Automated testing
- Code linting and syntax validation
- Docker containerization
- Jenkins BUILD pipeline
- GitHub Actions CI workflow
- Git-based development with meaningful commits and branching

---

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Application development |
| Flask | Web/API application |
| Pytest | Automated unit and API testing |
| Flake8 | Python linting |
| Docker | Application containerization |
| Gunicorn | Production WSGI server inside Docker |
| Jenkins | BUILD/CI pipeline |
| GitHub Actions | Automated CI workflow |
| Git/GitHub | Version control and source repository |

---

## 3. Project Structure

```text
ACEest-Fitness-DevOps/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .flake8
├── Jenkinsfile
├── README.md
│
├── tests/
│   ├── __init__.py
│   └── test_app.py
│
└── .github/
    └── workflows/
        └── main.yml
```

### Important files

- `app.py` — Flask application and fitness business logic
- `tests/test_app.py` — automated Pytest test suite
- `requirements.txt` — Python dependencies
- `Dockerfile` — Docker image definition
- `Jenkinsfile` — Jenkins pipeline
- `.github/workflows/main.yml` — GitHub Actions workflow
- `README.md` — project documentation

---

## 4. Application Features

The application provides the following REST endpoints.

### Home

```http
GET /
```

Returns application name, status, and version.

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "UP"
}
```

### List Fitness Programs

```http
GET /programs
```

The application currently provides:

- Fat Loss
- Muscle Gain
- Beginner

Each program contains a description, calorie factor, and workout list.

### Get One Program

```http
GET /programs/<program_name>
```

Example:

```bash
curl http://127.0.0.1:5000/programs/Fat%20Loss
```

### Calculate Estimated Calories

```http
POST /calculate-calories
```

Example:

```bash
curl -X POST http://127.0.0.1:5000/calculate-calories \
  -H "Content-Type: application/json" \
  -d '{"weight":70,"program":"Fat Loss"}'
```

Example response:

```json
{
  "calories": 1540,
  "program": "Fat Loss",
  "weight": 70.0
}
```

### Validate Client Profile

```http
POST /clients
```

Example:

```bash
curl -X POST http://127.0.0.1:5000/clients \
  -H "Content-Type: application/json" \
  -d '{"name":"John","age":25,"weight":70,"program":"Fat Loss"}'
```

The endpoint validates the client information and returns the estimated calories for the selected program.

---

# 5. Local Development

## Prerequisites

Install the following before running the application:

- Python 3.12 or later
- Git
- Docker Desktop
- GitHub account
- Jenkins installation/agent for the Jenkins stage

## Clone the repository

```bash
git clone https://github.com/2025tm93169/ACEest-Fitness-DevOps.git
cd ACEest-Fitness-DevOps
```

## Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the application

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

# 6. Manual Testing

After starting the application, the following checks can be performed.

### Check application

```bash
curl http://127.0.0.1:5000/
```

### Check health

```bash
curl http://127.0.0.1:5000/health
```

### List programs

```bash
curl http://127.0.0.1:5000/programs
```

### Check a specific program

```bash
curl http://127.0.0.1:5000/programs/Fat%20Loss
```

### Calculate calories

```bash
curl -X POST http://127.0.0.1:5000/calculate-calories \
  -H "Content-Type: application/json" \
  -d '{"weight":70,"program":"Fat Loss"}'
```

### Validate a client

```bash
curl -X POST http://127.0.0.1:5000/clients \
  -H "Content-Type: application/json" \
  -d '{"name":"John","age":25,"weight":70,"program":"Fat Loss"}'
```

Invalid input can also be tested, for example an unknown program or a negative weight.

---

# 7. Automated Testing with Pytest

The automated test suite is located at:

```text
tests/test_app.py
```

Run all tests:

```bash
pytest -q
```

The test suite covers:

- Home endpoint
- Health endpoint
- Program listing
- Existing program lookup
- Missing/invalid program handling
- Calorie calculation
- Invalid weight handling
- Calorie API validation
- Client creation/validation
- Missing client fields
- Invalid client program

## Syntax validation

```bash
python -m compileall -q app.py tests
```

## Linting

```bash
flake8 app.py tests
```

The `.flake8` configuration is included in the repository to keep linting consistent locally and in CI.

---

# 8. Docker Containerization

## Build the Docker image

```bash
docker build -t aceest-fitness .
```

## Run the container

```bash
docker run --rm -p 5000:5000 aceest-fitness
```

The application can then be accessed at:

```text
http://127.0.0.1:5000
```

Check the containerized health endpoint:

```bash
curl http://127.0.0.1:5000/health
```

## Run tests inside the container

The test suite is included in the Docker image so that the same containerized environment can execute the automated tests.

```bash
docker run --rm \
  --entrypoint python \
  aceest-fitness \
  -m pytest -q
```

The Docker image runs the application using Gunicorn and a non-root `appuser` for better container security.

---

# 9. Jenkins BUILD Pipeline

The Jenkins configuration is stored in:

```text
Jenkinsfile
```

The pipeline performs the following stages:

```text
Checkout
   ↓
Install Dependencies
   ↓
Build & Lint
   ↓
Run Tests
   ↓
Build Docker Image
```

## Jenkins setup

1. Open Jenkins.
2. Create a new Pipeline job.
3. Configure the job to use the GitHub repository.
4. Select `Jenkinsfile` from the repository.
5. Run the pipeline.
6. Verify that all stages complete successfully.

The Jenkins agent used for the Docker stage must have Docker installed and permission to execute Docker commands.

---

# 10. GitHub Actions CI

The GitHub Actions workflow is located at:

```text
.github/workflows/main.yml
```

The workflow is triggered on:

- Every `push`
- Every `pull_request`

The workflow performs three main activities required by the assignment.

## Build & Lint

- Checks out the repository
- Sets up Python
- Installs dependencies
- Checks Python syntax
- Runs Flake8
- Runs Pytest

## Docker Image Assembly

The workflow builds the Docker image from the `Dockerfile`.

## Automated Testing

The workflow executes the Pytest suite inside the built Docker image.

The Docker stage depends on the application build/lint/test stage passing first.

---

# 11. Git and GitHub Workflow

The repository uses meaningful commits to demonstrate incremental development rather than committing the entire final project as one change.

The development history is organized around the assignment phases.

Recommended commit history:

```text
Initialise ACEest Flask project
        ↓
Add ACEest fitness program endpoints
        ↓
Add calorie estimation and client validation
        ↓
Add pytest coverage for fitness API
        ↓
Containerize ACEest application with Docker
        ↓
Add Jenkins CI pipeline
        ↓
Add GitHub Actions build and test workflow
        ↓
Document setup and development workflow
```

A feature branch is also used for the Docker test-suite improvement:

```text
main
  │
  ├── feature/docker-test-suite
  │       │
  │       └── Include test suite in Docker image
  │
  └── Merge Docker test suite improvement
```

This demonstrates both incremental commits and branch-based development.

---

# 12. Development / DevOps Flow

```text
                 Developer
                     │
                     ▼
                Git / GitHub
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
   GitHub Actions            Jenkins
          │                     │
          ▼                     ▼
   Build & Syntax          Build & Lint
          │                     │
          ▼                     ▼
       Flake8                Pytest
          │                     │
          ▼                     ▼
       Pytest              Docker Build
          │                     │
          ▼                     │
    Docker Build               │
          │                     │
          ▼                     ▼
   Container Tests        BUILD Result
```

---

# 13. Assignment Requirement Mapping

| Requirement | Project Implementation |
|---|---|
| Flask web application | `app.py` |
| Git/GitHub repository | Git repository + GitHub |
| Meaningful commits | Incremental Git history |
| Branch management | `feature/docker-test-suite` |
| Unit testing | `tests/test_app.py` with Pytest |
| Build/syntax validation | `compileall` |
| Linting | Flake8 |
| Docker container | `Dockerfile` |
| Jenkins BUILD environment | `Jenkinsfile` |
| GitHub Actions | `.github/workflows/main.yml` |
| Documentation | `README.md` |

---

# 14. Conclusion

This project demonstrates the DevOps lifecycle for the ACEest Fitness & Gym application by combining application development, version control, automated testing, containerization, Jenkins automation, and GitHub Actions CI.

The implementation is intentionally lightweight so that the focus remains on the DevOps practices required by the assignment while still providing functional fitness-management APIs.
