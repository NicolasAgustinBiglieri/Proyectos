# User Registration API

This API handles user registration, email verification, authentication, and CRUD operations.

## Features

- User registration with email verification
- JWT authentication and authorization
- CRUD operations for user management

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB

### Installation

1. Clone the repository:
    
    git clone https://github.com/NicolasAgustinBiglieri/Proyectos.git
    cd Proyectos
    cd ProyectosPython
    cd API_Ecommerce


2. Create a virtual environment and install dependencies:
    ```
    python -m venv .venv
    
    # On Linux/Mac:
    source venv/bin/activate  
    # On Windows:
    .\.venv\Scripts\Activate  # If your system has restrictions, use first: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
    
    pip install -r requirements.txt
    ```

3. Run the application:

    uvicorn main:app --reload


### Running Tests

To run the tests, use:

pytest -v

## Authentication and Authorization

The API uses JSON Web Tokens (JWT) to handle user authentication and authorization. When a user registers or logs in, a JWT token is generated and used to authorize subsequent requests to protected endpoints.

### Generating JWT Tokens

JWT tokens are generated using a shared secret and a specified encryption algorithm. Once a user successfully logs in, they are provided with a valid JWT token which they can include in subsequent requests.

### Authentication Requirements

Some endpoints of the API require authentication to access them.

## API Documentation

Once the server is running, you can access the API documentation in your web browser by visiting the following URL:

http://127.0.0.1:8000/docs
or
http://127.0.0.1:8000/redoc

## Configuration .env file

Make sure to configure the environment variables correctly in a .env file. There is a sample file named .env_example from which you should copy all the variables and paste them into a .env file that you need to create. Here's an example of the required environment variables and their purposes:

```
# Secret key used to sign the JWT tokens
SECRET = "133f0a525a3a26eba5d4cdc8c1d746cf5633fdd9c0b4250a9e8e2acfb14859bb"

# Algorithm used to encrypt the JWT tokens
ALGORITHM = "HS256" 

# Duration in minutes of validity of the access token
ACCESS_TOKEN_DURATION = 1

# Mail account used in the verification sending service
EMAIL_ACCOUNT= "example@mail.com"

# Password for the email used in the verification sending service
EMAIL_PASSWORD= "examplePassword"
```

You can create a secret with the following command: openssl rand -hex 32

## Dependencies

The dependencies of the API are listed in the requirements.txt file.