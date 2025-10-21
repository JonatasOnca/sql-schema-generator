# Copyright 2025 TecOnca Data Solutions.

import logging
from pathlib import Path
from typing import Optional

from config import Config
from logger_config import SQLSchemaGeneratorError
from libs.csv_importer import CSVImporter
from libs.validator import DataValidator
from libs.sql_generator import SQLQueryGenerator
from libs.generate_schema import SchemaGenerator
from libs.generate_transform_functions import MappingFunctionsGenerator
from libs.generate_yaml import YAMLGenerator

class SQLSchemaGeneratorApp:
    """Aplicação principal do SQL Schema Generator"""
    
    def __init__(
        self,
        input_dir: Path = None,
        output_dir: Path = None,
        database_type: str = "MySQL",
        validate_only: bool = False
    ):
        self.logger = logging.getLogger(__name__)
        
        # Configurações
        self.input_dir = input_dir or Config.TABLES_CONFIG_DIR
        self.output_dir = output_dir or Config.BASE_DIR
        self.database_type = database_type
        self.validate_only = validate_only
        
        # Componentes
        self.importer = CSVImporter(self.input_dir)
        self.validator = DataValidator()
        self.sql_generator = SQLQueryGenerator(database_type)
        self.schema_generator = SchemaGenerator()
        self.mapping_generator = MappingFunctionsGenerator()
        self.yaml_generator = YAMLGenerator()
        
        # Dados
        self.tables_config = []
    
    def run(self) -> bool:
        """
        Executa o processo completo de geração
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # 1. Valida diretórios
            if not self._validate_directories():
                return False
            
            # 2. Importa configurações
            if not self._import_configurations():
                return False
            
            # 3. Valida dados
            if not self._validate_data():
                return False
            
            # Se apenas validação, para aqui
            if self.validate_only:
                self.logger.info("Validação concluída. Modo --validate-only ativo.")
                return True
            
            # 4. Gera saídas
            return self._generate_outputs()
            
        except Exception as e:
            self.logger.error(f"Erro durante execução: {e}")
            return False
    
    def _validate_directories(self) -> bool:
        """Valida se os diretórios existem e são acessíveis"""
        try:
            if not self.input_dir.exists():
                raise SQLSchemaGeneratorError(f"Diretório de entrada não existe: {self.input_dir}")
            
            if not self.input_dir.is_dir():
                raise SQLSchemaGeneratorError(f"Caminho de entrada não é um diretório: {self.input_dir}")
            
            # Garante que diretórios de saída existam
            Config.ensure_output_dirs()
            
            # Valida permissões de escrita
            return self.validator.validate_output_directories(self.output_dir)
            
        except Exception as e:
            self.logger.error(f"Erro na validação de diretórios: {e}")
            return False
    
    def _import_configurations(self) -> bool:
        """Importa configurações dos arquivos CSV"""
        try:
            self.logger.info("Importando configurações de tabelas...")
            self.tables_config = self.importer.import_tables_config()
            
            if not self.tables_config:
                raise SQLSchemaGeneratorError("Nenhuma configuração de tabela encontrada")
            
            self.logger.info(f"Importadas configurações de {len(self.tables_config)} banco(s)")
            
            for db_config in self.tables_config:
                db_name = db_config.get('file', 'unknown')
                table_count = len(db_config.get('tables', []))
                self.logger.info(f"  - {db_name}: {table_count} tabela(s)")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro na importação: {e}")
            return False
    
    def _validate_data(self) -> bool:
        """Valida os dados importados"""
        try:
            self.logger.info("Validando dados importados...")
            
            all_valid = True
            
            for db_config in self.tables_config:
                if not self.validator.validate_database_config(db_config):
                    all_valid = False
            
            # Mostra relatório de validação
            report = self.validator.get_validation_report()
            
            if report['warning_count'] > 0:
                self.logger.warning(f"Encontrados {report['warning_count']} avisos")
            
            if report['error_count'] > 0:
                self.logger.error(f"Encontrados {report['error_count']} erros")
                return False
            
            self.logger.info("✅ Validação concluída sem erros")
            return all_valid
            
        except Exception as e:
            self.logger.error(f"Erro na validação: {e}")
            return False
    
    def _generate_outputs(self) -> bool:
        """Gera todos os arquivos de saída"""
        try:
            self.logger.info("Iniciando geração de arquivos...")
            
            success_count = 0
            total_tables = sum(len(db['tables']) for db in self.tables_config)
            
            for database_config in self.tables_config:
                database_name = database_config.get('file')
                tables = database_config.get('tables', [])
                
                self.logger.info(f"Processando banco: {database_name}")
                
                for table in tables:
                    table_name = table.get('table')
                    fields_details = table.get('fields_details', [])
                    
                    try:
                        # Gera SQL
                        self.sql_generator.generate_table_sql(
                            database_name, table_name, fields_details
                        )
                        
                        # Gera Schema
                        self.schema_generator.generate_table_schema(
                            database_name, table_name, fields_details
                        )
                        
                        success_count += 1
                        self.logger.debug(f"✅ {database_name}.{table_name}")
                        
                    except Exception as e:
                        self.logger.error(f"❌ Erro ao processar {database_name}.{table_name}: {e}")
                        continue
                
                try:
                    # Gera arquivos por banco
                    self.mapping_generator.generate_mapping_functions(database_name, database_config)
                    self.yaml_generator.generate_tables_config(database_name, database_config)
                    self.yaml_generator.generate_chunks_config(database_name)
                    
                    self.logger.info(f"✅ Arquivos auxiliares gerados para {database_name}")
                    
                except Exception as e:
                    self.logger.error(f"❌ Erro ao gerar arquivos auxiliares para {database_name}: {e}")
            
            self.logger.info(f"Geração concluída: {success_count}/{total_tables} tabelas processadas")
            
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Erro na geração: {e}")
            return False

# Função legada para compatibilidade
def generator(argv=None):
    """Função legada - mantida para compatibilidade"""
    app = SQLSchemaGeneratorApp()
    return app.run()