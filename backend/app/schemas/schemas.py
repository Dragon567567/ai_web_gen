from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Auth schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# Code generation schemas
class CodeGenerateRequest(BaseModel):
    prompt: str

class CodeModifyRequest(BaseModel):
    original_code: str
    feedback: str

class CodeFile(BaseModel):
    filename: str
    content: str
    folder: str = "frontend"

class CodeGenerateResponse(BaseModel):
    id: int
    prompt: str
    generated_code: str
    created_at: datetime

    class Config:
        from_attributes = True

# App schemas
class AppCreate(BaseModel):
    name: str
    description: Optional[str] = None
    code: str

class AppUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    is_published: Optional[int] = None

class AppResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    code: str
    user_id: int
    is_published: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AppListResponse(BaseModel):
    apps: List[AppResponse]
    total: int

# Deployment schemas
class DeployRequest(BaseModel):
    name: Optional[str] = None
    code: str

class DeploymentResponse(BaseModel):
    id: int
    app_name: str
    deployed_url: Optional[str]
    port: Optional[int]
    status: str = "running"
    created_at: datetime

    class Config:
        from_attributes = True

# Session schemas
class CreateSessionRequest(BaseModel):
    title: Optional[str] = None

class UpdateSessionRequest(BaseModel):
    title: Optional[str] = None

class AddMessageRequest(BaseModel):
    role: str
    content: str
    files: Optional[List[CodeFile]] = []

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    files: Optional[List[CodeFile]] = []
    created_at: datetime

class ChatSessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatSessionDetailResponse(BaseModel):
    id: int
    title: str
    messages: List[ChatMessageResponse]
    created_at: datetime
    updated_at: datetime
