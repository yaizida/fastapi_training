from fastapi import FastAPI, Body
# Для работы с  JSON в теле запроса
# импортируем из pydantic класс BaseModel
import uvicorn

from app.schemas.schemas import Person
# Создание объекта приложения.
app = FastAPI()


# Меняем метод GET на POST, указываем статичный адрес.
@app.post('/hello')
# Вместо множества параметра теперь будет только один - person,
# в качестве анатации указываем класс Person.
def greetings(
    person: Person = Body(
        ..., examples=Person.Config.schema_extra['examples']
            )
        ) -> dict[str, str]:
    # Обращение к атрибутам класса происходит через точку
    # при этом будут работать проверки на уровне типов данных
    # В IDE будут работать автодополнени
    surnames = ' '.join(person.surname)
    result = ' '.join([person.name, surnames])
    result = result.title()
    if person.age is not None:
        result += ', ' + str(person.age)
    if person.edcucation_level is not None:
        result += ', ' + person.edcucation_level.lower()
    if person.is_staff:
        result += ', сотрудник'
    return {'Hello': result}


if __name__ == '__main__':
    # Команда на запуск uvicorn.
    # Здесь же можно указать хост и\или порт при неопхоимости,
    # а также другие параметры.
    uvicorn.run('main:app', reload=True)
