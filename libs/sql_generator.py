# Copyright 2025 TecOnca Data Solutions.

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from string import Template
from typing import List, Dict, Any, Optional

from config import Config
from logger_config import TemplateError
from libs.type_data import TypeMapper

class DatabaseDialect(ABC):
    """Classe base para dialetos de banco de dados"""
    
    @abstractmethod
    def cast_field(self, field_name: str, field_type: str, field_mask: str = None) -> str:
        """Aplica cast apropriado para o campo no dialeto específico"""
        pass
    
    @abstractmethod
    def get_type_mapping(self, field_type: str) -> str:
        """Retorna o tipo de dados apropriado para o dialeto"""
        pass

class MySQLDialect(DatabaseDialect):
    """Dialeto MySQL"""
    
    def __init__(self):
        self.type_mapper = TypeMapper()
    
    def cast_field(self, field_name: str, field_type: str, field_mask: str = None) -> str:
        """Aplica cast para MySQL"""
        # Trata palavras reservadas
        reserved_words = ['option', 'order', 'group', 'select', 'from', 'where']
        if field_name.lower() in reserved_words:
            field_name = f'`{field_name}`'
        
        # Por enquanto, força CHAR para compatibilidade
        # TODO: Implementar lógica mais sofisticada baseada no tipo
        return f'CAST({field_name} AS CHAR) AS {field_name}'
    
    def get_type_mapping(self, field_type: str) -> str:
        """Mapeia tipos para MySQL"""
        return self.type_mapper.get_mysql_type(field_type)

class PostgreSQLDialect(DatabaseDialect):
    """Dialeto PostgreSQL"""
    
    def __init__(self):
        self.type_mapper = TypeMapper()
    
    def cast_field(self, field_name: str, field_type: str, field_mask: str = None) -> str:
        """Aplica cast para PostgreSQL"""
        pg_type = self.get_type_mapping(field_type)
        return f'CAST({field_name} AS {pg_type}) AS {field_name}'
    
    def get_type_mapping(self, field_type: str) -> str:
        """Mapeia tipos para PostgreSQL"""
        return self.type_mapper.get_postgresql_type(field_type)

class SQLServerDialect(DatabaseDialect):
    """Dialeto SQL Server"""
    
    def __init__(self):
        self.type_mapper = TypeMapper()
    
    def cast_field(self, field_name: str, field_type: str, field_mask: str = None) -> str:
        """Aplica cast para SQL Server"""
        sql_type = self.get_type_mapping(field_type)
        return f'CAST({field_name} AS {sql_type}) AS {field_name}'
    
    def get_type_mapping(self, field_type: str) -> str:
        """Mapeia tipos para SQL Server"""
        return self.type_mapper.get_sqlserver_type(field_type)

class SQLQueryGenerator:
    """Gerador de queries SQL melhorado"""
    
    def __init__(self, database_type: str = "MySQL"):
        self.logger = logging.getLogger(__name__)
        self.database_type = database_type
        self.dialect = self._get_dialect(database_type)
        self.template_path = Config.TEMPLATES_DIR / "sql.sql"
    
    def _get_dialect(self, database_type: str) -> DatabaseDialect:
        """Factory para dialetos de banco"""
        dialects = {
            "MySQL": MySQLDialect,
            "PostgreSQL": PostgreSQLDialect,
            "SQLServer": SQLServerDialect
        }
        
        dialect_class = dialects.get(database_type)
        if not dialect_class:
            raise ValueError(f"Dialeto não suportado: {database_type}")
        
        return dialect_class()
    
    def generate_table_sql(
        self, 
        database_name: str, 
        table_name: str, 
        fields_details: List[tuple],
        output_dir: Path = None
    ) -> None:
        """
        Gera arquivo SQL para uma tabela
        
        Args:
            database_name: Nome do banco de dados
            table_name: Nome da tabela
            fields_details: Lista de tuplas com detalhes dos campos
            output_dir: Diretório de saída (opcional)
        """
        try:
            output_dir = output_dir or Config.OUTPUT_SQL_DIR
            
            # Processa os campos
            sanitized_fields = self._process_fields(fields_details)
            
            # Gera o SQL a partir do template
            sql_content = self._render_template(
                database_name=database_name,
                table_name=table_name,
                fields=sanitized_fields
            )
            
            # Salva o arquivo
            self._save_sql_file(output_dir, database_name, table_name, sql_content)
            
            self.logger.info(f"SQL gerado para {database_name}.{table_name}")
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar SQL para {table_name}: {e}")
            raise TemplateError(f"Erro ao gerar SQL: {e}")
    
    def _process_fields(self, fields_details: List[tuple]) -> List[str]:
        """Processa os campos aplicando cast apropriado"""
        processed_fields = []
        
        for field_detail in sorted(fields_details):
            if len(field_detail) < 2:
                continue
            
            field_name = field_detail[0]
            field_type = field_detail[1]
            field_mask = field_detail[4] if len(field_detail) > 4 else None
            
            cast_expression = self.dialect.cast_field(field_name, field_type, field_mask)
            processed_fields.append(cast_expression)
        
        return processed_fields
    
    def _render_template(self, database_name: str, table_name: str, fields: List[str]) -> str:
        """Renderiza o template SQL"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as file:
                template_content = file.read()
            
            template = Template(template_content)
            return template.substitute(
                _fields=",\n    ".join(fields),
                _database_name=database_name,
                _table_name=table_name
            )
        
        except Exception as e:
            raise TemplateError(f"Erro ao renderizar template: {e}")
    
    def _save_sql_file(
        self, 
        output_dir: Path, 
        database_name: str, 
        table_name: str, 
        content: str
    ) -> None:
        """Salva o arquivo SQL"""
        sql_dir = output_dir / database_name
        sql_dir.mkdir(parents=True, exist_ok=True)
        
        sql_file = sql_dir / f"{table_name}.sql"
        
        with open(sql_file, 'w', encoding='utf-8') as file:
            file.write(content)
    
    def generate_multiple_tables(
        self, 
        databases_config: List[Dict[str, Any]], 
        output_dir: Path = None
    ) -> None:
        """Gera SQLs para múltiplas tabelas de múltiplos bancos"""
        for database_config in databases_config:
            database_name = database_config.get('file', 'unknown')
            tables = database_config.get('tables', [])
            
            for table in tables:
                table_name = table.get('table')
                fields_details = table.get('fields_details', [])
                
                if table_name and fields_details:
                    self.generate_table_sql(
                        database_name=database_name,
                        table_name=table_name,
                        fields_details=fields_details,
                        output_dir=output_dir
                    )