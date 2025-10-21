# Copyright 2025 TecOnca Data Solutions.

import os
from pathlib import Path

class Config:
    """Configurações centralizadas do projeto"""
    
    # Diretórios base
    BASE_DIR = Path(__file__).parent
    TEMPLATES_DIR = BASE_DIR / "templates"
    FILES_DIR = BASE_DIR / "files"
    LIBS_DIR = BASE_DIR / "libs"
    
    # Diretórios de entrada
    TABLES_CONFIG_DIR = FILES_DIR / "tables-config"
    CHUNKS_CONFIG_DIR = FILES_DIR / "chunks-config"
    DATABASE_CONFIG_DIR = FILES_DIR / "database-config"
    
    # Diretórios de saída
    OUTPUT_SQL_DIR = BASE_DIR / "_SQL"
    OUTPUT_SCHEMA_DIR = BASE_DIR / "_SCHEMA"
    OUTPUT_YAML_DIR = BASE_DIR / "_YAML"
    
    # Configurações de database
    DEFAULT_DATABASE = "MySQL"
    SUPPORTED_DATABASES = ["MySQL", "PostgreSQL", "SQLServer"]
    
    # Configurações de logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def ensure_output_dirs(cls):
        """Garante que os diretórios de saída existam"""
        for dir_path in [cls.OUTPUT_SQL_DIR, cls.OUTPUT_SCHEMA_DIR, cls.OUTPUT_YAML_DIR]:
            dir_path.mkdir(exist_ok=True)