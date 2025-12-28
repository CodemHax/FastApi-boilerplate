# FastAPI Project

A boilerplate FastAPI application with essential features for building modern web APIs.

## Features

- **FastAPI Framework**: High-performance, easy-to-use web framework for building APIs with Python 3.7+.
- **Automatic API Documentation**: Interactive Swagger UI and ReDoc documentation generated automatically.
- **Dependency Injection**: Built-in support for dependency injection to manage app components.
- **Async Support**: Asynchronous request handling for better performance.
- **Pydantic Models**: Data validation and serialization using Pydantic.
- **CORS Support**: Cross-Origin Resource Sharing enabled for web clients.
- **Environment Configuration**: Support for environment variables and settings management.
- **Testing**: Basic setup for unit and integration tests using pytest.
- **Docker Support**: Optional Docker configuration for containerization.
- **User Authentication**: Registration and login with username/email and password.
- **JWT Tokens**: Access and refresh token-based authentication using Jose library.
- **Password Security**: Secure password hashing and verification using bcrypt.
- **MongoDB Integration**: Asynchronous user data storage with Motor.
- **Redis Caching**: User profile caching for improved performance.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-fastapi-project.git
   cd your-fastapi-project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser and go to `http://127.0.0.1:8000/docs` for the Swagger UI documentation.

## API Endpoints

- `POST /auth/register`: Register a new user with username, password, and email.
- `POST /auth/login`: Authenticate user and return access and refresh tokens.
- `GET /auth/profile`: Retrieve authenticated user's profile (requires JWT token).
- `POST /auth/refresh`: Refresh access token using refresh token.

## Testing

Run tests with:
```bash
pytest
```

## Deployment

For production, use a server like Gunicorn with Uvicorn workers:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

## License

This project is licensed under the MIT License.
