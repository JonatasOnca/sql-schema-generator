import logging
from libs.import_files import ImportCSV

def main(argv=None):
    database = []
    obj = ImportCSV()
    database = obj.import_files_database()

    print(database)

if __name__=="__main__":
    logging.info(f"Iniciando a Geração dos SQLs e Schemas")
    main()
    logging.info(f"Finalizando a Geração dos SQLs e Schemas")