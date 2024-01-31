import re
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, validator, root_validator

from app.constants import SCHEMA_EXTRA


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


# Создадим клаасс Person, унаследованный от BaseModel;
# в атрибутах класса перечислим ожидаемые параметры запроса.
# Анатируем атрибуты клкасса
class Person(BaseModel):
    name: str = Field(
        ..., max_length=20,
        title='Полное имя',
        description='Можно вводить в любом регистре'
    )
    surname: Union[str, list[str]] = Field(
        ..., max_length=50)
    age: Optional[int] = Field(None, gt=4, le=99)
    is_staff: bool = Field(False, alias='is_staff')
    edcucation_level: Optional[EducationLevel]

    class Config:
        title = 'Класс для приветствия'
        # мигимальня длина всех полей где она есть
        min_anystr_length = 2
        schema_extra = SCHEMA_EXTRA

    # В качесетвее аргумента валидатору передается имя поля,
    # которое нужно проверять
    @validator('name')
    # Первый параметр функции-валидатора должен называться строго cls
    # Вторым паораметром идет проверяемое значение,
    # его можно назвать как угодно
    # Декоратор @classmethod ставить нельзя, иначе валидатор не сработает
    def name_cant_be_numeric(cls, value: str):
        if value.isnumeric():
            # При ошибке валидации можно выбросить
            # ValueError, TypeError, или AssertionError.
            # В нашем случае подходит ValueError
            # В аргументе передаём сообщение об ошибке.
            raise ValueError('Имя не может быть  числом')
        # Если проверка пройдена, возвращаем значение поля.
        return value

    # Корневой валидатор можно использовать без параметров
    @root_validator(skip_on_failure=True)
    # skip... - пропустить если в прошлом вадиаторе была ошибка
    # К названию параметров функции-валидатора нет строгих требований
    # Первым передаётся класс, вторым - словарь со значениями всех полей
    def using_different_languages(cls, values):
        # Объединяем все фамалии в единую строку
        # Даже если value['surname'] - строка, ошибки не будет
        # Просто все буквы занаво объединятся в строку.
        surname = ''.join(values['surname'])
        # Объединяем имя и фамилию в одну строку.
        cheked_value = values['name'] + ' ' + surname
        # Ишем хотя ьы одну кириллическую букву в строке
        # и хотя бы одну латинскую букву
        # Флаг re.IGNORECASE указывает на то, что регистр не важен.
        if (re.search('[а-я]', cheked_value, re.IGNORECASE)
                and re.search('[a-z]', cheked_value, re.IGNORECASE)):
            raise ValueError(
                'Пожалуйста, не смешивайте русские и латинские буквы'
                )

        # Если проверка пройдена, возвращается словарь со всеми значениями.
        return values
