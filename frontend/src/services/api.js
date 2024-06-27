// src/services/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});


export const login = async (credentials) => {
  const response = await api.post('/token', credentials, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
  console.log('Login response:', response); // 添加这行来查看完整的响应
  return response.data;
};

export const getPosts = () => api.get('/posts');
export const createPost = (postData) => api.post('/posts', postData);
export const getPostById = (id) => api.get(`/posts/${id}`);
export const getCurrentUser = () => api.get('/users/me');
export const updateCurrentUser = (userData) => api.put('/users/me', userData);

// User management
export const getUsers = () => api.get('/admin/users');
export const updateUserRoles = (userId, roles) => api.put(`/admin/users/${userId}/roles`, { roles });

// Role management
export const getRoles = () => api.get('/admin/roles');
export const createRole = (roleData) => api.post('/admin/roles', roleData);
export const updateRole = (roleId, roleData) => api.put(`/admin/roles/${roleId}`, roleData);
export const deleteRole = (roleId) => api.delete(`/admin/roles/${roleId}`);

// Permission management
export const getPermissions = () => api.get('/admin/permissions');
export const createPermission = (permissionData) => api.post('/admin/permissions', permissionData);
export const updatePermission = (permissionId, permissionData) => api.put(`/admin/permissions/${permissionId}`, permissionData);
export const deletePermission = (permissionId) => api.delete(`/admin/permissions/${permissionId}`);



export default api;