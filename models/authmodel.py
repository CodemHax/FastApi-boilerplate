from pydantic import BaseModel , EmailStr


class LoginModel(BaseModel):
    username: str
    password: str


class RegisterModel(BaseModel):
    username: str
    password: str
    email: EmailStr


class TokenModel(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

