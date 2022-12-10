from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models import Genre
from services import GenreService, get_genre_service

router = APIRouter()


class GenreAPI(Genre):
    pass


@router.get('/{genre_id}', response_model=GenreAPI)
async def genre_details(genre_id: UUID, genre_service: GenreService = Depends(get_genre_service)) -> GenreAPI:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return GenreAPI(**genre.dict())


@router.get('/genres', response_model=list[GenreAPI])
async def genre_list_details(genre_service: GenreService = Depends(get_genre_service)) -> list[GenreAPI]:
    ...
