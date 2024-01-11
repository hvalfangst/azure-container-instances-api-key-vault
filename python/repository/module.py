from typing import Any

from azure.core.credentials import AzureNamedKeyCredential
from azure.core.paging import ItemPaged
from azure.data.tables import TableServiceClient, TableClient, TableEntity
from config.module import partition_key, filter_query_all_heroes, endpoint, table_name


def init_heroes_table(credential: AzureNamedKeyCredential) -> TableClient:
    service = TableServiceClient(endpoint=endpoint, credential=credential)
    return service.get_table_client(table_name)


def get_hero(table: TableClient, row_key: str) -> TableEntity:
    return table.get_entity(partition_key=partition_key, row_key=row_key)


def list_heroes(table: TableClient) -> ItemPaged[TableEntity]:
    return table.query_entities(query_filter=filter_query_all_heroes)


def create_hero(table: TableClient, row_key: int, data) -> dict[str, Any]:
    my_entity = new_hero(data=data, key=row_key)
    return table.create_entity(entity=my_entity)


def new_hero(data: dict[str, Any], key: int) -> dict[str, str, dict[str, Any]]:
    """
    Create an entity dictionary for Azure Table Storage.
    """
    return {
        "PartitionKey": partition_key,
        "RowKey": str(key),
        **data
    }


def to_dict(request_json: Any) -> dict[str, Any]:
    """
    Create a payload structure from the request JSON.
    """
    return {
        "Name": request_json['hero_name'],
        "Class": request_json['hero_class'],
        "Damage": request_json['hero_damage']
    }


def delete_hero(table: TableClient, row_key: str):
    table.delete_entity(partition_key=partition_key, row_key=row_key)
