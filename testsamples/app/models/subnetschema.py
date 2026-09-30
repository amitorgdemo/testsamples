from typing import Optional
from pydantic import BaseModel, Field

class SubnetSchema(BaseModel):
    name: str = Field(..., min_length=1, description="The unique allocation name for the subnet partition")
    address_prefix: str  = Field(..., min_length=1, description="The specific structural CIDR block for this sub-network partition")