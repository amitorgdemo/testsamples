from typing import Optional
from pydantic import BaseModel, Field

class ItemPayload(BaseModel):
    item_id: Optional[int]
    item_name: str
    quantity: int

