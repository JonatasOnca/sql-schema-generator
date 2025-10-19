# Copyright 2025 TecOnca Data Solutions.


import logging
from libs.import_files import ImportCSV
from libs.generate_query import QueryGenerator
from libs.generate_schema import SchemaGenerator
from libs.generate_transform_functions import MappingFunctionsGenerator
from libs.generate_yaml import YAMLGenerator

def generator(argv=None):
    tables_config = []
    obj = ImportCSV()
    tables_config = obj.import_files_tables_config()

    ObjQuery = QueryGenerator()
    ObjSchema = SchemaGenerator()
    ObjMappingFunctions = MappingFunctionsGenerator()
    ObjYAML = YAMLGenerator()

    try:
        for database in tables_config:
            database_name = database.get('file')
            for table in database.get('tables'):
                table_name = table.get('table')
                fields_details = table.get('fields_details')
                ObjQuery.generate_table_sql(database_name, table_name, fields_details)
                ObjSchema.generate_table_schema(database_name, table_name, fields_details)
            
            ObjMappingFunctions.generate_mapping_functions(database_name, database)
            ObjYAML.generate_tables_config(database_name, database)
            ObjYAML.generate_chunks_config(database_name)

    except Exception as a:
        logging.error(f"Error: {a}")
        raise Exception(f"Error: {a}")

if __name__=="__main__":
    logging.info(f"Iniciando a Geração dos SQLs e Schemas")
    main()
    logging.info(f"Finalizando a Geração dos SQLs e Schemas")