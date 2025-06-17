from pokeroom._pokeroomobject import PokeroomObject


class Token(PokeroomObject):
    def __init__(
        self,
        refresh: str,
        access: str
    ) -> None:
        super().__init__()
        
        self.refresh: str = refresh
        self.access: str = access
        
        self._attrs = (self.refresh, self.access)
        
    @classmethod
    def de_json(cls, data) -> "Token":
        data = cls._parse_data(data)
        return super().de_json(data)