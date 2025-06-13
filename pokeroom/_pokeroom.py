from utils.types import BaseUrl, JSONDict
from utils.logging import get_logger
from error import InvalidJWTToken
from endpoints import Endpoints
from functools import cache
from typing import Union, Optional, Any
import requests
from aiohttp import ClientSession
from http import HTTPStatus

class Pokeroom():
    
    def __init__(
        self,
        base_url: BaseUrl = "http://127.0.0.1/api/v1/",
    ):  
        self._base_url: BaseUrl = base_url
        
    _LOGGER = get_logger(__name__)
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
                        ) -> JSONDict:
        if access_token is None:
            raise InvalidJWTToken(f"Call `{self.get_teams.__name__}` need user's token to access API.")
        
        headers: JSONDict = {"Authorization": f"Bearer {access_token}"}
        
        return await self._do_get(
            self._ENDPOINTS.USER_TEAMS_LIST,
            headers
        )    
        
        
    # --- PRIVATE ---
    async def _do_get(self, 
                      endpoint: str, 
                      headers: JSONDict,
                      **kwargs, ) -> Union[bool, JSONDict, list[JSONDict]]:
        async with ClientSession() as session:
            self._LOGGER.debug("Calling Pokeroom API endpoint `%s`", endpoint)
            async with session.get(
                url = f"{self._base_url}{endpoint}/",
                headers = headers,
                **kwargs
            ) as response:
                if response.status != HTTPStatus.OK:
                    raise RuntimeError(
                        f"API request to {endpoint} failed with status {response.status}"
                    )
                try:
                    result = await response.json()
                except ValueError as e:
                    self._LOGGER.error("Failed to parse JSON response: %s", str(e))
                    return False
                self._LOGGER.debug(
                    "Call to Pokeroom API endpoint `%s` finished with return value `%s`", endpoint, result
                    )
                
        return result
        
        
        
    
    def _do_post(self, endpoint: str, data: JSONDict, **kwargs, ) -> Union[bool, JSONDict, list[JSONDict]]:
        pass
    
    # def _do_patch(self, endpoint: str, data: JSONDict, **kwargs, ): 
    #     pass
    
    # def _do_delete(self, endpoint:str, **kwargs,): 
    #     pass
    
    
    
    
    
pr = Pokeroom()
