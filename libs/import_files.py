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
                    unique_keys = []
                    foreign_keys = []

                    field_where = []
                    partition_id = []
                    table_name = ''
                    for item in _table:
                        table_name = item[0]
                        fields.append((item[1],))
                        fields_details.append((item[1], item[2], item[3], item[4], item[5], item[6]))
                        if item[3] != '':
                            keys.append(item[1])
                        if 'PRIMARY' in item[3]:
                            primary_keys.append(item[1])
                        if 'UNIQUE' in item[3]:
                            unique_keys.append(item[1])
                        if 'FOREIGN KEY' in item[3]:
                            foreign_keys.append(item[1])
                        if item[6] == 'X':
                            field_where.append(item[1])
                            field_where.append(item[5])
                            field_where.append(item[2])
                        if item[6] == 'X':
                            partition_id.append(item[1])  
                            partition_id.append('DAY')                    
                    # _fields = [t for t in (set(tuple(i) for i in fields))]
                    # _fields_details = [t for t in (set(tuple(i) for i in fields_details))]
                    # _keys = [t for t in (set(tuple(i) for i in keys))]
                    # _primary_keys = [t for t in (set(tuple(i) for i in primary_keys))]
                    # _unique_keys = [t for t in (set(tuple(i) for i in unique_keys))]
                    # _foreign_keys = [t for t in (set(tuple(i) for i in foreign_keys))]

                    table = {
                        "table": table_name,
                        "fields": sorted(fields),
                        "fields_details": sorted(fields_details),
                        "keys": sorted(keys),
                        "primary_keys": sorted(primary_keys),
                        "unique_keys": sorted(unique_keys),
                        "foreign_keys": sorted(foreign_keys),
                        "field_where": field_where,
                        "partition_id": partition_id  or ['_PARTITIONTIME', 'DAY']
                    }
                    tables.append(table)
                files = {
                    "file": arquivo[:-4],
                    "tables": tables
                }
                list_of_files.append(files)
        return list_of_files