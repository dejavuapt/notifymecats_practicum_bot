from typing import Optional

class PokeroomError(Exception):
    def __init__(self, message: str):
        
        super().__init__()
        msg = message.removeprefix("Error: ") \
            .removeprefix("[Error]: ") \
            .removeprefix("Bad Request: ")
        if msg != message:
            msg = msg.capitalize()
        self.message: str = msg
        
    def __str__(self) -> str:
        return self.message
    
    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.message)
    
    
class InvalidJWTToken(PokeroomError):
    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__("Invalid jwt token" if message is None else message)