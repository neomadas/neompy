from enum import IntEnum as PythonIntEnum

from django.db.models import IntegerChoices


class IntEnum(PythonIntEnum):
  @classmethod
  def ToIntegerChoices(cls) -> IntegerChoices:
    keys = [(key.name, key.value) for key in list(cls)]
    return IntegerChoices(f'{cls.__name__}Choices', keys)
