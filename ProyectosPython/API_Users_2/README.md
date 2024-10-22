# API_Users_2 - Development in Progress

This API is currently under development and aims to handle user registration, email verification, authentication, and management of user roles. The API also includes a secure password recovery mechanism.

## Features

- User registration with email verification
- JWT authentication and role-based authorization (user and admin roles)
- CRUD operations for managing users
- Password recovery system via email
- Secure connection management using PostgreSQL and psycopg2

## Technologies and Frameworks

This API is built using modern and widely adopted technologies for backend development. Here’s a breakdown of the tools and technologies used:

- **Programming Language**: Python 3.8+
- **Framework**: FastAPI – A modern, fast web framework for building APIs
- **Database**: PostgreSQL – A robust, scalable relational database system
- **Database Connection**: psycopg2 – A PostgreSQL adapter for Python, managing connections efficiently using connection pools
- **Security**: JWT (JSON Web Tokens) for secure authentication and bcrypt for password hashing
- **Email Service**: SMTP for sending email verification and password recovery tokens
- **Testing**: pytest for unit tests

### Purpose

The **API_Users_2** allows the following operations:
- **User Registration**: Users can sign up with email verification.
- **User Authentication**: Users can log in with a secure JWT-based authentication system.
- **Role Management**: There are predefined roles (`R_USER`, `R_ADMIN`). Admins can modify or delete users.
- **Password Recovery**: Users can request a password reset via email.
- **User Operations**: Admins can update or delete user information, ensuring role-based access control.

## Getting Started

### Prerequisites

To run this API, you’ll need the following:

- Python 3.8+
- PostgreSQL installed and running

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/NicolasAgustinBiglieri/Proyectos.git
    cd Proyectos/ProyectosPython/API_Users_2
    ```

2. Set up a Python virtual environment and install dependencies:
    ```sh
    python -m venv .venv

    # On Linux/Mac:
    source .venv/bin/activate  
    # On Windows:
    .venv\Scripts\activate  
    
    # If your system has restrictions, use first:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    
    # Installation of dependencies:

    pip install -r requirements.txt

    If you have issues with requirements.txt, you can install the packages manually:

    pip install fastapi[all]
    pip install psycopg2
    pip install passlib
    pip install python-jose
    pip install pytest
    pip install bcrypt
    ```

3. Set up PostgreSQL:
    - Ensure PostgreSQL is running.
    - Create a database, e.g., `api_users_2`.
    - Configure the `.env` file as explained below.

4. Run the application:
    ```sh
    uvicorn main:app --reload
    ```

### Running Tests

To run the tests, use:
```sh
pytest -v
```

## User Registration and Authentication

The API uses **JWT (JSON Web Tokens)** for authentication and **role-based access control** for managing permissions across endpoints. Passwords are hashed using **bcrypt** for secure storage.

### Authentication Workflow

1. **User Registration**: Users register with their email and password.
2. **Email Verification**: A verification token is sent to the user's email. The user must confirm their account by visiting the verification link.
3. **JWT Token Generation**: After successful login, a JWT token is issued for the session, allowing access to protected endpoints.
4. **Role-Based Access**: 
    - `R_USER`: Default role with basic access.
    - `R_ADMIN`: Elevated permissions to manage users (CRUD).

## API Endpoints

Here are some key endpoints currently implemented:

### User Registration and Authentication

- **POST /register**: Register a new user.
- **POST /login**: Log in and receive a JWT token.
- **POST /forgot-password**: Request a password reset link.
- **POST /reset-password**: Reset the user's password with a valid token.

### User Management (Admin only)

- **PUT /users/{id}**: Update user information (admin access required).
- **DELETE /users/{id}**: Delete a user (admin access required).

## API Documentation

The API automatically generates documentation accessible via:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Configuration .env File

Ensure that you configure the environment variables correctly in a `.env` file. Here's an example of what the `.env` file might look like:

```sh
# Clave secreta utilizada para firmar los tokens JWT
SECRET = "your_generated_secret"
# Algoritmo utilizado para cifrar los tokens JWT
ALGORITHM = "HS256" 
# Duración en minutos de validez del token de acceso
ACCESS_TOKEN_DURATION = 1
# Correo electrónico utilizado en el servicio de envío de verificación
EMAIL_ACCOUNT= "your_email@example.com"
# Contraseña para el correo electrónico utilizado en el servicio de envío de verificación
EMAIL_PASSWORD= "your_email_password"

# Datos para la conexión a PostgreSQL
_DATABASE = "api_users_2"
_USERNAME = "your_postgres_username"
_PASSWORD = "your_postgres_password"
_DB_PORT = "5432"
_HOST = "127.0.0.1"
_MIN_CON = 1
_MAX_CON = 5
_pool = None
```

You can create a secret with the following command: 
```sh
openssl rand -hex 32
```

## Dependencies

The dependencies of the API are listed in the requirements.txt file.
