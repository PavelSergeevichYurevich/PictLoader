from typing import Annotated, Literal
from pydantic import BaseModel, Field, conint


class ImageSearchScema(BaseModel):
    provider: Literal["pexels", "auto"]
    q: str
    page: Annotated[int, conint(ge=1)] = 1
    limit: Annotated[int, conint(ge=1, le=80)] = 20
    