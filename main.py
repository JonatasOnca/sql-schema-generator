import logging
from libs.import_files import ImportCSV
from libs.generate_query import QueryGeneratorTemplate

def main(argv=None):
    databases = []
    obj = ImportCSV()
    databases = obj.import_files_database()

    temp = QueryGeneratorTemplate()
    

    try:
        for database in databases:
            # print(database['file'])
            # print(database['tables'])
            for table in database.get('tables'):
                temp.generate_table_schema(table)
    
    except Exception as a:
        logging.error(f"Error: {a}")
        raise Exception(f"Error: {a}")

if __name__=="__main__":
    logging.info(f"Iniciando a Geração dos SQLs e Schemas")
    main()
    logging.info(f"Finalizando a Geração dos SQLs e Schemas")