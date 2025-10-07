# Copyright 2025 TecOnca Data Solutions.


import logging
from string import Template
from pathlib import Path

import os
from libs.type_data import _STRING, _DATE_DATE, _DATE_TIMESTAMP, _DATE_DATETIME, _DATE, _INTEGER, _BOOL, _NUMERIC

def get_correct_type_by_database(
        database: str = 'MySQL', 
        field_type: str = None
    ):

    if database == 'MySQL':
        if field_type in _STRING:
            return 'CHAR'
        if field_type in _DATE:
            return 'TIMESTAMP'
        elif field_type in _INTEGER + _BOOL:
            return 'SIGNED'
        elif field_type in _NUMERIC:
            return 'DECIMAL'
        else:
            return field_type
    
def cast_on_select(
        database: str = 'MySQL',
        field_name: str = None,
        field_type: str = None,
        field_mask: str = '%Y-%m-%d %H:%i:%s.%f',

):
    if field_name == 'option':
        return f'CAST(`option` AS  CHAR) AS `option`'
    elif field_name == 'order':
        return f'CAST(`order` AS CHAR) AS `order`'
    else:
        return f'CAST({field_name} AS CHAR) AS {field_name}'
    
    # if database == 'MySQL' and field_type in _DATE:
    #     return f'CAST({field_name} AS CHAR) AS {field_name}'
    # else:
    #     if field_name == 'option':
    #         return f'CAST(`option` AS {get_correct_type_by_database(database, field_type)}) AS `option`'
    #     elif field_name == 'order':
    #         return f'CAST(`order` AS {get_correct_type_by_database(database, field_type)}) AS `order`'
    #     return f'CAST({field_name} AS {get_correct_type_by_database(database, field_type)}) AS {field_name}'

class QueryGenerator():

    def __init__(self) -> None:
        pass
    

    def generate_table_sql(
        self,
        database_name, 
        table_name, 
        fields_details
    ):
        try:
            fields_details.sort()
            sanitize = [cast_on_select('MySQL', item[0], item[1], item[4]) for item in fields_details]
            with open(f"{os.getcwd()}/templates/sql.sql", 'r') as template:
                text = Template(template.read())
                template.close()

                result = text.substitute(
                    _fields = ",\n    ".join(sanitize),
                    _database_name=database_name,
                    _table_name = table_name,
                )

                sql_filename = f'{table_name}.sql'
                os.makedirs(f"_SQL/{database_name}/", exist_ok=True)
                filename =f"_SQL/{database_name}/" + sql_filename

                self.write_sql(filename, result)

        except Exception as a:
            logging.error(f"TECHNICAL Error - Unable to open SQL template or generate SQL: {a}")
            raise Exception(f"TECHNICAL Error - Unable to open SQL template or generate SQL: {a}")

    def write_sql(self, filename: str, file: str):
        generated_sql_file = open(
            Path.joinpath(
                Path(__file__).resolve().parents[1], filename), "w")
        generated_sql_file.write(file)
        generated_sql_file.close()
        return None