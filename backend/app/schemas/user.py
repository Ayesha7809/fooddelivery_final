from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    user_type: str

    class Config:
        orm_mode = True

