# React-Python Authentication Project

This project is a web application that provides user authentication functionality using React.js for the frontend and Python for the backend. 

## Project Structure

The project is organized into two main directories: `frontend` and `backend`.

### Frontend

- **`frontend/package.json`**: Configuration file for npm, listing dependencies and scripts for the React application.
- **`frontend/public/index.html`**: The main HTML file that serves as the entry point for the React application.
- **`frontend/src/index.js`**: Entry point for the React application, rendering the App component.
- **`frontend/src/App.js`**: Defines the main App component, serving as the root component for the application.
- **`frontend/src/pages/Login.js`**: Exports a Login component that renders the login form and handles user input.
- **`frontend/src/components/AuthForm.js`**: Exports an AuthForm component that encapsulates the form logic for user authentication.
- **`frontend/src/services/auth.js`**: Contains functions for handling authentication requests, interacting with the backend API.
- **`frontend/src/styles/App.css`**: CSS styles for the App component and other components in the frontend.
- **`frontend/.env`**: Stores environment variables for the frontend application.

### Backend

- **`backend/requirements.txt`**: Lists the Python dependencies required for the backend application.
- **`backend/app/main.py`**: Entry point for the Python backend application, initializing the web server and setting up routes.
- **`backend/app/api/auth.py`**: Contains authentication-related API endpoints, including login and user management.
- **`backend/app/models/user.py`**: Defines the User model, representing the user data structure.
- **`backend/app/utils/security.py`**: Contains utility functions for handling security-related tasks.
- **`backend/.env`**: Stores environment variables for the backend application.

### Docker

- **`docker-compose.yml`**: Defines the services and configurations for running the frontend and backend applications together using Docker.
- **`.gitignore`**: Specifies files and directories to be ignored by Git.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd react-python-auth
   ```

2. **Frontend Setup**:
   - Navigate to the `frontend` directory:
     ```
     cd frontend
     ```
   - Install dependencies:
     ```
     npm install
     ```
   - Start the frontend application:
     ```
     npm start
     ```

3. **Backend Setup**:
   - Navigate to the `backend` directory:
     ```
     cd ../backend
     ```
   - Create a virtual environment and activate it:
     ```
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Start the backend application:
     ```
     python app/main.py
     ```

## Usage

- Access the frontend application at `http://localhost:3000`.
- The backend API will be available at `http://localhost:5000`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.