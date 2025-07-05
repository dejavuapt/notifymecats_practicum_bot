from pokeroom._pokeroomobject import PokeroomObject
from pokeroom.utils.types import JSONDict

class Member(PokeroomObject):
    def __init__(
        self,
        username: str,
        data: JSONDict,
    ) -> None:
        super().__init__()
        
        self.team_id: str = data.get("team")
        self.role: str = data.get("role")
        self.username: str = username
        
        self._attrs = (self.role, self.team_id, self.username)
        
    @classmethod
    def de_json(cls, data) -> "Member":
        data = cls._parse_data(data)
        return super().de_json(data)