import axios from 'axios';
import type { GenerateResponse } from '../types';

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const generateCode = async (prompt: string): Promise<GenerateResponse> => {
  try {
    const response = await api.post<GenerateResponse>('/generate', {
      prompt,
      messages: []
    });
    return response.data;
  } catch (error) {
    console.error('API调用失败:', error);
    throw error;
  }
};