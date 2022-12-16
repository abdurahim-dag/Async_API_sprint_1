from http import HTTPStatus
from uuid import UUID
from api.v1.query_parameters import FilmParams
from fastapi import APIRouter, Depends, HTTPException

from models import FilmDetail, Film
from services import FilmService, get_film_service, cache


router = APIRouter()


@router.get(
    '',
    response_model=list[Film],
    summary='Главная страница фильмов.',
    description='На ней выводятся популярные фильмы, с указанием поля сортировки и жанра.',
    response_description="Список фильмов.",
)
@cache(26)
async def film_list(
        film_service: FilmService = Depends(get_film_service),
        common_params: FilmParams = Depends(),
) -> list[Film]:
    films = await film_service.get_list(common_params)
    return films

@router.get(
    '/search',
    response_model=list[Film],
    summary='Полнотекстовый поиск по фильмам.',
    description="""
    Полнотекстовый поиск фильма, по указанному параметру query в запросе.
    """,
    response_description="Список фильмов.",
)
@cache(26)
async def film_list_search(
        film_service: FilmService = Depends(get_film_service),
        common_params: FilmParams = Depends()
) -> list[Film]:
    films = await film_service.get_list(common_params)
    return films


@router.get(
    '/{film_id}',
    response_model=FilmDetail,
    summary='Информация о фильме.',
    description='Детальная информация о фильме.',
    response_description="Фильм с информацией по всем имеющимися полям.",
)
@cache(60)
async def film_detail(
        film_id: UUID,
        film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film
