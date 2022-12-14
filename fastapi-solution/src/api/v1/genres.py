from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models import Genre, GenreDetail
from services import GenreService, cache, get_genre_service


router = APIRouter()


@router.get('/{genre_id}', response_model=GenreDetail)
@cache(6)
async def genre_details(genre_id: UUID, genre_service: GenreService = Depends(get_genre_service)) -> GenreDetail:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre


@router.get('/', response_model=list)
@cache(6)
async def genre_list(genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    genre = await genre_service.get_list()
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre
