from utils.types import BaseUrl, JSONDict

from error import InvalidJWTToken
from endpoints import Endpoints
from functools import cache
from typing import Union, Optional, Any
import requests

from _pokeroomobject import Team, User
from _baserequest import BaseRequest

class Pokeroom(BaseRequest):
    
    def __init__(
        self,
        base_url: BaseUrl = "http://127.0.0.1/api/v1/",
    ):  
        super().__init__("Pokeroom API")
        self._base_url: BaseUrl = base_url
        
    
    _ENDPOINTS = Endpoints()
    
    @property
    def base_url(self) -> str:
        return self._base_url
    
    async def registration_in_service(self, 
                                      user_data: Optional[JSONDict] = None,
                                      **kwargs, ) -> Union[bool, JSONDict]:
        if user_data is None:
            return False # TODO: need raise. {username, password, email}
        
        # TODO: Need some do when cred not good
        response_register: Union[bool, JSONDict] = await self._do_post(
            self._ENDPOINTS.USERS_LIST,
            data = user_data,
        )
        if response_register:
            response = await self._do_post(
                self._ENDPOINTS.TOKEN_CREATE,
                data = {
                    "username": response_register.get("username"),
                    "password": user_data.get("password")
                }
            )
            return response # format: {"refresh": str, "access": str}
        return False
        
    
    async def get_teams(self,
                        access_token: Optional[JSONDict] = None,
                        ) -> Union[bool, tuple[Team, ...]]:
        if access_token is None:
            raise InvalidJWTToken(f"Call `{self.get_teams.__name__}` need user's token to access API.")
        
        headers: JSONDict = {"Authorization": f"Bearer {access_token}"}
    
        result = await self._do_get(
            self._ENDPOINTS.USER_TEAMS_LIST,
            headers
        )
        # response must me a list in everything. Check exception in de json method
        return Team.de_list(result)
