import os
from pathlib import Path
from azure.identity import ClientSecretCredential
from fabric_cicd import FabricWorkspace, publish_all_items

# Get the target environment from pipeline
target_env = os.environ["TARGET_ENV"] 

# Map env to workspace ID
workspace_map = {
    "dev": os.environ["DEV_WORKSPACE_ID"],
    "tst": os.environ["TEST_WORKSPACE_ID"],
    "prd": os.environ["PROD_WORKSPACE_ID"],
}

workspace_id = workspace_map[target_env]

# Call the service Principal with vargroup
credential = ClientSecretCredential(
    tenant_id=os.environ["TENANT_ID"],
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
)

# Connect to workspace and deploy
workspace = FabricWorkspace(
    workspace_id=workspace_id,
    environment=target_env,
    repository_directory=str(Path(__file__).resolve().parent),
    item_type_in_scope=[
    "Notebook", "DataPipeline", "Environment",
    "Lakehouse", "SparkJobDefinition", "SemanticModel",
    "Report", "Warehouse", "Dataflow", "Eventhouse",
    "KQLDatabase", "KQLQueryset", "KQLDashboard",
    "Eventstream", "Reflex", "MirroredDatabase",
    "SQLDatabase", "GraphQLApi", "CopyJob", "VariableLibrary"],
    token_credential=credential,
)

publish_all_items(workspace)
print(f"Successfully deployed to {workspace_id}")
