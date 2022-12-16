from http import HTTPStatus
from api.v1.query_parameters import PersonParams
from uuid import UUID
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException, Request

from models import Person, PersonDetail, Film
from services import PersonService, get_person_service, cache


router = APIRouter()


@router.get(
    '/{person_id}',
    response_model=PersonDetail,
    summary='Информация о персоне.',
    description='Детальная информация о персоне.',
    response_description="ИИнформация со всеми имеющимися полям о персоне.",
)
@cache(60)
async def person_detail(person_id: UUID, person_service: PersonService = Depends(get_person_service)) -> PersonDetail:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get(
    '/{person_id}/film',
    response_model=list[Film],
    summary='Информация о фильме.',
    description='Детальная информация о фильме связанном с персоной.',
    response_description="Фильм с информацией по всем имеющимися полям.",
)
async def person_film(
        person_id: UUID,
        request: Request,
        person_service: PersonService = Depends(get_person_service)
) -> list[Film]:
    person: PersonDetail = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    ids = [str(film_id) for film_id in person.film_ids]
    query_str = ""
    for _id in ids:
        q = f"ids={_id}"
        query_str += '&' + q
    if query_str:
        query_str = '?' + query_str[1:]
        app = request.app
        url = app.url_path_for("film_list_search")
        url += query_str
        return RedirectResponse(url)
    return person


