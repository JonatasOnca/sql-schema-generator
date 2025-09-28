import logging
from string import Template
from pathlib import Path

import os

_TYPE = [
    'sql',
]

class QueryGenerator():

    def __init__(self) -> None:
        pass
    

    def generate_table_sql(
        self,
        database_name, 
        table_name, 
        fields
    ):
        try:
            fields.sort()
            sanitize = ','.join([item[0] for item in fields])
            sanitize = sanitize.split(',')

            for item in _TYPE:
                with open(f"{os.getcwd()}/sql-templates/{item}.sql", 'r') as template:
                    text = Template(template.read())
                    template.close()

                result = text.substitute(
                    _fields = ",\n    ".join(sanitize),
                    _database_name=database_name,
                    _table_name = table_name,
                )

                sql_filename = f'{table_name}_{item}.sql'
                os.makedirs(f"SQL/{database_name}/", exist_ok=True)
                filename =f"SQL/{database_name}/" + sql_filename

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