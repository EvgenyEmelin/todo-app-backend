from sqlalchemy import select

from app.db.session import DbSession
from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: DbSession) -> None:
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return list(self.db.scalars(select(CategoryORM)).all())

    def get_by_id(self, category_id: str) -> CategoryORM:
        return self.db.get(CategoryORM, category_id)

    def create(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name = name)
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category

    def delete(self, category: CategoryORM) -> None:
        self.db.delete(category)
        self.db.commit()

