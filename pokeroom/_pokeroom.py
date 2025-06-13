from pokeroom.utils.types import BaseUrl, JSONDict

from pokeroom.error import InvalidJWTToken
from pokeroom.endpoints import Endpoints
from typing import Union, Optional, Any
import requests

from pokeroom._pokeroomobject import Team, Token
from pokeroom._baserequest import BaseRequest

class Pokeroom(BaseRequest):
    
    def __init__(
        self,
        base_url: BaseUrl = "http://localhost:8000/api/v1/",
    ):  
        super().__init__("Pokeroom API")
        self._base_url: BaseUrl = base_url
        
    
    _ENDPOINTS = Endpoints()
    
    @property
    def base_url(self) -> str:
        return self._base_url
    
    async def registration_in_service(
        self, 
        user_data: Optional[JSONDict] = None,
        **kwargs, 
    ) -> Token:
        """
        Registers a user in the service
        
        Args:
            user_data (:obj:`JSONDict`): User credentials username, email and password
            
        Returns:
            result (:obj:`bool`, :obj:`JSONDict`): If errors - :obj: `False` else 
            dictionary of access and refresh tokens
        """
        if user_data is None:
            return False # TODO: need raise. {username, password, email}
        
        # TODO: Need some do when cred not good
        result_reg: Union[bool, JSONDict] = await self._do_post(
            self._ENDPOINTS.USERS_LIST,
            data = user_data,
        )
        print(f"{result_reg}")
        if isinstance(result_reg, dict):
            result = await self._do_post(
                self._ENDPOINTS.TOKEN_CREATE,
                data = {
                    "username": result_reg.get("username"),
                    "password": user_data.get("password")
                }
            )
            print(result)
            return Token.de_json(result)
        else:
            raise ValueError("lazy..")
    
    async def get_teams(
        self,
        access_token: str,
    ) -> tuple[Team, ...]:
        """
        Retrieves the list of user teams. 
        Teams gets by owner user or where he is a member.
        
        Args:
            access_token (:obj:`str`): JWT Token to access data
            
        Returns:
            result (:obj:`bool`, tuple[:class:`Team`]): List of user's teams or if error - False
        """
        if access_token is None:
            raise InvalidJWTToken(f"Call `{self.get_teams.__name__}` need user's token to access API.")
        
        headers: JSONDict = {"Authorization": f"Bearer {access_token}"}
    
        result = await self._do_get(
            self._ENDPOINTS.USER_TEAMS_LIST,
            headers
        )
        # response must be a list in everything. Check exception in `de_json` method
        return Team.de_list(result)
