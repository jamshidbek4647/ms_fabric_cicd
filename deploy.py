import os
from pathlib import Path
from azure.identity import ClientSecretCredential
from fabric_cicd import FabricWorkspace, publish_all_items

target_env = os.environ["TARGET_ENV"]
workspace_map = {
    "dev": os.environ["DEV_WORKSPACE_ID"],
    "tst": os.environ["TEST_WORKSPACE_ID"],
    "prd": os.environ["PROD_WORKSPACE_ID"],
}
workspace_id = workspace_map[target_env]

# Point to the environment-specific subfolder
repo_root = Path(__file__).resolve().parent
env_folder = repo_root / "fabric" / target_env

if not env_folder.exists():
    raise FileNotFoundError(f"Environment folder not found: {env_folder}")

credential = ClientSecretCredential(
    tenant_id=os.environ["TENANT_ID"],
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
)

workspace = FabricWorkspace(
    workspace_id=workspace_id,
    environment=target_env,
    repository_directory=str(env_folder),
    item_type_in_scope=["Notebook", "DataPipeline", "Environment"],
    token_credential=credential,
)

publish_all_items(workspace)
print(f"✅ Deployed {target_env} from {env_folder}")
