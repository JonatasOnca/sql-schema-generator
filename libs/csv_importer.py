# Copyright 2025 TecOnca Data Solutions.

import csv
import logging
from operator import itemgetter 
from itertools import groupby 
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

from config import Config
from logger_config import FileProcessingError

@dataclass
class TableField:
    """Representa um campo de tabela"""
    name: str
    data_type: str
    constraints: str
    description: str
    mask: str
    filter_flag: str

@dataclass
class TableConfig:
    """Representa a configuração de uma tabela"""
    name: str
    fields: List[str]
    fields_details: List[Tuple]
    keys: List[str]
    primary_keys: List[str]
    unique_keys: List[str]
    foreign_keys: List[str]
    field_where: List[str]
    partition_id: List[str]

class CSVImporter:
    """Importador melhorado de arquivos CSV de configuração"""
    
    def __init__(self, tables_config_dir: Path = None):
        self.tables_config_dir = tables_config_dir or Config.TABLES_CONFIG_DIR
        self.logger = logging.getLogger(__name__)
    
    def import_tables_config(self) -> List[Dict[str, Any]]:
        """
        Importa configurações de tabelas de arquivos CSV
        
        Returns:
            Lista de configurações de bancos de dados com suas tabelas
        """
        try:
            csv_files = list(self.tables_config_dir.glob("*.csv"))
            if not csv_files:
                raise FileProcessingError(f"Nenhum arquivo CSV encontrado em {self.tables_config_dir}")
            
            databases_config = []
            
            for csv_file in csv_files:
                self.logger.info(f"Processando arquivo: {csv_file.name}")
                
                # Lê e processa o CSV
                raw_data = self._read_csv_file(csv_file)
                tables_data = self._group_data_by_table(raw_data)
                tables_config = self._process_tables_data(tables_data)
                
                database_config = {
                    "file": csv_file.stem,  # Nome do arquivo sem extensão
                    "tables": tables_config
                }
                databases_config.append(database_config)
            
            return databases_config
            
        except Exception as e:
            self.logger.error(f"Erro ao importar configurações de tabelas: {e}")
            raise FileProcessingError(f"Erro ao importar configurações: {e}")
    
    def _read_csv_file(self, csv_file: Path) -> List[Tuple]:
        """Lê um arquivo CSV e retorna os dados como lista de tuplas"""
        try:
            with open(csv_file, mode='r', encoding='utf-8-sig') as file:
                reader = csv.reader(file, delimiter=",")
                return [tuple(row) for row in reader if row]  # Remove linhas vazias
        except Exception as e:
            raise FileProcessingError(f"Erro ao ler arquivo {csv_file}: {e}")
    
    def _group_data_by_table(self, raw_data: List[Tuple]) -> List[List[Tuple]]:
        """Agrupa os dados por nome da tabela"""
        raw_data.sort()  # Ordena por nome da tabela (primeira coluna)
        return [list(group) for _, group in groupby(raw_data, key=itemgetter(0))]
    
    def _process_tables_data(self, tables_data: List[List[Tuple]]) -> List[Dict[str, Any]]:
        """Processa os dados agrupados por tabela e cria as configurações"""
        tables_config = []
        
        for table_rows in tables_data:
            if not table_rows:
                continue
                
            table_name = table_rows[0][0]
            self.logger.debug(f"Processando tabela: {table_name}")
            
            table_config = self._create_table_config(table_rows)
            tables_config.append(table_config.to_dict())
        
        return tables_config
    
    def _create_table_config(self, table_rows: List[Tuple]) -> TableConfig:
        """Cria a configuração de uma tabela a partir das suas linhas"""
        table_name = table_rows[0][0]
        
        # Inicializa listas
        fields = []
        fields_details = []
        keys = []
        primary_keys = []
        unique_keys = []
        foreign_keys = []
        field_where = []
        partition_id = []
        
        for row in table_rows:
            if len(row) < 6:
                self.logger.warning(f"Linha incompleta ignorada para tabela {table_name}: {row}")
                continue
            
            field_name = row[1]
            data_type = row[2]
            constraints = row[3] if len(row) > 3 else ""
            description = row[4] if len(row) > 4 else ""
            mask = row[5] if len(row) > 5 else ""
            filter_flag = row[6] if len(row) > 6 else ""
            
            # Adiciona field básico
            fields.append(field_name)
            fields_details.append((field_name, data_type, constraints, description, mask, filter_flag))
            
            # Processa constraints
            if constraints:
                keys.append(field_name)
                if 'PRIMARY' in constraints.upper():
                    primary_keys.append(field_name)
                if 'UNIQUE' in constraints.upper():
                    unique_keys.append(field_name)
                if 'FOREIGN KEY' in constraints.upper():
                    foreign_keys.append(field_name)
            
            # Processa filtros e particionamento
            if filter_flag == 'X':
                field_where.extend([field_name, mask, data_type])
                partition_id.extend(['DAY', field_name])
        
        # Remove duplicatas mantendo ordem
        fields = list(dict.fromkeys(fields))
        keys = list(dict.fromkeys(keys))
        primary_keys = list(dict.fromkeys(primary_keys))
        unique_keys = list(dict.fromkeys(unique_keys))
        foreign_keys = list(dict.fromkeys(foreign_keys))
        
        return TableConfig(
            name=table_name,
            fields=sorted(fields),
            fields_details=sorted(fields_details),
            keys=sorted(keys),
            primary_keys=sorted(primary_keys),
            unique_keys=sorted(unique_keys),
            foreign_keys=sorted(foreign_keys),
            field_where=field_where,
            partition_id=partition_id or ['DAY']
        )

# Extensão da dataclass para incluir método to_dict
def to_dict(self) -> Dict[str, Any]:
    """Converte o TableConfig para dicionário"""
    return {
        "table": self.name,
        "fields": [(f,) for f in self.fields],
        "fields_details": self.fields_details,
        "keys": self.keys,
        "primary_keys": self.primary_keys,
        "unique_keys": self.unique_keys,
        "foreign_keys": self.foreign_keys,
        "field_where": self.field_where,
        "partition_id": self.partition_id
    }

# Adiciona o método à classe
TableConfig.to_dict = to_dict