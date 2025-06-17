from pokeroom.utils.types import JSONDict
from pokeroom._pokeroomobject import PokeroomObject
from typing import Optional


class Team(PokeroomObject):
    def __init__(self,
                 team_id: str,
                 owner: str,
                 role: str,
                 data: JSONDict) -> None:
        super().__init__()
        
        self.name: str = data.get("name", None)
        self.id: str = team_id
        self.owner_id: str = owner
        self.user_role: str = role
        self.description: Optional[str] = data.get("description", None)
        
        self._attrs = (self.id, self.name, self.owner_id, self.description, self.user_role)
        
    @classmethod
    def de_json(cls, data: JSONDict) -> "Team":
        data = cls._parse_data(data)
        return super().de_json(data=data)