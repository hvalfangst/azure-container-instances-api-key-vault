from typing import Any, Dict

from azure.core.credentials import AzureNamedKeyCredential
from azure.core.paging import ItemPaged
from azure.data.tables import TableServiceClient, TableEntity
from config.module import AzureStorageAccountTablesConfig


class HeroesRepository:
    def __init__(self, credential: AzureNamedKeyCredential, config: AzureStorageAccountTablesConfig) -> None:
        self.service = TableServiceClient(endpoint=config.endpoint, credential=credential)
        self.table = self.service.get_table_client(config.table_name)
        self.partition_key = config.partition_key
        self.filter = config.filter_query_all_heroes

    def get(self, row_key: str) -> TableEntity:
        return self.table.get_entity(partition_key=self.partition_key, row_key=row_key)

    def list(self) -> ItemPaged[TableEntity]:
        return self.table.query_entities(query_filter=self.filter)

    def create(self, row_key: int, data: Dict[str, Any]) -> Dict[str, Any]:
        entity_data = {
            "PartitionKey": self.partition_key,
            "RowKey": str(row_key),
            **data
        }
        return self.table.create_entity(entity=entity_data)

    def delete(self, row_key: str) -> None:
        self.table.delete_entity(partition_key=self.partition_key, row_key=row_key)


class HeroPayloadConverter:
    @staticmethod
    def to_dict(request_json: Any) -> Dict[str, Any]:
        return {
            "Name": request_json.get('hero_name'),
            "Class": request_json.get('hero_class'),
            "Damage": request_json.get('hero_damage')
        }
