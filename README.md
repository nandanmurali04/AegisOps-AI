# AegisOps-AI 🛡️

### Enterprise Cybersecurity Incident Management Platform

AegisOps-AI is a backend-focused cybersecurity incident management platform designed to help security teams manage, track, assign, and audit security incidents through a centralized REST API.

The project demonstrates backend engineering concepts used in security operations, including authentication, authorization, relational database management, incident lifecycle management, and audit logging.

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation and Setup](#-installation-and-setup)
- [Database Configuration](#-database-configuration)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Implementation Details](#-implementation-details)
- [Testing the API](#-testing-the-api)
- [Security Considerations](#-security-considerations)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

## 📖 Overview

Security Operations Center (SOC) teams handle incidents such as suspicious login attempts, unauthorized access, malware alerts, and other potential security threats.

Managing these incidents manually can make it difficult to maintain consistent records, control access to sensitive information, and track the actions performed by different users.

AegisOps-AI addresses these challenges by providing a structured backend for authentication, access control, incident management, assignment, and audit trails.

The application uses FastAPI to expose REST endpoints, PostgreSQL to persist application data, and SQLAlchemy to interact with the database.

## ✨ Features

### 1. User Authentication
- User registration and login endpoints.
- Password hashing instead of storing plain-text passwords.
- JWT-based authentication for protected API endpoints.
- Token-based access to authorized resources.

### 2. Role-Based Access Control (RBAC)
- Access control based on user roles.
- Authentication and authorization checks on protected endpoints.
- Separation of permissions between different categories of users.

### 3. Incident Management
- Create new security incidents.
- Retrieve incident information.
- Update existing incident records.
- Delete incidents where authorized.
- Track incident information throughout its lifecycle.

### 4. Incident Assignment
- Associate incidents with responsible users.
- Support accountability during incident handling.
- Keep assignment-related actions traceable.

### 5. Audit Logging
- Maintain records of relevant incident-related actions.
- Associate audit records with incidents and actions.
- Retrieve the audit history for an individual incident.

### 6. REST API Documentation
- Interactive Swagger UI through FastAPI.
- Request and response validation.
- OpenAPI-based API documentation.

## 🧰 Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python | Backend development |
| Web framework | FastAPI | REST API development |
| ASGI server | Uvicorn | Runs the application |
| Database | PostgreSQL | Persistent relational storage |
| ORM | SQLAlchemy | Database models and queries |
| Data validation | Pydantic | Request and response validation |
| Authentication | JSON Web Tokens (JWT) | Token-based authentication |
| Password security | bcrypt-based hashing | Protects stored passwords |
| API testing | Swagger UI | Interactive endpoint testing |
| Version control | Git and GitHub | Source control and collaboration |

## 🏗️ System Architecture

The application follows a layered backend architecture.

```text
                    Client / API Consumer
                             |
                             v
                      FastAPI REST API
                             |
                             v
                   Authentication Layer
                       JWT Validation
                             |
                             v
                 Authorization / RBAC Layer
                             |
                             v
                    Application Logic
                     /             \
                    v               v
             Incident Service    Audit Logging
                    |               |
                    v               v
                 SQLAlchemy ORM
                         |
                         v
                    PostgreSQL
```

### Request flow

1. A client sends an HTTP request to a FastAPI endpoint.
2. FastAPI validates the request data.
3. Protected endpoints verify the user's authentication token.
4. Authorization logic checks whether the user has permission to perform the operation.
5. Application logic processes the request.
6. SQLAlchemy communicates with PostgreSQL when database access is required.
7. Relevant actions are recorded in the audit log.
8. The API returns a structured HTTP response.

## 📂 Project Structure

The repository contains a backend directory. The structure below illustrates the intended organization; retain the actual filenames and modules present in your repository.

```text
AegisOps-AI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── .gitignore
├── LICENSE
└── README.md
```

### Directory responsibilities

- `api/` — API routes and endpoint definitions.
- `core/` — Shared configuration, authentication, and security utilities.
- `models/` — SQLAlchemy database models.
- `schemas/` — Pydantic request and response schemas.
- `services/` — Application logic and reusable operations.
- `main.py` — FastAPI application entry point.
- `requirements.txt` — Python dependencies.
- `.env` — Local environment configuration and secrets.

Some of these folders may not exist in the current version. Adjust this section to match the actual repository.

## 💻 Prerequisites

Install the following software before running the project:

- Python 3.11 or a compatible Python 3 version.
- PostgreSQL.
- Git.
- Visual Studio Code or another code editor.

Verify the installations:

```powershell
python --version
git --version
psql --version
```

If PostgreSQL's command-line tools are not in your system PATH, verify PostgreSQL through pgAdmin instead.

## 🚀 Installation and Setup

### Step 1: Clone the repository

Open PowerShell or the VS Code terminal.

```powershell
git clone https://github.com/nandanmurali04/AegisOps-AI.git
cd AegisOps-AI
```

### Step 2: Navigate to the backend

```powershell
cd backend
```

Confirm the available files:

```powershell
Get-ChildItem
```

If your existing application uses a different directory or entry point, use the directory containing its `requirements.txt` and FastAPI application.

### Step 3: Create a virtual environment

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
venv\Scripts\activate.bat
```

### Step 4: Install dependencies

If the project already contains `requirements.txt`, install the dependencies from that file:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If no requirements file exists, create one based on the imports and packages used by the application. Do not replace a working dependency list with a guessed one.

### Step 5: Configure PostgreSQL

Start the PostgreSQL service and open pgAdmin or a PostgreSQL terminal.

Create a database named `aegisops`:

```sql
CREATE DATABASE aegisops;
```

If your application uses a dedicated PostgreSQL user, create or configure that user and grant the required database permissions.

### Step 6: Configure environment variables

Create a `.env` file in the directory expected by your application's configuration.

Example configuration:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/aegisops
SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

These variable names are examples. Use the exact names expected by your existing configuration module and the PostgreSQL driver installed in your environment.

Never commit actual passwords, JWT secrets, or other credentials to GitHub.

### Step 7: Initialize the database schema

Use the database initialization mechanism implemented by the project.

For example, if the application uses SQLAlchemy's `Base.metadata.create_all()` during startup, ensure that all required models are imported before table creation.

If the project uses Alembic migrations, apply the existing migrations instead:

```powershell
alembic upgrade head
```

Do not run both approaches blindly; follow the initialization method actually implemented in the codebase.

### Step 8: Start the FastAPI server

If the FastAPI application is defined in `app/main.py`, run:

```powershell
uvicorn app.main:app --reload
```

If the entry point is `main.py` in the current directory, use:

```powershell
uvicorn main:app --reload
```

The `--reload` option automatically restarts the development server when Python source files change.

A successful startup should show that Uvicorn is listening on:

```text
http://127.0.0.1:8000
```

## 📚 API Documentation

Once the server is running, open the interactive API documentation.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **OpenAPI schema:** http://127.0.0.1:8000/openapi.json

These URLs work when the application uses FastAPI's default documentation settings.

Use Swagger UI to inspect the actual registered endpoints, required parameters, request schemas, and response codes.

## 🔐 Implementation Details

### 1. Authentication and Password Hashing

The authentication module supports user registration and login.

During registration:
1. The application validates the submitted user information.
2. The password is hashed using the configured password-hashing implementation.
3. The user record is stored in PostgreSQL.

During login:
1. The submitted credentials are checked against the stored user record.
2. The submitted password is verified against the stored hash.
3. If authentication succeeds, the application issues a JWT access token.

The original password should never be stored in the database.

### 2. JWT Authentication

JSON Web Tokens allow a client to present a signed token when accessing protected endpoints.

A typical request uses the following header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

The backend validates the token and identifies the authenticated user before allowing access to protected resources.

JWTs are signed tokens, not encrypted containers. Avoid placing sensitive information in their payloads.

### 3. Role-Based Access Control

RBAC restricts actions according to a user's assigned role and permissions.

The authorization layer checks whether the authenticated user is allowed to perform the requested operation.

For example, an incident management platform may distinguish between administrators, analysts, and read-only users. The actual roles and permissions must match those implemented in the project.

### 4. Incident Lifecycle Management

Incident records represent security events that require investigation or resolution.

Typical incident attributes include:

- Incident identifier.
- Title and description.
- Severity.
- Status.
- Assignment information.
- Creation and update timestamps.

The API provides CRUD operations: Create, Read, Update, and Delete.

The exact fields and permitted status transitions depend on the existing SQLAlchemy models and API schemas.

### 5. Incident Assignment

Incident assignment associates an incident with a responsible user.

This helps security teams track ownership and coordinate investigations. The backend should validate referenced user IDs and enforce the appropriate permissions before changing assignments.

### 6. Audit Logging

Audit logs provide a history of relevant operations performed on incidents.

The application includes an audit-log table and an endpoint for retrieving logs associated with a particular incident.

Example endpoint pattern:

```http
GET /incidents/{incident_id}/logs
```

The endpoint should be tested against the running application to confirm its registered route and authorization requirements.

Audit records support accountability and help investigators understand how incident records have changed over time.

## 🧪 Testing the API

### Step 1: Start the application

Run the appropriate Uvicorn command from the backend directory.

### Step 2: Open Swagger UI

Navigate to:

http://127.0.0.1:8000/docs

### Step 3: Test user registration

Find the registered user registration endpoint and submit the required request body.

Confirm that the application returns the expected response and that the user record is stored in PostgreSQL.

### Step 4: Test login

Use the registered credentials with the login endpoint.

Confirm that the application returns an access token when authentication succeeds.

### Step 5: Test protected endpoints

Use Swagger UI's **Authorize** feature if the application exposes a compatible bearer-token security scheme.

Enter the token in the format requested by the interface and call a protected endpoint.

Verify that unauthorized requests are rejected.

### Step 6: Test incident management

Test the implemented operations for:

- Creating an incident.
- Retrieving incidents.
- Updating an incident.
- Deleting an incident, if supported for the authenticated user.
- Assigning an incident.
- Retrieving the incident's audit history.

### Step 7: Verify database persistence

Open PostgreSQL and inspect the relevant tables to confirm that changes are persisted.

### Step 8: Test authorization boundaries

Where multiple roles are implemented, test that users cannot perform operations outside their assigned permissions.

Record unexpected responses and correct the implementation before deployment.

## 🔒 Security Considerations

- Store credentials and secrets in environment variables.
- Never commit `.env` files containing real credentials.
- Hash passwords using a suitable password-hashing algorithm.
- Validate JWT signatures, expiration, and required claims.
- Apply authorization checks to all protected operations.
- Validate user-supplied input.
- Use parameterized ORM operations rather than unsafe SQL string construction.
- Protect audit logs against unauthorized modification.
- Use HTTPS and production-grade secret management when deploying.
- Avoid exposing stack traces and internal configuration to API clients.

## 🛠️ Troubleshooting

### Database connection error

Check that PostgreSQL is running, the database exists, and the configured username, password, host, port, and database name are correct.

### Module not found

Activate the virtual environment and install the project's dependencies:

```powershell
pip install -r requirements.txt
```

### Import error when starting Uvicorn

Run the command from the correct directory and use the module path that matches the actual location of the FastAPI application.

### Authentication failure

Check the login request schema, password-verification logic, JWT secret, token expiration, and authorization header.

### Database tables are missing

Verify that the application's models are imported and that its schema initialization or migration procedure has been executed successfully.

### Port 8000 is already in use

Run the development server on another port:

```powershell
uvicorn app.main:app --reload --port 8001
```

If your entry point differs, replace `app.main:app` with the correct module path.

## 🗺️ Future Enhancements

Potential improvements include:

- Security incident analytics dashboard.
- Advanced filtering and search.
- Incident severity and SLA tracking.
- Notifications and escalation workflows.
- Automated security-event ingestion.
- Integration with SIEM tools.
- Containerization using Docker.
- Automated unit and integration tests.
- Production deployment and monitoring.

These are proposed enhancements, not claims that every feature is currently implemented.

## 👨‍💻 Author

**Nandan Murali Nair**

B.Tech — Computer Science and Engineering (Artificial Intelligence)

GitHub: [@nandanmurali04](https://github.com/nandanmurali04)

## 📄 License

This repository includes an MIT license. Refer to the [LICENSE](LICENSE) file for the applicable terms.

---

**AegisOps-AI** — Building a structured, auditable foundation for cybersecurity incident management.
