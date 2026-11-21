
from fastapi import APIRouter
from typing import Optional

from backend.services.catalogue_service import (
    get_all_programs,
    search_programs
)

router = APIRouter(
    prefix="/programs",
    tags=["Catalogue des formations"]
)


@router.get("/")
def list_programs():
    return get_all_programs()


@router.get("/search")
def find_programs(
    query: Optional[str] = None,
    city: Optional[str] = None
):
    return search_programs(query=query, city=city)
