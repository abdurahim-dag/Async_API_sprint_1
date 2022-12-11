from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models import Genre
from services import GenreService, get_genre_service, cache
from services.genre_person import GenrePersons
router = APIRouter()


class GenreAPI(Genre):
    pass


@router.get('/{genre_id}', response_model=GenreAPI)
async def genre_details(genre_id: UUID, genre_service: GenrePersons = Depends(get_genre_service)) -> GenreAPI:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre.dict()


@router.get('/genre_list/{genre_id}', response_model=list)
async def genre_list_details(genre_id: str, genre_service: GenrePersons = Depends(get_genre_service)) -> list[GenreAPI]:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre.dict()
