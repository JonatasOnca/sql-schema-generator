# Copyright 2025 TecOnca Data Solutions.

# --- Variáveis ---
# Define o interpretador Python base
PYTHON = python3.11

# Define o nome do diretório do ambiente virtual
VENV_DIR = .venv

# Define o caminho para o executável Python dentro do .venv
VENV_PYTHON = $(VENV_DIR)/bin/python

# --- Configurações ---
# Alvo padrão que será executado se você digitar apenas "make"
.DEFAULT_GOAL := help

# Alvos que não representam arquivos
.PHONY: help venv install run test clean

# --- Comandos ---

help:
	@echo "Comandos disponíveis:"
	@echo "  make venv     -> Cria o ambiente virtual Python."
	@echo "  make install  -> Instala as dependências do requirements.txt no venv."
	@echo "  make run      -> Executa o script principal (main.py) usando o venv."
	@echo "  make test     -> Roda os testes (ex: pytest)."
	@echo "  make clean    -> Remove o ambiente virtual e arquivos temporários."

venv:
	@# Cria o venv apenas se o diretório não existir
	test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)

install: venv
	@echo "Instalando dependências..."
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

run:
	@echo "Executando o programa..."
	$(VENV_PYTHON) main.py
	@echo "Finalizando o programa..."

activate:
	@echo "Para ativar o ambiente virtual, execute no seu terminal:"
	@echo "  source $(VENV_DIR)/bin/activate"
	@echo "Para desativar depois, basta digitar 'deactivate'."

test:
	@echo "Rodando testes..."
	$(VENV_PYTHON) -m pytest

clean:
	@echo "Limpando arquivos temporários..."
	rm -rf $(VENV_DIR)
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete