from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models import FilmMixin
from services.film import FilmService, get_film_service


router = APIRouter()


class FilmAPI(FilmMixin):
    pass


@router.get('/{film_id}', response_model=FilmAPI)
async def film_details(film_id: UUID, film_service: FilmService = Depends(get_film_service)) -> FilmAPI:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmAPI(**film.dict())


@router.get('', response_model=list[FilmAPI])
async def film_list_details(film_service: FilmService = Depends(get_film_service)) -> list[FilmAPI]:
    ...
