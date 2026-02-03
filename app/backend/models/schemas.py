from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class GenerateRequest(BaseModel):
    prompt: str
    messages: Optional[List[Message]] = []

class GeneratedCode(BaseModel):
    html: str
    css: str
    javascript: str

class GenerateResponse(BaseModel):
    message: str
    code: Optional[GeneratedCode] = None