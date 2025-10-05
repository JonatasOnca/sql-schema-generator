# Copyright 2025 TecOnca Data Solutions.


import logging
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import os 

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class YAMLGenerator():

    def __init__(self) -> None:
        self.template = f"{PARENT_DIR}/templates"

    def generate_tables_config(        
        self,
        database_name,
        database,
    ):
        os.makedirs(f"_YAML/{database_name}", exist_ok=True)
        template_name = "tables-config.yaml" 
        file_loader = FileSystemLoader(self.template)
        env = Environment(loader=file_loader)
        template = env.get_template(template_name)
        try:  
            msg = template.render(database=database)

            generated_dag_file = open(
                Path.joinpath(
                    Path(__file__).resolve().parents[1], f"_YAML/{database_name}/{template_name}"), "w")
            generated_dag_file.write(msg)
            generated_dag_file.close()


        except Exception as a:
            logging.error(f"TECHNICAL Error: {a}")
            raise Exception(f"TECHNICAL Error: {a}")
