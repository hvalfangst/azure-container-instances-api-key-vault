import os
from azure.core.credentials import AzureNamedKeyCredential


class AzureStorageAccountTablesConfig:
    def __init__(self, account_name: str, table_name: str, partition_key: str):
        self.account_name = account_name
        self.table_name = table_name
        self.endpoint = f"https://{account_name}.table.core.windows.net"
        self.partition_key = partition_key
        self.filter_query_all_heroes = f"PartitionKey eq '{partition_key}'"


class AzureCredentials:
    @staticmethod
    def get_credential(account_name: str) -> AzureNamedKeyCredential:
        access_key = os.environ.get("ACCESS_KEY")

        if access_key is None:
            raise ValueError(f"Environment variable 'ACCESS_KEY' is not set.")

        return AzureNamedKeyCredential(account_name, access_key)
