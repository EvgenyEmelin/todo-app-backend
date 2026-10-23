from app.db.session import DbSession
from app.repositories.category import CategoryRepository
from app.schemas.category import (
    CategoriesCreateSchema,
    CategoriesSchema,
    CategoryUpdateSchema,
)


class CategoryNotFound(Exception):
    """""Категория не найдена в БД"""""

class CategoryService:

    def __init__(self,db: DbSession) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_category(self) -> list[CategoriesSchema]:
        category_orm = self.category_repository.get_all()
        return [CategoriesSchema.model_validate(category) for category in category_orm]

    def create_category(self, category_create: CategoriesCreateSchema) -> CategoriesSchema:
        category_orm = self.category_repository.create(name=category_create.name)
        self.db.commit()
        return CategoriesSchema.model_validate(category_orm)

    def update_category(self, category_id: str, category_update: CategoryUpdateSchema) -> CategoriesSchema:
        try:
            category_for_update = self.category_repository.get_by_id(category_id=category_id)
        except Exception:
            raise CategoryNotFound("Категория не найдена")
        if category_update.name:
                category_for_update.name = category_update.name
        self.db.commit()
        return CategoriesSchema.model_validate(category_for_update)


    def delete_category(self, category_id: str) -> None:
        try:
            category_for_delete = self.category_repository.get_by_id(category_id = category_id)
        except Exception:
            raise CategoryNotFound("Категория не найдена")

        self.category_repository.delete(category_for_delete)
        self.db.commit()
