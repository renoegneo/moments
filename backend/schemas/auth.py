from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    token_type: str = "bearer"

class RegisterRequest(LoginRequest):
    fingerprint: str

class RegisterResponse(BaseModel):
    status: str
    details: str


