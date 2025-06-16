from functools import cache


class Endpoints():
    
    def __init__(self):
        self._USERS_LIST: str = "u"
        self._TOKEN_CREATE: str = "token/jwt/create"
        self._TEAMS_LIST: str = "teams"
    
    @property
    def USERS_LIST(self) -> str:
        return self._USERS_LIST
    
    @property
    def TOKEN_CREATE(self) -> str:
        return self._TOKEN_CREATE
        
    @property
    @cache
    def USER_TEAMS_LIST(self) -> str:
        return "%s/%s" % (self._USERS_LIST, self._TEAMS_LIST)
