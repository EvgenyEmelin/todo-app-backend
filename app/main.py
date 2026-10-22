from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.db.session import engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_origins=["http://localhost:3000"],
    allow_headers=["*"])


def task_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

def category_to_model(category_orm: CategoryORM) -> CategoriesSchema:
    return CategoriesSchema(id = category_orm.id, name=category_orm.name)

@app.get("/tasks")
def read_tasks(db: DbSession) -> list[TaskSchema]:
    query = db.scalars(select(TaskORM)).all()
    return [task_to_model(task) for task in query]

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: DbSession) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed = payload.completed)
    db.add(new_task)
    db.commit()

    return task_to_model(new_task)

@app.patch("/tasks/{task_id}")
def update_task(task_id, payload: TaskUpdateSchema, db: DbSession) -> TaskSchema:
    query = db.get(TaskORM, task_id)
    if payload.title:
        query.title = payload.title
    if payload.completed is not None:
        query.completed = payload.completed
    db.commit()

    return query

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id, db: DbSession) -> None:
    query = db.get(TaskORM, task_id)
    db.delete(query)
    db.commit()



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
