from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models import Person
from services import PersonService, get_person_service

router = APIRouter()


class PersonAPI(Person):
    pass


@router.get('/{person_id}', response_model=PersonAPI)
async def person_details(person_id: UUID, person_service: PersonService = Depends(get_person_service)) -> PersonAPI:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonAPI(**person.dict())


@router.get('/persons', response_model=list[PersonAPI])
async def person_list_details(person_service: PersonService = Depends(get_person_service)) -> list[PersonAPI]:
    ...
