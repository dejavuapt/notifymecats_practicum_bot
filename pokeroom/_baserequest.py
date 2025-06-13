from aiohttp import ClientSession
from http import HTTPStatus
from utils.types import JSONDict
from typing import Union, Optional
from utils.logging import get_logger

class BaseRequest:
    
    def __init__(self, service_name: str):
        self._service_name = service_name
    
    _LOGGER = get_logger(__name__)

    async def _do_get(self, 
                      endpoint: str, 
                      headers: JSONDict,
                      **kwargs, ) -> Union[bool, JSONDict, list[JSONDict]]:
        async with ClientSession() as session:
            self._LOGGER.debug("Calling %s endpoint `%s`", self._service_name , endpoint)
            async with session.get(
                url = f"{self._base_url}{endpoint}/",
                headers = headers
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
                    "Call to %s endpoint `%s` finished with return value `%s`", self._service_name, endpoint, result
                    )
                
        return result
        
    async def _do_post(self, 
                 endpoint: str, 
                 data: JSONDict, 
                 headers: Optional[JSONDict] = None,
                 **kwargs, ) -> Union[bool, JSONDict, list[JSONDict]]:
        if headers is None:
            headers = {}
        async with ClientSession() as session:
            self._LOGGER.debug("Calling %s endpoint `%s`", self._service_name , endpoint)
            async with session.post(
                url = f"{self._base_url}{endpoint}/",
                headers = headers,
                data = data
            ) as response:
                if response.status not in [HTTPStatus.CREATED, HTTPStatus.OK]:
                    raise RuntimeError(
                        f"API request to {endpoint} failed with status {response.status}"
                    )
                
                try:
                    result = await response.json()
                except ValueError as e:
                    self._LOGGER.error("Failed to parse JSON response: %s", str(e))
                    return False
                self._LOGGER.debug(
                    "Call to %s endpoint `%s` finished with return value `%s`", self._service_name, endpoint, result
                    )
        return result
    
    # def _do_patch(self, endpoint: str, data: JSONDict, **kwargs, ): 
    #     pass
    
    # def _do_delete(self, endpoint:str, **kwargs,): 
    #     pass