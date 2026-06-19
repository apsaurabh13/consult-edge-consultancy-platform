from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class RegisterRequest(BaseModel):
    first_name: str = Field(
        min_length=2,
        max_length=100
    )

    last_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    phone: str = Field(
        min_length=10,
        max_length=20
    )

    password: str = Field(
        min_length=8
    )