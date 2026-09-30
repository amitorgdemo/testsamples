from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.subnetschema import SubnetSchema
from azure.mgmt.network.models import  AddressSpace

class VirtualNetworkRequest(BaseModel):
    subscription_id: str = Field(
        ..., 
        min_length=1, 
        description="The Azure Subscription ID used for this request", 
    )
    # resourse_group: str
    # location: str 
    # vnet_name:str
    # vnet_address_space:str
    # subnet_name: str
    # subnet_addres_pefix:str
    resource_group: str = Field(
        ..., 
        min_length=1, 
        description="The targeted resource group space", 
    ) 
    vnet_name: str = Field(
        ..., 
        min_length=1, 
        description="The primary name of the Virtual Network environment", 
    )
    location: str = Field(
        ..., 
        min_length=1, 
        description="The targeted deployment datacenter region", 
    ) 
    address_space: str = Field(
        ..., 
        min_length=1, 
        description="The main top-level CIDR network range block allocation", 
    )
    subnets: List[SubnetSchema] = Field(
        ..., 
        min_items=1, 
        description="A list containing at least one valid subnet definition layout block"
    )

    network_security_group_name: Optional [str] = Field(default=None)    

class VirtualNetworkResponse(BaseModel):
    id: Optional[str] 
    subscription_id: str
    azure_resource_id: str
    name: str =Field(..., description="The name of the Virtual Network")
    location: str
    resource_group: str
    address_space: List[str]
    subnets: List[SubnetSchema]
    provisioning_state: str