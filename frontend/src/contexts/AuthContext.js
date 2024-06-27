import React, { createContext, useState, useContext, useEffect } from 'react';
import { getCurrentUser, login as apiLogin } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const response = await getCurrentUser();
      setUser(response.data);
      console.log('User data:', response.data);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    const response = await apiLogin(credentials);
    console.log('Login response in AuthContext:', response); // 添加这行
    if (response.access_token) {
      localStorage.setItem('token', response.access_token);
      await fetchUser();
    } else {
      throw new Error('No access token received');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const hasRole = (roleName) => {
    return user?.roles?.some(role => role.name.toLowerCase() === roleName.toLowerCase());
  };

  const value = {
    user,
    login,
    logout,
    isAuthenticated: !!user,
    isAdmin: hasRole('Admin'),
    hasRole
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}