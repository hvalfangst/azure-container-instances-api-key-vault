import os

from azure.core.credentials import AzureNamedKeyCredential

account_name = "hvalfangststorageaccount"
table_name = "hvalfangststoragetable"
endpoint = f"https://{account_name}.table.core.windows.net"
partition_key = "Heroes"
filter_query_all_heroes = "PartitionKey eq 'Heroes'"


def get_credential() -> AzureNamedKeyCredential:
    access_key = os.environ.get("ACCESS_KEY")

    if access_key is None:
        raise ValueError("Environment variable CONFIG_FILE_PATH is not set.")

    return AzureNamedKeyCredential(account_name, access_key)
