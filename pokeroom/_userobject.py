from pokeroom._pokeroomobject import PokeroomObject
from pokeroom.utils.types import JSONDict
from typing import Optional

class User(PokeroomObject):
    def __init__(self,
                 id: str,
                 data: Optional[JSONDict] = None,
                 ) -> None:
        super().__init__()
        
        self.name: str = data.get("username", None)
        self.id: str = id
        self.first_name: str = data.get("first_name", None)
        self.last_name: str = data.get("last_name", None)
        self.email: str = data.get("email", None)
        
        self._attrs = (
            self.name,
            self.id,
            self.first_name,
            self.last_name,
            self.email
        )
        
    @classmethod
    def de_json(cls, data: JSONDict) -> "User":
        data = cls._parse_data(data)
        return super().de_json(data=data)