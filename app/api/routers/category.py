@app.get("/categories")
def read_categories(db: DbSession) -> list[CategoriesSchema]:
    query = db.scalars(select(CategoryORM)).all()
    return [category_to_model(category) for category in query]

@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoriesCreateSchema, db: DbSession) -> CategoriesSchema:
    new_category = CategoryORM(name = payload.name)
    db.add(new_category)
    db.commit()

    return category_to_model(new_category)

@app.patch("/categories/{category_id}")
def update_category(category_id, payload: CategoryUpdateSchema, db: DbSession) -> CategoriesSchema:
    query = db.get(CategoryORM, category_id)
    if payload.name:
        query.name = payload.name
        db.commit()
        return query
    raise HTTPException(status_code=404, detail={"detail": "Category not found"})

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id, db: DbSession):
    query = db.get(CategoryORM, category_id)
    db.delete(query)
    db.commit()