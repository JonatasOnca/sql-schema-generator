# Copyright 2025 TecOnca Data Solutions.

import logging
from pathlib import Path
import json
import os 

_INTEGER = [
    'int',
    'int64',
    'integer',
    'bigint',
    'mediumint',
    'smallint',
    'tinyint',
    'numeric',
]

_BOOL = [
    'bool',
    'boolean',
]

_STRING = [
    'varchar',
    'nvarchar',
    'char',
    'bit',
    'varbinary',
    'binary',
    'tinyblob',
    'tinytext',
    'text',
    'blob',
    'mediumtext',
    'mediumblob',
    'longtext',
    'longblob',
    'enum',
]

_DATE_DATETIME = [
    'smalldatetime',
    'datetime',
    'datetime2',
]

_DATE_DATE = [
    'date',
]

_DATE_TIMESTAMP = [
    'timestamp',
]
_DATE_CUSTOM = [
    'time',
    'year',
]

_DATE = _DATE_DATETIME + _DATE_DATE + _DATE_TIMESTAMP + _DATE_CUSTOM

_NUMERIC = [
    'dec',
    'decimal',
    'double precision',
    'double',
    'float',
]

def get_correct_type_schema(field: str):

    if field in _STRING:
        return 'STRING'
    if field in _DATE_DATE:
        return 'DATE'
    if field in _DATE_TIMESTAMP:
        return 'TIMESTAMP'
    if field in _DATE_DATETIME:
        return 'DATETIME'
    if field in _DATE:
        return 'TIMESTAMP'
    elif field in _INTEGER + _BOOL:
        return 'INTEGER'
    elif field in _NUMERIC:
        return 'NUMERIC'
    else:
        return field


class SchemaGenerator():

    def __init__(self) -> None:
        pass 

    def generate_table_schema(self, database_name, table_name, fields_details):
        try:
            fields_details.sort()
            _fields = []
            for item in fields_details:
                _fields.append({
                                "name": item[0],
                                "mode": "NULLABLE",
                                "type": get_correct_type_schema(item[1]),
                                "description": item[3],
                                "fields": []
                                })   
            os.makedirs(f"SCHEMA/{database_name}/", exist_ok=True)
            schema_filename = f'{table_name}.json'
            filename =f"SCHEMA/{database_name}/" + schema_filename
            schema = {'fields': _fields}
            self.write_schema(schema, filename) 
            return None
        except Exception as a:
            logging.error(f"TECHNICAL Error - Generate SCHEMA: {a}")
            raise Exception(f"TECHNICAL Error - Generate SCHEMA: {a}")

    def write_schema(self, _fields, filename):
        generated_sql_file = open(
            Path.joinpath(
                Path(__file__).resolve().parents[1], filename), "w")
        json.dump(_fields, generated_sql_file, indent=4, ensure_ascii=False)
        generated_sql_file.close()
        return None
