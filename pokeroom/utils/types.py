from typing import Union, Callable, Any

BaseUrl = Union[str, Callable[[str], str]]

JSONDict = dict[str, Any]