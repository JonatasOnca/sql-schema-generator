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

    def generate_table_schema(self, base, table):
        base_table = table.get('table')
        fields_type = table.get('fields_details')
        fields = []
        for item in fields_type:
            fields.append({
                            "mode": "NULLABLE",
                            "name": item[0],
                            "type": get_correct_type_schema(item[1]),
                            "description": item[3] 
                            })   
        os.makedirs(f"SCHEMA/{base}/", exist_ok=True)
        schema_filename = f'{base_table}.json'
        filename =f"SCHEMA/{base}/" + schema_filename
        self.write_schema(fields, filename) 
        return None

    def write_schema(self, fields, filename):
        generated_sql_file = open(
            Path.joinpath(
                Path(__file__).resolve().parents[1], filename), "w")
        json.dump(fields, generated_sql_file, indent=4, ensure_ascii=False)
        generated_sql_file.close()
        return None
