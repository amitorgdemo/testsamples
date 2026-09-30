from pydantic import BaseModel, Field
from typing import Optional

class ResourceGroupRequest(BaseModel):
    subscription_id: str = Field(..., min_length=1, description="The Azure Subscription ID")
    resource_group_name: str = Field(..., min_length=1, description="Name of the resource group to create")
    location: str = Field(..., min_length=1, description="Azure Region location targeted")

class ResourceGroupResponse(BaseModel):
    azure_resource_id: str = Field(..., description="Fully qualified Azure Resource Manager identifier ID")
    name: str = Field(..., description="The confirmed name of the resource group")
    location: str = Field(..., description="The regional placement assignment")
    provisioning_state: str = Field(..., description="Current status of operation deployment")
