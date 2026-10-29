from datetime import date
from pydantic import BaseModel, Field

class Registration(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$")
    age: int = Field(ge=13, le=120)
    joined: date = Field(default_factory=date.today)
    newsletter: bool = False

@app.post("/register", status_code=201)
def register(user: Registration):
    return {"welcome": user.name, "joined": user.joined}
