# Copyright 2025 TecOnca Data Solutions.


import logging
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os

from libs.type_data import _STRING, _DATE, _INTEGER, _BOOL, _NUMERIC

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_correct_type_schema(field: str):

    if field in _STRING:
        return 'STRING'
    if field in _DATE:
        return 'TIMESTAMP'
    elif field in _INTEGER + _BOOL:
        return 'INTEGER'
    elif field in _NUMERIC:
        return 'NUMERIC'
    else:
        return field

class MappingFunctionsGenerator():

    def __init__(self) -> None:
        self.template = f"{PARENT_DIR}/templates"
    

    def generate_mapping_functions(        
        self,
        database_name,
        database,
    ):

        os.makedirs(f"_MAPPING/{database_name}", exist_ok=True)
        template_name = "transform_functions.py" 
        file_loader = FileSystemLoader(self.template)
        env = Environment(loader=file_loader)
        template = env.get_template(template_name)
        try:  
            msg = template.render(database=database, string=_STRING, date=_DATE, integer=_INTEGER + _BOOL, decimal=_NUMERIC)

            generated_dag_file = open(
                Path.joinpath(
                    Path(__file__).resolve().parents[1], f"_MAPPING/{database_name}/{template_name}"), "w")
            generated_dag_file.write(msg)
            generated_dag_file.close()


        except Exception as a:
            logging.error(f"TECHNICAL Error: {a}")
            raise Exception(f"TECHNICAL Error: {a}")
