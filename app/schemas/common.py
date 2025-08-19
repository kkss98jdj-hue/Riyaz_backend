from typing import Generic,TypeVar,Optional
from pydantic.generics import GenericModel

T= TypeVar('T')

class BaseResponse(GenericModel,Generic[T]):
    Status:str
    Message:str
    Data:Optional[T]=None