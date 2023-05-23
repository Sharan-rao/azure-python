import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from pulumi_azure_native import keyvault

tenantId = "52c5f229-1e7a-4773-af5a-ef52db324ced"
objectId = "d46510dc-7a3c-4275-b1c0-edc843a90a5f"

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("resource_group")

# Create an Azure resource (Storage Account)
account = storage.StorageAccount(
    "sa",
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(
        name=storage.SkuName.STANDARD_LRS,
    ),
    kind=storage.Kind.STORAGE_V2,
)

# Create a second Azure resource (Key Vault)
#change name 
vault = keyvault.Vault("vault", 
    properties=keyvault.VaultPropertiesArgs(
        access_policies=[keyvault.AccessPolicyEntryArgs(
            object_id=objectId,
            permissions=keyvault.PermissionsArgs(
                certificates=[
                    "get",
                    "list",
                    "delete",
                    "create",
                    "import",
                    "update",
                    "managecontacts",
                    "getissuers",
                    "listissuers",
                    "setissuers",
                    "deleteissuers",
                    "manageissuers",
                    "recover",
                    "purge",
                ],
                keys=[
                    "encrypt",
                    "decrypt",
                    "wrapKey",
                    "unwrapKey",
                    "sign",
                    "verify",
                    "get",
                    "list",
                    "create",
                    "update",
                    "import",
                    "delete",
                    "backup",
                    "restore",
                    "recover",
                    "purge",
                ],
                secrets=[
                    "get",
                    "list",
                    "set",
                    "delete",
                    "backup",
                    "restore",
                    "recover",
                    "purge",
                ],
            ),
            tenant_id=tenantId,
        )],
        enabled_for_deployment=True,
        enabled_for_disk_encryption=True,
        enabled_for_template_deployment=True,
        sku=keyvault.SkuArgs(
            family="A",
            name="standard",
        ),
    tenant_id=tenantId,
    ),
    resource_group_name=resource_group.name,
    vault_name="nwkvault45") #change the vault name

# Export the primary key of the Storage Account
primary_key = (
    pulumi.Output.all(resource_group.name, account.name)
    .apply(
        lambda args: storage.list_storage_account_keys(
            resource_group_name=args[0], account_name=args[1]
        )
    )
    .apply(lambda accountKeys: accountKeys.keys[0].value)
)

pulumi.export("primary_storage_key", primary_key)