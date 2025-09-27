# React-Python Authentication Backend

This project is a FastAPI backend for a React application that implements user authentication. It provides endpoints for user registration, login, and other authentication-related functionalities.

## Project Structure

```
react-python-auth-backend
├── app
│   ├── main.py                # Entry point of the FastAPI application
│   ├── api
│   │   └── v1
│   │       ├── __init__.py    # Initialization file for the v1 API module
│   │       └── auth.py        # Authentication routes
│   ├── core
│   │   ├── config.py          # Configuration settings
│   │   └── security.py        # Security-related functions
│   ├── models
│   │   └── user.py            # User model
│   ├── schemas
│   │   └── auth.py            # Pydantic schemas for authentication
│   ├── crud
│   │   └── user.py            # CRUD operations for User model
│   ├── db
│   │   ├── base.py            # Database base class
│   │   └── session.py         # Database session management
│   ├── services
│   │   └── auth_service.py     # Business logic for authentication
│   └── utils
│       └── jwt.py             # JWT utility functions
├── tests
│   └── test_auth.py           # Unit tests for authentication
├── requirements.txt           # Project dependencies
├── Dockerfile                 # Docker image instructions
├── .env.example               # Example environment variables
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd react-python-auth-backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy the `.env.example` file to `.env` and update the values as needed.

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

- The API provides endpoints for user registration and login.
- You can access the API documentation at `http://localhost:8000/docs` after running the application.

## Testing

- Run the tests using:
  ```bash
  pytest tests/test_auth.py
  ```

## Docker

To build and run the application using Docker, use the following commands:

1. **Build the Docker image:**
   ```bash
   docker build -t react-python-auth-backend .
   ```

2. **Run the Docker container:**
   ```bash
   docker run -d -p 8000:8000 react-python-auth-backend
   ```

## License

This project is licensed under the MIT License. See the LICENSE file for details.