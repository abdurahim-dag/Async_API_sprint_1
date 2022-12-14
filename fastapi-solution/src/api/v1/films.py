from http import HTTPStatus
from uuid import UUID
from api.v1.query_parameters import FilmParams
from fastapi import APIRouter, Depends, HTTPException

from models import FilmDetail, Film
from services import FilmService, get_film_service, cache


router = APIRouter()

@router.get('/', response_model=list[Film])
@cache(6)
async def film_list_details(
        film_service: FilmService = Depends(get_film_service),
        common_params: FilmParams = Depends()
) -> list[Film]:
    films = await film_service.get_list(common_params)
    return films

@router.get('/search', response_model=list[Film])
@cache(6)
async def film_list_details(
        film_service: FilmService = Depends(get_film_service),
        common_params: FilmParams = Depends()
) -> list[Film]:
    films = await film_service.get_list(common_params)
    return films


@router.get('/{film_id}', response_model=FilmDetail)
@cache(60)
async def film_details(film_id: UUID, film_service: FilmService = Depends(get_film_service)) -> FilmDetail:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmDetail(**film.dict())
