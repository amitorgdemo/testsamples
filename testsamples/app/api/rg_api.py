from fastapi import APIRouter, HTTPException, status
from app.models import ResourceGroupRequest, ResourceGroupResponse
from app.services import ensure_resource_group_exists

router = APIRouter(prefix="/resource-groups", tags=["Azure Resource Groups Workspace"])

@router.post("", response_model=ResourceGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_resource_group(request: ResourceGroupRequest):
    try:
        return ensure_resource_group_exists(
            subscription_id=request.subscription_id,
            resource_group_name=request.resource_group_name,
            location=request.location
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Resource Group Service Execution Failure: {str(e)}"
        )
