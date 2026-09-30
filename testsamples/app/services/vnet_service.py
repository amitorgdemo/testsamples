import uuid
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import VirtualNetwork, AddressSpace, Subnet

from app.models import VirtualNetworkRequest
from app.db import vnet_repo
from app.services import ensure_resource_group_exists

def provision_virtual_network(request: VirtualNetworkRequest) -> dict:

    ensure_resource_group_exists(
        subscription_id=request.subscription_id,
        resource_group_name=request.resource_group,
        location=request.location
    )    
    
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id=request.subscription_id)
    
    azure_subnets = [
        Subnet(name=s.name, address_prefix=s.address_prefix) for s in request.subnets
    ]
    
    vnet_params = VirtualNetwork(
        location=request.location,
        address_space=AddressSpace(address_prefixes=[request.address_space]),
        subnets=azure_subnets
    )
    
    async_vnet_creation = network_client.virtual_networks.begin_create_or_update(
        request.resource_group, 
        request.vnet_name, 
        vnet_params
    )
    result = async_vnet_creation.result()
    
    resource_id = str(uuid.uuid4())
    record = {
        "id": resource_id,
        "subscription_id": request.subscription_id,
        "azure_resource_id": result.id,
        "name": result.name,
        "location": result.location,
        "resource_group": request.resource_group,
        "address_space": result.address_space.address_prefixes if result.address_space else [request.address_space],
        "subnets": [{"name": s.name, "address_prefix": s.address_prefix} for s in request.subnets],
        "provisioning_state": result.provisioning_state
    }
    
    vnet_repo.save_resource(resource_id, record)
    return record

def fetch_live_azure_vnet_details(subscription_id: str, resource_group: str, vnet_name: str) -> dict:
    credential = DefaultAzureCredential()
    network_client = NetworkManagementClient(credential, subscription_id=subscription_id)
    
    vnet = network_client.virtual_networks.get(resource_group, vnet_name)
    
    return {
        "id": None,
        "subscription_id": subscription_id,
        "azure_resource_id": vnet.id,
        "name": vnet.name,
        "location": vnet.location,
        "resource_group": resource_group,
        "address_space": vnet.address_space.address_prefixes if vnet.address_space else [],
        "subnets": [{"name": s.name, "address_prefix": s.address_prefix} for s in (vnet.subnets or [])],
        "provisioning_state": vnet.provisioning_state
    }
