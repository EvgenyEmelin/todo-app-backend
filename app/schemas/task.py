from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

    model_config = ConfigDict(from_attributes= True)

class TaskCreateSchema(BaseModel):
    title: str
    completed: bool = False

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None