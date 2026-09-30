
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource.resources import ResourceManagementClient

def ensure_resource_group_exists(subscription_id: str, resource_group_name: str, location: str) -> dict:
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id=subscription_id)
    
    # It reuses the group if it exists, or spins up a new one if it doesn't.
    result = resource_client.resource_groups.create_or_update(
        resource_group_name,
        {"location": location}
    )
    
    return {
        "azure_resource_id": result.id,
        "name": result.name,
        "location": result.location,
        "provisioning_state": result.properties.provisioning_state if result.properties else "Succeeded"
    }
