from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models import Person
from services import PersonService, get_person_service, cache
from services.genre_person import GenrePersons

router = APIRouter()


class PersonAPI(Person):
    pass


@router.get('/{person_id}', response_model=Person_PD)
@cache(60)
async def person_details(person_id: UUID, person_service: GenrePersons = Depends(get_person_service)) -> PersonAPI:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person.dict()


@router.get('/persons_list/{person_id}', response_model=list)
async def person_list_details(person_id: str, person_service: GenrePersons = Depends(get_person_service)) -> PersonAPI:
    person = await person_service.get_by_text(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person
