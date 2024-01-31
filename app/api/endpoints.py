from fastapi import APIRouter, Body

from app.schemas.schemas import Person

router = APIRouter()


@router.post('/hello')
def greetings(
    person: Person = Body(
        ...,
        examples=Person.Config.schema_extra['examples']
    )
) -> dict[str, str]:
    if isinstance(person.surname, list):
        surname = ' '.join(person.surname)
    else:
        surname = person.surname
    result = ' '.join([person.name, surname])
    result = result.title()
    if person.age is not None:
        result += ', ' + str(person.age)
    if person.edcucation_level is not None:
        result += ', ' + person.edcucation_level.lower()
    if person.is_staff:
        result += ', сотрудник'
    return {'Hello': result}
