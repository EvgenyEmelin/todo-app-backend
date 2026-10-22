from pydantic import BaseModel


class CategoriesSchema(BaseModel):
    id: str
    name: str

class CategoriesCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(CategoriesCreateSchema):
    pass