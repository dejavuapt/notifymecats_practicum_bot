from typing import TypeVar, Optional
from pokeroom.utils.types import JSONDict

Poke_T = TypeVar("Poke_T", bound = "PokeroomObject", covariant = True)

class PokeroomObject:
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    def _de_json(
        cls: type[Poke_T],
        data: JSONDict, 
    ) -> Poke_T:
        try:
            obj = cls(**data)
        except TypeError as exc:
            raise
        return obj
    
    @staticmethod
    def _parse_data(data: JSONDict) -> JSONDict:
        """ Гарантия того что входные данные не будут изменены """
        return data.copy()
    
    @classmethod
    def de_json(
        cls: type[Poke_T],
        data: JSONDict,
    ) -> Poke_T:
        return cls._de_json(data = data)
    
    @classmethod
    def de_list(
        cls: type[Poke_T],
        data: list[JSONDict]
    ) -> tuple[Poke_T, ...]:
        return tuple(cls.de_json(d) for d in data)