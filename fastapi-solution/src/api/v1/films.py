from http import HTTPStatus
from uuid import UUID
from api.v1.query_parameters import FilmParams
from fastapi import APIRouter, Depends, HTTPException

from models import FilmDetail, FilmSearch
from services import FilmService, get_film_service, cache


router = APIRouter()


@router.get('/search', response_model=list[FilmSearch])
async def film_list_details(
        #film_service: FilmService = Depends(get_film_service),
        common_params: FilmParams = Depends()
) -> list[FilmSearch]:

    for c in common_params:
        print(c)


@router.get('/{film_id}', response_model=FilmDetail)
@cache(60)
async def film_details(film_id: UUID, film_service: FilmService = Depends(get_film_service)) -> FilmDetail:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmDetail(**film.dict())


#
# @router.get('/genre_list/{genre_id}', response_model=list)
# async def genre_list_details(genre_id: str, genre_service: GenrePersons = Depends(get_genre_service)) -> list[GenreAPI]:
#     genre = await genre_service.get_by_id(genre_id)
#     if not genre:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
#     return genre.dict()
