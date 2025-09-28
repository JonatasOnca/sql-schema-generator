import logging
from libs.import_files import ImportCSV
from libs.generate_query import QueryGenerator
from libs.generate_schema import SchemaGenerator


def main(argv=None):
    databases = []
    obj = ImportCSV()
    databases = obj.import_files_database()

    Schema = SchemaGenerator()
    

    try:
        for database in databases:
            base = database.get('file')
            for table in database.get('tables'):
                Schema.generate_table_schema(base, table)
    
    except Exception as a:
        logging.error(f"Error: {a}")
        raise Exception(f"Error: {a}")

if __name__=="__main__":
    logging.info(f"Iniciando a Geração dos SQLs e Schemas")
    main()
    logging.info(f"Finalizando a Geração dos SQLs e Schemas")