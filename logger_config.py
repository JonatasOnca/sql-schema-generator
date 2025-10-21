# Copyright 2025 TecOnca Data Solutions.

import logging
import sys
from pathlib import Path
from config import Config

def setup_logging(log_level: str = Config.LOG_LEVEL, log_file: Path = None):
    """
    Configura o sistema de logging do projeto
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Arquivo opcional para salvar logs
    """
    
    # Configuração do formatter
    formatter = logging.Formatter(Config.LOG_FORMAT)
    
    # Logger principal
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo (opcional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

class SQLSchemaGeneratorError(Exception):
    """Exceção base para erros do SQL Schema Generator"""
    pass

class ConfigurationError(SQLSchemaGeneratorError):
    """Erro de configuração"""
    pass

class FileProcessingError(SQLSchemaGeneratorError):
    """Erro no processamento de arquivos"""
    pass

class TemplateError(SQLSchemaGeneratorError):
    """Erro no processamento de templates"""
    pass

class DatabaseError(SQLSchemaGeneratorError):
    """Erro relacionado ao banco de dados"""
    pass