# Copyright 2025 TecOnca Data Solutions.

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from logger_config import ConfigurationError

class DataValidator:
    """Classe para validação de dados de entrada"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.errors = []
        self.warnings = []
    
    def validate_csv_data(self, csv_data: List[tuple], filename: str) -> bool:
        """
        Valida dados de um arquivo CSV
        
        Args:
            csv_data: Dados do CSV como lista de tuplas
            filename: Nome do arquivo para reportar erros
            
        Returns:
            True se válido, False caso contrário
        """
        self.errors = []
        self.warnings = []
        
        if not csv_data:
            self.errors.append(f"Arquivo {filename} está vazio")
            return False
        
        # Valida header implícito (primeira linha)
        expected_columns = 7  # table, field, type, constraint, description, mask, filter
        
        for i, row in enumerate(csv_data, 1):
            self._validate_row(row, i, filename, expected_columns)
        
        if self.errors:
            for error in self.errors:
                self.logger.error(error)
            return False
        
        if self.warnings:
            for warning in self.warnings:
                self.logger.warning(warning)
        
        return True
    
    def _validate_row(self, row: tuple, row_num: int, filename: str, expected_columns: int):
        """Valida uma linha individual do CSV"""
        # Verifica número de colunas
        if len(row) < 3:  # Mínimo: table, field, type
            self.errors.append(
                f"{filename}:{row_num} - Linha com poucas colunas: {len(row)} (mínimo 3)"
            )
            return
        
        if len(row) > expected_columns:
            self.warnings.append(
                f"{filename}:{row_num} - Linha com colunas extras: {len(row)} (esperado {expected_columns})"
            )
        
        # Valida campos obrigatórios
        table_name = row[0].strip() if row[0] else ""
        field_name = row[1].strip() if row[1] else ""
        field_type = row[2].strip() if row[2] else ""
        
        if not table_name:
            self.errors.append(f"{filename}:{row_num} - Nome da tabela vazio")
        
        if not field_name:
            self.errors.append(f"{filename}:{row_num} - Nome do campo vazio")
        
        if not field_type:
            self.errors.append(f"{filename}:{row_num} - Tipo do campo vazio")
        
        # Valida nomes (não podem ter caracteres especiais perigosos)
        if table_name and not self._is_valid_identifier(table_name):
            self.warnings.append(
                f"{filename}:{row_num} - Nome de tabela suspeito: '{table_name}'"
            )
        
        if field_name and not self._is_valid_identifier(field_name):
            self.warnings.append(
                f"{filename}:{row_num} - Nome de campo suspeito: '{field_name}'"
            )
    
    def _is_valid_identifier(self, name: str) -> bool:
        """Verifica se um nome é um identificador SQL válido"""
        if not name:
            return False
        
        # Remove backticks se presentes
        clean_name = name.strip('`"[]')
        
        # Verifica se contém apenas caracteres alfanuméricos e underscore
        if not clean_name.replace('_', '').replace('-', '').isalnum():
            return False
        
        # Não pode começar com número
        if clean_name[0].isdigit():
            return False
        
        return True
    
    def validate_table_config(self, table_config: Dict[str, Any]) -> bool:
        """Valida configuração de uma tabela"""
        required_keys = ['table', 'fields_details']
        
        for key in required_keys:
            if key not in table_config:
                self.errors.append(f"Configuração de tabela faltando chave obrigatória: {key}")
                return False
        
        if not table_config['fields_details']:
            self.errors.append(f"Tabela {table_config.get('table', 'unknown')} sem campos")
            return False
        
        return True
    
    def validate_database_config(self, database_config: Dict[str, Any]) -> bool:
        """Valida configuração de um banco de dados"""
        if 'file' not in database_config:
            self.errors.append("Configuração de banco faltando nome do arquivo")
            return False
        
        if 'tables' not in database_config or not database_config['tables']:
            self.errors.append(f"Banco {database_config['file']} sem tabelas")
            return False
        
        # Valida cada tabela
        for table in database_config['tables']:
            if not self.validate_table_config(table):
                return False
        
        return True
    
    def validate_output_directories(self, base_dir: Path) -> bool:
        """Valida se os diretórios de saída podem ser criados"""
        try:
            test_dirs = ['_SQL', '_SCHEMA', '_YAML']
            for dir_name in test_dirs:
                test_path = base_dir / dir_name
                test_path.mkdir(exist_ok=True)
            return True
        except Exception as e:
            self.errors.append(f"Não foi possível criar diretórios de saída: {e}")
            return False
    
    def get_validation_report(self) -> Dict[str, Any]:
        """Retorna relatório de validação"""
        return {
            'is_valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings)
        }