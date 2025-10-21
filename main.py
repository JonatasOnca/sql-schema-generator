# Copyright 2025 TecOnca Data Solutions.

import sys
import argparse
from pathlib import Path

from config import Config
from logger_config import setup_logging, SQLSchemaGeneratorError
from generator import SQLSchemaGeneratorApp

def create_argument_parser():
    """Cria o parser de argumentos da linha de comando"""
    parser = argparse.ArgumentParser(
        description="SQL Schema Generator - Gera SQLs, schemas e YAMLs a partir de configurações CSV"
    )
    
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Config.TABLES_CONFIG_DIR,
        help="Diretório com arquivos CSV de configuração"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Config.BASE_DIR,
        help="Diretório base para saída"
    )
    
    parser.add_argument(
        "--database-type",
        choices=Config.SUPPORTED_DATABASES,
        default=Config.DEFAULT_DATABASE,
        help="Tipo de banco de dados alvo"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Nível de log"
    )
    
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Arquivo para salvar logs (opcional)"
    )
    
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Apenas valida os arquivos sem gerar saídas"
    )
    
    return parser

def main():
    """Função principal da aplicação"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Configura logging
    logger = setup_logging(args.log_level, args.log_file)
    
    try:
        logger.info("=== SQL Schema Generator ===")
        logger.info(f"Iniciando processamento...")
        logger.info(f"Input: {args.input_dir}")
        logger.info(f"Output: {args.output_dir}")
        logger.info(f"Database: {args.database_type}")
        
        # Cria e executa a aplicação
        app = SQLSchemaGeneratorApp(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            database_type=args.database_type,
            validate_only=args.validate_only
        )
        
        success = app.run()
        
        if success:
            logger.info("✅ Processamento concluído com sucesso!")
            return 0
        else:
            logger.error("❌ Processamento falhou")
            return 1
            
    except SQLSchemaGeneratorError as e:
        logger.error(f"Erro na aplicação: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Processamento interrompido pelo usuário")
        return 1
    except Exception as e:
        logger.error(f"Erro inesperado: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())