# Patient Encounter System

A backend REST API built using **FastAPI** and **SQLAlchemy** to manage patients, doctors, and appointments in a healthcare system.

This project uses **a single MySQL database** for both application runtime and automated testing.  
All test cases are designed to **clean up any data they create**, ensuring database consistency.

---

## Table of Contents

- Overview
- Tech Stack
- Features
- Database Strategy
- Project Structure
- Setup Instructions
- Environment Variables
- Database Initialization
- Running the Application
- Running Tests
- Test Coverage
- CI/CD Pipeline
- Security & Code Quality
- API Endpoints

---

## Overview

The Patient Encounter System provides APIs to:

- Manage patients and doctors
- Schedule appointments with strict business rules
- Prevent data corruption using validation and constraints
- Ensure production-ready quality using automated tests and CI/CD

---

## Tech Stack

- **Python** ≥ 3.10
- **FastAPI**
- **SQLAlchemy 2.0**
- **MySQL** (single database for app + tests)
- **Poetry** (dependency management)
- **Pytest + pytest-cov**
- **Ruff**
- **Black**
- **Bandit**
- **GitHub Actions**

---

## Features

### Patient Management

- Create, read, list, and delete patients
- Unique email enforcement
- Prevent deletion if appointments exist

### Doctor Management

- Create, read, list, and delete doctors
- Activate / deactivate doctors
- Prevent deletion if appointments exist

### Appointment Management

- Create appointments
- Prevent overlapping appointments for doctors
- Prevent appointments for inactive doctors
- Prevent appointments in the past
- List and delete appointments

---

## Database Strategy

- **Only ONE database is used (MySQL)**
- No SQLite or mock databases are used
- Same database URL is used for:
  - Application runtime
  - Automated tests
- All tests:
  - Create required data explicitly
  - Delete test data after execution
  - Do not leave residual records

This approach ensures:

- Realistic testing against production-like data
- No schema mismatch between test and runtime environments

---

## Project Structure

```text
patient-encounter-system/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── src/
│   └── patient_encounter_system/
│       ├── models/
│       │   ├── appointment.py
│       │   ├── doctor.py
│       │   └── patient.py
│       ├── schemas/
│       │   ├── appointment_pydantic.py
│       │   ├── doctor_pydantic.py
│       │   └── patient_pydantic.py
│       ├── services/
│       │   ├── appointment_service.py
│       │   ├── doctor_service.py
│       │   └── patient_service.py
│       ├── database.py
│       ├── main.py
│       ├── create_tables.py
│       └── delete_my_tables.py
│
├── tests/
│   ├── test_patients.py
│   ├── test_doctors.py
│   └── test_appointments.py
│
├── pyproject.toml
├── README.md
├── .env
└── .gitignore
```

## Setup Instructions

### 1. Clone the Repository

    git clone https://github.com/<your-username>/patient-encounter-system.git
    cd patient-encounter-system

### 2. Install Poetry

    pip install poetry

### 3. Install Dependencies

    poetry install

## Environment Variables

Create a .env file or set environment variables:

    DATABASE_URL=mysql+pymysql://username:password@localhost:3306/patient_db

This same variable is used for:
Local development
Automated tests
CI pipeline
Database Initialization

### Create database tables:

    poetry run python -m patient_encounter_system.create_tables

### Delete all tables (if required):

    poetry run python -m patient_encounter_system.delete_my_tables

### Running the Application

    poetry run uvicorn patient_encounter_system.main:app --reload

### Application URL:

    http://127.0.0.1:8000

### Swagger UI:

    http://127.0.0.1:8000/docs

## Running Tests

### Run all tests:

    poetry run pytest

### Run a specific test file:

    poetry run pytest tests/test_patients.py

### Run a single test case:

    poetry run pytest tests/test_patients.py::test_create_patient_success

All tests automatically clean up any data they create.

## Test Coverage

### Run tests with coverage:

    poetry run pytest --cov=src --cov-report=term-missing

### Minimum required coverage:

    80%

### Current coverage:

    88%

## CI/CD Pipeline

--GitHub Actions pipeline includes:

--Dependency installation using Poetry

--Ruff linting

--Black formatting checks

--Bandit security scanning

--Pytest with coverage enforcement

--Build validation

--Pipeline triggers:

--Push to main

--Pull requests to main

--Database credentials are securely injected using GitHub Environment Secrets.

--Security & Code Quality

--Ruff – Static code analysis

--Black – Code formatting enforcement

--Bandit – Security vulnerability scanning

--pip-audit – Dependency vulnerability auditing

## API Endpoints

### Patients

    POST /patients

    GET /patients

    GET /patients/{id}

    DELETE /patients/{id}

### Doctors

    POST /doctors

    GET /doctors

    GET /doctors/{id}

    PUT /doctors/{id}/toggle-status

    DELETE /doctors/{id}

### Appointments

    POST /appointments

    GET /appointments

    GET /appointments/{id}

    DELETE /appointments/{id}
