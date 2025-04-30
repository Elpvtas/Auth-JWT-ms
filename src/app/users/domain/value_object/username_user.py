from pydantic import BaseModel, Field, field_validator

class UsernameUser(BaseModel):
    value: str = Field(..., description="Username")

    @field_validator("value")
    def validate_username(cls, v):
        if not v.strip():
            raise ValueError("Username cannot be empty.")
        if len(v) > 50:
            raise ValueError("Username must not exceed 50 characters.")
        return v

    def __eq__(self, other):
        return isinstance(other, UsernameUser) and self.value == other.value

    def __str__(self):
        return self.value
