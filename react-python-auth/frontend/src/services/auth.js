import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/auth/';

export const login = async (credentials) => {
    try {
        const response = await axios.post(`${API_URL}login`, credentials);
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error('Login failed');
    }
};

export const logout = async () => {
    try {
        await axios.post(`${API_URL}logout`);
    } catch (error) {
        throw error.response ? error.response.data : new Error('Logout failed');
    }
};