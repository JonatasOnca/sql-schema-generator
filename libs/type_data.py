# Copyright 2025 TecOnca Data Solutions.

from typing import Dict, List

# Definições de tipos de dados
_INTEGER = [
    'int',
    'int64',
    'integer',
    'bigint',
    'mediumint',
    'smallint',
    'tinyint',
]

_BOOL = [
    'bool',
    'boolean',
]

_STRING = [
    'varchar',
    'nvarchar',
    'char',
    'bit',
    'varbinary',
    'binary',
    'tinyblob',
    'tinytext',
    'text',
    'blob',
    'mediumtext',
    'mediumblob',
    'longtext',
    'longblob',
    'enum',
]

_DATE_DATETIME = [
    'smalldatetime',
    'datetime',
    'datetime2',
]

_DATE_DATE = [
    'date',
]

_DATE_TIMESTAMP = [
    'timestamp',
]

_DATE_CUSTOM = [
    'time',
    'year',
]

_DATE = _DATE_DATETIME + _DATE_DATE + _DATE_TIMESTAMP + _DATE_CUSTOM

_NUMERIC = [
    'numeric',
    'dec',
    'decimal',
    'double precision',
    'double',
    'float',
]

_JSON = [
    'json',
]

class TypeMapper:
    """Classe para mapeamento de tipos entre diferentes bancos de dados"""
    
    def __init__(self):
        self._mysql_types = {
            'string': 'VARCHAR',
            'integer': 'INT',
            'bigint': 'BIGINT',
            'decimal': 'DECIMAL',
            'float': 'FLOAT',
            'double': 'DOUBLE',
            'date': 'DATE',
            'datetime': 'DATETIME',
            'timestamp': 'TIMESTAMP',
            'boolean': 'BOOLEAN',
            'text': 'TEXT',
            'json': 'JSON'
        }
        
        self._postgresql_types = {
            'string': 'VARCHAR',
            'integer': 'INTEGER',
            'bigint': 'BIGINT',
            'decimal': 'DECIMAL',
            'float': 'REAL',
            'double': 'DOUBLE PRECISION',
            'date': 'DATE',
            'datetime': 'TIMESTAMP',
            'timestamp': 'TIMESTAMP',
            'boolean': 'BOOLEAN',
            'text': 'TEXT',
            'json': 'JSONB'
        }
        
        self._sqlserver_types = {
            'string': 'NVARCHAR',
            'integer': 'INT',
            'bigint': 'BIGINT',
            'decimal': 'DECIMAL',
            'float': 'FLOAT',
            'double': 'FLOAT',
            'date': 'DATE',
            'datetime': 'DATETIME2',
            'timestamp': 'DATETIME2',
            'boolean': 'BIT',
            'text': 'NVARCHAR(MAX)',
            'json': 'NVARCHAR(MAX)'
        }
    
    def get_generic_type(self, field_type: str) -> str:
        """Retorna o tipo genérico baseado no tipo de entrada"""
        field_type_lower = field_type.lower()
        
        if field_type_lower in [t.lower() for t in _STRING]:
            return 'string'
        elif field_type_lower in [t.lower() for t in _INTEGER]:
            return 'integer' if field_type_lower != 'bigint' else 'bigint'
        elif field_type_lower in [t.lower() for t in _BOOL]:
            return 'boolean'
        elif field_type_lower in [t.lower() for t in _NUMERIC]:
            if 'float' in field_type_lower:
                return 'float'
            elif 'double' in field_type_lower:
                return 'double'
            else:
                return 'decimal'
        elif field_type_lower in [t.lower() for t in _DATE]:
            if field_type_lower == 'date':
                return 'date'
            elif field_type_lower in ['timestamp']:
                return 'timestamp'
            else:
                return 'datetime'
        elif field_type_lower in [t.lower() for t in _JSON]:
            return 'json'
        else:
            return 'string'  # Fallback
    
    def get_mysql_type(self, field_type: str) -> str:
        """Retorna o tipo MySQL correspondente"""
        generic_type = self.get_generic_type(field_type)
        return self._mysql_types.get(generic_type, 'VARCHAR')
    
    def get_postgresql_type(self, field_type: str) -> str:
        """Retorna o tipo PostgreSQL correspondente"""
        generic_type = self.get_generic_type(field_type)
        return self._postgresql_types.get(generic_type, 'VARCHAR')
    
    def get_sqlserver_type(self, field_type: str) -> str:
        """Retorna o tipo SQL Server correspondente"""
        generic_type = self.get_generic_type(field_type)
        return self._sqlserver_types.get(generic_type, 'NVARCHAR')
    
    def get_bigquery_type(self, field_type: str) -> str:
        """Retorna o tipo BigQuery correspondente (para schemas)"""
        generic_type = self.get_generic_type(field_type)
        
        mapping = {
            'string': 'STRING',
            'integer': 'INTEGER',
            'bigint': 'INTEGER',
            'decimal': 'NUMERIC',
            'float': 'FLOAT',
            'double': 'FLOAT',
            'date': 'DATE',
            'datetime': 'TIMESTAMP',
            'timestamp': 'TIMESTAMP',
            'boolean': 'BOOLEAN',
            'text': 'STRING',
            'json': 'JSON'
        }
        
        return mapping.get(generic_type, 'STRING')