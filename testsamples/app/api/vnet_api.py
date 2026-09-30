from fastapi import APIRouter, HTTPException, status, Query
from typing import Dict, Any

from app.models import VirtualNetworkRequest, VirtualNetworkResponse
from app.db import vnet_repo

# Import decoupled service layer functionalities
from app.services import provision_virtual_network, fetch_live_azure_vnet_details

router = APIRouter(prefix="/vnets", tags=["Azure Virtual Networks"])

@router.post("", response_model=VirtualNetworkResponse, status_code=status.HTTP_201_CREATED)
async def create_vnet(request: VirtualNetworkRequest):
    try:
        return provision_virtual_network(request)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Azure VNET Framework Provisioning Error: {str(e)}"
        )

@router.get("/db/{resource_id}")
async def get_vnet(resource_id: str):
    record = vnet_repo.get_resource(resource_id)
    if not record:
        raise HTTPException(
            status_code=404, 
            detail="VNET record not found in the local database storage layer."
        )
    return record

@router.get("")
async def list_vnets():
    return vnet_repo.get_all_resources()

@router.get("/azure/details", response_model=VirtualNetworkResponse)
async def get_vnet_details(
    subscription_id: str = Query(...), 
    resource_group: str = Query(...), 
    vnet_name: str = Query(...)
):
    try:
        return fetch_live_azure_vnet_details(subscription_id, resource_group, vnet_name)
    except Exception as e:
        raise HTTPException(
            status_code=404, 
            detail=f"Failed to fetch vnet detail context: {str(e)}"
        )
