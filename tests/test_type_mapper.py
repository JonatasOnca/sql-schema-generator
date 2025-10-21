# Copyright 2025 TecOnca Data Solutions.

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from libs.type_data import TypeMapper

class TestTypeMapper(unittest.TestCase):
    
    def setUp(self):
        """Setup para cada teste"""
        self.mapper = TypeMapper()
    
    def test_generic_type_mapping(self):
        """Testa mapeamento para tipos genéricos"""
        assert self.mapper.get_generic_type('varchar') == 'string'
        assert self.mapper.get_generic_type('int') == 'integer'
        assert self.mapper.get_generic_type('bigint') == 'bigint'
        assert self.mapper.get_generic_type('bool') == 'boolean'
        assert self.mapper.get_generic_type('date') == 'date'
        assert self.mapper.get_generic_type('timestamp') == 'timestamp'
        assert self.mapper.get_generic_type('decimal') == 'decimal'
        assert self.mapper.get_generic_type('json') == 'json'
    
    def test_mysql_type_mapping(self):
        """Testa mapeamento para MySQL"""
        assert self.mapper.get_mysql_type('varchar') == 'VARCHAR'
        assert self.mapper.get_mysql_type('int') == 'INT'
        assert self.mapper.get_mysql_type('bool') == 'BOOLEAN'
        assert self.mapper.get_mysql_type('json') == 'JSON'
    
    def test_postgresql_type_mapping(self):
        """Testa mapeamento para PostgreSQL"""
        assert self.mapper.get_postgresql_type('varchar') == 'VARCHAR'
        assert self.mapper.get_postgresql_type('int') == 'INTEGER'
        assert self.mapper.get_postgresql_type('json') == 'JSONB'
    
    def test_sqlserver_type_mapping(self):
        """Testa mapeamento para SQL Server"""
        assert self.mapper.get_sqlserver_type('varchar') == 'NVARCHAR'
        assert self.mapper.get_sqlserver_type('int') == 'INT'
        assert self.mapper.get_sqlserver_type('bool') == 'BIT'
    
    def test_bigquery_type_mapping(self):
        """Testa mapeamento para BigQuery"""
        assert self.mapper.get_bigquery_type('varchar') == 'STRING'
        assert self.mapper.get_bigquery_type('int') == 'INTEGER'
        assert self.mapper.get_bigquery_type('bool') == 'BOOLEAN'
        assert self.mapper.get_bigquery_type('json') == 'JSON'
    
    def test_fallback_type(self):
        """Testa fallback para tipos desconhecidos"""
        assert self.mapper.get_generic_type('unknown_type') == 'string'
        assert self.mapper.get_mysql_type('unknown_type') == 'VARCHAR'

if __name__ == '__main__':
    unittest.main()