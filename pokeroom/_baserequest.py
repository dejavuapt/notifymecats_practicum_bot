from aiohttp import ClientSession
from http import HTTPStatus, HTTPMethod
from pokeroom.utils.types import JSONDict
from typing import Union, Optional
from pokeroom.utils.logging import get_logger

class BaseRequest:
    
    def __init__(self, service_name: str):
        self._service_name = service_name
    
    _LOGGER = get_logger(__name__)
    
    async def _do_request(
        self,
        method: HTTPMethod,
        endpoint: str,
        *,
        headers: Optional[JSONDict] = None,
        data: Optional[JSONDict] = None,
    ) -> Union[bool, JSONDict, list[JSONDict]]:
        async with ClientSession() as session:
            http_method = getattr(session, method.lower(), None)
            self._LOGGER.debug("Calling %s %s endpoint `%s`", method, self._service_name , endpoint)
            if not http_method:
                raise ValueError(f"Not supported method: {method}") 
           
            headers = headers or {}
            data = data or {}
           
            async with http_method(
               url = f"{self._base_url}{endpoint}/", 
               headers = headers,
               data = data
            ) as response:
                if not str(response.status).startswith("2"):
                    raise RuntimeError(
                       f"API request to {endpoint} failed with status {response.status}"
                   )
                try:
                    result = await response.json()
                except ValueError as exp:
                    self._LOGGER.error("Failed to parse JSON response: %s", str(exp))
                    return False
                self._LOGGER.debug(
                    "Call to %s endpoint `%s` finished with return value `%s`", self._service_name, endpoint, result
                    ) 
        return result
                   

    async def _do_get(self, 
                      endpoint: str, 
                      headers: JSONDict,
                      **kwargs, ) -> Union[bool, JSONDict, list[JSONDict]]:
        return await self._do_request(HTTPMethod.GET, endpoint, headers=headers)
        
    async def _do_post(self, 
                 endpoint: str, 
                 data: JSONDict, 
                 headers: Optional[JSONDict] = None,
                 **kwargs, ) -> Union[bool, JSONDict, list[JSONDict]]:
        result = await self._do_request(HTTPMethod.POST, endpoint, headers=headers, data=data)
        return result
    
    # def _do_patch(self, endpoint: str, data: JSONDict, **kwargs, ): 
    #     pass
    
    # def _do_delete(self, endpoint:str, **kwargs,): 
    #     pass