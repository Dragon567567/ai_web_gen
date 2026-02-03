export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

export interface GeneratedCode {
  html: string;
  css: string;
  javascript: string;
}

export interface GenerateResponse {
  message: string;
  code: GeneratedCode | null;
}