from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_category_service
from app.schemas.category import (
    CategoriesCreateSchema,
    CategoriesSchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryNotFound, CategoryService

router_category = APIRouter(prefix="/categories")


@router_category.get("")
def read_categories(category_service: CategoryService = Depends(get_category_service)) -> list[CategoriesSchema]:
    return category_service.list_category()

@router_category.post("", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoriesCreateSchema, category_service: CategoryService = Depends(get_category_service)) -> CategoriesSchema:
    return category_service.create_category(category_create=payload)


@router_category.patch("/{category_id}")
def update_category(category_id,
                    payload: CategoryUpdateSchema, 
                    category_service: CategoryService = Depends(get_category_service)
                    ) -> CategoriesSchema:
    try:
        return category_service.update_category(category_id=category_id, category_update=payload)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router_category.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id, category_service: CategoryService = Depends(get_category_service)):
    try:
        category_service.delete_category(category_id=category_id)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e