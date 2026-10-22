from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str
    completed: bool = False

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None