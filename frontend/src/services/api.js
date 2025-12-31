import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8001';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth
export const register = (userData) => api.post('/auth/register', userData);
export const login = (credentials) => api.post('/auth/login', credentials);
export const logout = () => api.post('/auth/logout');
export const getCurrentUser = () => api.get('/auth/me');
export const refreshToken = () => api.post('/auth/refresh');
export const getUserStats = (userId) => api.get(`/auth/stats/${userId}`);
export const getMyStats = () => api.get('/auth/me/stats');

// Moments
export const createMoment = (momentData) => api.post('/moments', momentData);
export const getMomentsFeed = (skip = 0, limit = 20) => 
  api.get(`/moments/feed?skip=${skip}&limit=${limit}`);
export const getMoment = (momentId) => api.get(`/moments/${momentId}`);
export const getUserMoments = (userId, skip = 0, limit = 20) => 
  api.get(`/moments/user/${userId}?skip=${skip}&limit=${limit}`);
export const deleteMoment = (momentId) => api.delete(`/moments/${momentId}`);
export const searchMoments = (query, skip = 0, limit = 20) => 
  api.get(`/moments/search?q=${query}&skip=${skip}&limit=${limit}`);

// Likes
export const toggleLike = (momentId) => api.post(`/likes/${momentId}`);
export const getLikesCount = (momentId) => api.get(`/likes/${momentId}/count`);
export const checkLikeStatus = (momentId) => api.get(`/likes/${momentId}/check`);

// Comments
export const createComment = (momentId, commentData) => 
  api.post(`/comments/${momentId}`, commentData);
export const getComments = (momentId, skip = 0, limit = 50) => 
  api.get(`/comments/${momentId}?skip=${skip}&limit=${limit}`);
export const deleteComment = (commentId) => api.delete(`/comments/${commentId}`);

export default api;