import React, { useState } from 'react';
import AuthForm from '../components/AuthForm';
import { login } from '../services/auth';

const Login = () => {
    const [error, setError] = useState(null);

    const handleLogin = async (credentials) => {
        try {
            await login(credentials);
            // Redirect or perform additional actions on successful login
        } catch (err) {
            setError('Invalid username or password');
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            {error && <p className="error">{error}</p>}
            <AuthForm onSubmit={handleLogin} />
        </div>
    );
};

export default Login;