from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")
class ResultVO(GenericModel, Generic[T]):
    code: int = 0
    message: str = 'success'
    data: Optional[T] = None

def success_result(data: T) -> T:
    return ResultVO(data=data)

class UserAppReqVO(BaseModel):
    desc: str