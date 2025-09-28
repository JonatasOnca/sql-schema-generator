import logging
from string import Template
from pathlib import Path
import json

import os

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DESCRIPTION_DIR = f"{PARENT_DIR}/template_sql"

_INTEGER = [
    'int',
    'int64',
    'integer',
    'numeric',
    'bigint',
    'mediumint',
    'smallint',
    'tinyint',
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

_DATE = [
    'smalldatetime',
    'datetime',
    'datetime2',
    'date',
    'time',
    'timestamp',
    'year',
]

_FLOAT = [
    'dec',
    'decimal',
    'double precision',
    'double',
    'float',
]

def get_correct_type_schema(field: str):

    if field in _STRING + _DATE:
        return 'STRING'
    elif field in _INTEGER + _BOOL:
        return 'INTEGER'
    elif field in _FLOAT:
        return 'FLOAT'
    else:
        return field

def get_correct_type_from_rdbms(field: str):

    if field in _INTEGER:
        return 'BIGINT'
    elif field in _BOOL:
        return 'INTEGER'
    elif field in _STRING:
        return 'VARCHAR'
    elif field in _DATE:
        return 'VARCHAR'
    elif field in _FLOAT:
        return 'DECIMAL'
    else:
        return field

def get_correct_type_to_bigquery(field: str):

    if field in _INTEGER:
        return 'INTEGER'
    elif field in _BOOL:
        return 'BOOLEAN'
    elif field in _STRING:
        return 'STRING'
    elif field in _DATE:
        return 'DATETIME'
    elif field in _FLOAT:
        return 'DECIMAL'
    else:
        return field


class QueryGenerator():

    def __init__(self) -> None:
        pass

    def generate_template(
        self, 
        base_table, 
        source_table,
        target_table,
        p_key,
        fields,
        values,
        update_fields,
        keys,
        p_key_sub_query,
        incremental_field,
        recordstamp,
        join_key,
        incremental_field_merge,
        format_date
    ):

        sql_template = Template(sql_template_file.read())

        generated_sql_template = sql_template.substitute(
            base_table=f"{source_table}.{base_table}",
            target_table=f"{target_table}.{base_table}",
            p_key=p_key,
            fields=fields,
            update_fields=update_fields,
            keys=", ".join(keys),
            p_key_sub_query=p_key_sub_query,
            incremental_field=incremental_field,
            recordstamp = recordstamp,
            join_key = join_key,
            values=values,
            incremental_field_merge=incremental_field_merge,
            format_date=format_date,
            )

        return generated_sql_template   

 
    def generate_sql_database(
        self,
        source,
        settings,
        table,
    ):
        keys = table.get('all_keys')
        fields = table.get('fields')
        recordstamp = table.get('recordstamp')

        if not fields:
            print(f"Schema could not be retrieved for {source}")
        
        for dag in ['backfill', 'ELT']:
            self.generate_database(
                table=table,
                fields=fields,
                recordstamp=recordstamp,
                dag=dag,
                settings=settings,
                source=source,
                keys=keys,
            )
    

    def generate_database(
        self,
        table,
        fields,
        recordstamp,
        source
    ):
        try:
            base_table = table["base_table"]
            sanitize = fields.split(',')
            
            if dag == 'backfill':
                TEMPLATE_ELT = f'sql_template_{dag.lower()}.sql'

                if strategy == 'DIMENSION_TYPE2': 
                    TEMPLATE_ELT = f'sql_template_{dag.lower()}_all.sql'

                if recordstamp == '_PARTITIONTIME': 
                    TEMPLATE_ELT = f'sql_template_{dag.lower()}_all.sql'

            else:
                if recordstamp == '_PARTITIONTIME': 
                    TEMPLATE_ELT = f'sql_template_{dag.lower()}_all.sql'
                else:
                    TEMPLATE_ELT = f'sql_template_{dag.lower()}.sql'

            sanitize = list(map(lambda item: item.strip().replace("`",""), sanitize))

            with open(f"{os.getcwd()}/template_sql/{TEMPLATE_ELT}", 'r') as template:
                text = Template(template.read())
                template.close()
            
            update_field = ''
            create_field = ''

            exclution_list = ['validFromCtrl', 'validToCtrl', 'currentCtrl', 'isDeleted', 'insertionDateTime']
            _sanitize = []
            for key in sanitize:
                if key not in exclution_list:
                    _sanitize.append(key)

            result = text.substitute(
                fields = ",\n ".join(sanitize),
                table = base_table,
                source = source,
                update = update_field,
                create = create_field
            )

            database_sql_filepath = f"dags/{source}/{dag}/sql/{base_table}/database_{base_table}.sql"

            self.write_sql(database_sql_filepath, result)

        except Exception as a:
            print(f"TECHNICAL Error - Unable to open SQL template or generate SQL: {a}")
            logging.error(f"TECHNICAL Error - Unable to open SQL template or generate SQL: {a}")
            raise Exception(f"TECHNICAL Error - Unable to open SQL template or generate SQL: {a}")


    def generate_table_schema(self, table, source):
        base_table = table.get('base_table')
        fields_type = table.get('fields_type')
        fields = []
        fields_lz = []
        for item in fields_type:
            fields.append({
                            "mode": "NULLABLE",
                            "name": item.get('field'),
                            "type": get_correct_type_schema(item.get('type')),
                            "description": item.get('description') 
                            })
            fields_lz.append({
                            "mode": "NULLABLE",
                            "name": item.get('field'),
                            "type": get_correct_type_schema(item.get('type')),
                            "description": item.get('description') 
                            })
        fields_lz.append({
                            "mode": "NULLABLE",
                            "name": "insertionDateTime",
                            "type": "STRING",
                            "description": "Data e Hora que foi feita a inserção do dado na LZ" 
                        })
        # LANDING ZONE SCHEMA       
        schema_filename = f'{base_table}_landing_zone_schema.json'
        filename =f"dags/{source}/backfill/sql/{base_table}/" + schema_filename
        self.write_schema(fields_lz, filename) 
        return None


    def write_schema(self, fields, filename):
        generated_sql_file = open(
            Path.joinpath(
                Path(__file__).resolve().parents[1], filename), "w")
        json.dump(fields, generated_sql_file, ensure_ascii=False)
        generated_sql_file.close()
        return None

    def write_sql(self, filename: str, file: str):
        generated_sql_file = open(
            Path.joinpath(
                Path(__file__).resolve().parents[1], filename), "w")
        generated_sql_file.write(file)
        generated_sql_file.close()
        return None
