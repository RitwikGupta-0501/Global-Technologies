import re

from ninja import Schema
from pydantic import EmailStr, Field, field_validator, model_validator


class UserRegisterSchema(Schema):
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_complexity(cls, v: str):
        # Example: Enforce at least one number and one uppercase
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
