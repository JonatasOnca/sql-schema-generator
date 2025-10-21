# Copyright 2025 TecOnca Data Solutions.

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from libs.csv_importer import CSVImporter, TableConfig
from logger_config import FileProcessingError

class TestCSVImporter:
    
    def setup_method(self):
        """Setup para cada teste"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.importer = CSVImporter(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_import_empty_directory(self):
        """Testa importação de diretório vazio"""
        with pytest.raises(FileProcessingError):
            self.importer.import_tables_config()
    
    def test_import_valid_csv(self):
        """Testa importação de CSV válido"""
        # Cria arquivo CSV de teste
        csv_content = '''table_test,field1,int,PRIMARY KEY,Description 1,,
table_test,field2,varchar,,Description 2,,
table_test,field3,date,,,,%Y-%m-%d,X'''
        
        csv_file = self.temp_dir / "test.csv"
        csv_file.write_text(csv_content)
        
        result = self.importer.import_tables_config()
        
        assert len(result) == 1
        assert result[0]['file'] == 'test'
        assert len(result[0]['tables']) == 1
        
        table = result[0]['tables'][0]
        assert table['table'] == 'table_test'
        assert len(table['fields_details']) == 3
        assert 'field1' in table['primary_keys']
    
    def test_table_config_creation(self):
        """Testa criação de configuração de tabela"""
        table_rows = [
            ('test_table', 'id', 'int', 'PRIMARY KEY', 'ID field', '', ''),
            ('test_table', 'name', 'varchar', '', 'Name field', '', ''),
        ]
        
        config = self.importer._create_table_config(table_rows)
        
        assert config.name == 'test_table'
        assert 'id' in config.primary_keys
        assert 'name' in config.fields
        assert len(config.fields_details) == 2

if __name__ == '__main__':
    pytest.main([__file__])