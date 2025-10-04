# Copyright 2025 TecOnca Data Solutions.

import logging
from libs.import_files import ImportCSV
from libs.generate_query import QueryGenerator
from libs.generate_schema import SchemaGenerator
from libs.generate_mapping_functions import MappingFunctionsGenerator


def main(argv=None):
    databases = []
    obj = ImportCSV()
    databases = obj.import_files_database()

    Query = QueryGenerator()
    Schema = SchemaGenerator()
    MappingFunctions = MappingFunctionsGenerator()

    try:
        for database in databases:
            database_name = database.get('file')
            for table in database.get('tables'):
                table_name = table.get('table')
                fields_details = table.get('fields_details')
                Query.generate_table_sql(database_name, table_name, fields_details)
                Schema.generate_table_schema(database_name, table_name, fields_details)
            
            MappingFunctions.generate_mapping_functions(database_name, database)
        

    except Exception as a:
        logging.error(f"Error: {a}")
        raise Exception(f"Error: {a}")

if __name__=="__main__":
    logging.info(f"Iniciando a Geração dos SQLs e Schemas")
    main()
    logging.info(f"Finalizando a Geração dos SQLs e Schemas")