from pydantic import BaseModel, ConfigDict


class CategoriesSchema(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True) 

class CategoriesCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(CategoriesCreateSchema):
    pass