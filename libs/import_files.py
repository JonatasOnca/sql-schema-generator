# Copyright 2025 TecOnca Data Solutions.

from operator import itemgetter 
from itertools import groupby 
import csv
import os

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ImportCSV():

    def __init__(self, *args, **kwargs) -> None:
        self.template = f"{PARENT_DIR}/files/database"
    
    """

    """
    def import_files_database(self):
        list_of_files = []

        for diretorio, subpastas, arquivos in os.walk(self.template):
            for arquivo in arquivos:
                file = os.path.join(os.path.realpath(diretorio), arquivo)
                with open(f"{file}",  mode='r', encoding='utf-8-sig') as file:
                    reader = list(csv.reader(file, delimiter=","))
                    data = [tuple(row) for row in reader]
                    file.close()
  
                K = 0
                data.sort() 
                settings_csv = list(tuple(sub) for idx, sub in groupby(data, key = itemgetter(K))) 
                files = []
                tables = []
                for _table in settings_csv:
                    fields = []
                    fields_details = []
                    keys = []
                    primary_keys = []
                    for item in _table:
                        fields.append((item[1],))
                        fields_details.append((item[1], item[2], item[3], item[4], item[5]))
                        if item[3] != '':
                            keys.append((item[1],))
                        if 'PRIMARY' in item[3] or 'UNIQUE' in item[3]:
                            primary_keys.append((item[1],))
                    
                    _fields = [t for t in (set(tuple(i) for i in fields))]
                    _fields_details = [t for t in (set(tuple(i) for i in fields_details))]
                    _keys = [t for t in (set(tuple(i) for i in keys))]
                    _primary_keys = [t for t in (set(tuple(i) for i in primary_keys))]
                    
                    table = {
                        "table": item[0],
                        "fields_details": _fields_details,
                        "fields": _fields,
                        "keys": _keys,
                        "primary_keys": _primary_keys,
                    }
                    tables.append(table)
                files = {
                    "file": arquivo[:-4],
                    "tables": tables
                }
                list_of_files.append(files)
        return list_of_files