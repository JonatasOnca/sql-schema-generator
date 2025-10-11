# Copyright 2025 TecOnca Data Solutions.


import logging
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import csv
from collections import defaultdict

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class YAMLGenerator():

    def __init__(self) -> None:
        pass

    def generate_tables_config(        
        self,
        database_name, 
        database
    ):
        os.makedirs(f"_YAML/tables-config/{database_name}", exist_ok=True)
        template_name = "tables-config.yaml" 
        file_loader = FileSystemLoader(f"{PARENT_DIR}/templates")
        env = Environment(loader=file_loader)
        template = env.get_template(template_name)
        try:  
            msg = template.render(database=database)

            generated_dag_file = open(
                Path.joinpath(
                    Path(__file__).resolve().parents[1], f"_YAML/tables-config/{database_name}/{template_name}"), "w")
            generated_dag_file.write(msg)
            generated_dag_file.close()


        except Exception as a:
            logging.error(f"TECHNICAL Error: {a}")
            raise Exception(f"TECHNICAL Error: {a}")

    def generate_chunks_config(        
        self,
        database_name, 
    ):
        os.makedirs(f"_YAML/chunks-config/{database_name}", exist_ok=True)
        template_name = "chunks-config.yaml" 
        file_loader = FileSystemLoader(f"{PARENT_DIR}/templates")
        env = Environment(loader=file_loader)
        template = env.get_template(template_name)

        files = f"{PARENT_DIR}/files/chunks-config"
        for diretorio, subpastas, arquivos in os.walk(files):
            for arquivo in arquivos:
                if arquivo[:-4] == database_name:
                    file = os.path.join(os.path.realpath(diretorio), arquivo)
                    with open(f"{file}",  mode='r', encoding='utf-8-sig') as file:
                        reader = list(csv.reader(file, delimiter=","))
                        arquivo_csv = [tuple(row) for row in reader]
                        file.close()

                    grupos_de_tabelas = defaultdict(list)
                    tabelas = []
                    for linha in arquivo_csv:
                        # Evita erros se houver linhas em branco
                        if not linha:
                            continue

                        tabela = linha[0]
                        grupo = linha[1]

                        # Adiciona a tabela à lista correspondente ao seu grupo.
                        # Não é preciso verificar se a chave 'grupo' já existe!
                        tabelas.append(tabela)
                        grupos_de_tabelas[grupo].append(tabela)


                    try:  
                        msg = template.render(tabelas=tabelas, grupos_de_tabelas=grupos_de_tabelas)

                        generated_dag_file = open(
                            Path.joinpath(
                                Path(__file__).resolve().parents[1], f"_YAML/chunks-config/{database_name}/{template_name}"), "w")
                        generated_dag_file.write(msg)
                        generated_dag_file.close()


                    except Exception as a:
                        logging.error(f"TECHNICAL Error: {a}")
                        raise Exception(f"TECHNICAL Error: {a}")
