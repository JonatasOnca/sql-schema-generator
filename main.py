# Copyright 2025 TecOnca Data Solutions.


import logging
from generator import generator

def main(argv=None):
    try:
        generator()
    except Exception as a:
        logging.error(f"Error: {a}")
        raise Exception(f"Error: {a}")

if __name__=="__main__":
    logging.info(f"Iniciando...")
    main()
    logging.info(f"Finalizando...")