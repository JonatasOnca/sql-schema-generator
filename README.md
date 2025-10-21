# SQL Schema Generator

Gerador automático de SQLs, schemas JSON e configurações YAML a partir de arquivos CSV de configuração de tabelas.

## 📋 Características

- **Multi-banco**: Suporte para MySQL, PostgreSQL e SQL Server
- **Validação robusta**: Validação completa dos dados de entrada
- **Modular**: Arquitetura orientada a objetos e extensível
- **Logging avançado**: Sistema de logs configurável
- **Tipos de saída múltiplos**: SQL, JSON Schema, YAML Config
- **Tratamento de erros**: Exceções específicas e relatórios detalhados

## 🚀 Instalação

### Pré-requisitos
- Python 3.10+
- pip

### Setup
```bash
# Clone o repositório
git clone <repo-url>
cd sql-schema-generator

# Cria ambiente virtual e instala dependências
make install

# Ou manualmente:
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 💻 Uso

### Uso Básico
```bash
# Usando Makefile
make run

# Ou diretamente
python main.py
```

### Opções Avançadas
```bash
# Especificar diretórios e tipo de banco
python main.py --input-dir ./custom-config --database-type PostgreSQL

# Apenas validar sem gerar saídas
python main.py --validate-only

# Com logging em arquivo
python main.py --log-file ./logs/generator.log --log-level DEBUG

# Ajuda completa
python main.py --help
```

## 📁 Estrutura do Projeto

```
sql-schema-generator/
├── main.py                 # Ponto de entrada
├── generator.py           # Aplicação principal
├── config.py             # Configurações centralizadas
├── logger_config.py      # Sistema de logging
├── requirements.txt      # Dependências
├── Makefile             # Automação de tarefas
├── files/               # Arquivos de configuração
│   ├── tables-config/   # CSVs de configuração de tabelas
│   ├── chunks-config/   # CSVs de configuração de chunks
│   └── database-config/ # JSONs de configuração de BD
├── libs/                # Módulos da biblioteca
│   ├── csv_importer.py  # Importação de CSVs
│   ├── sql_generator.py # Geração de SQLs
│   ├── type_data.py     # Mapeamento de tipos
│   ├── validator.py     # Validação de dados
│   └── ...
├── templates/           # Templates Jinja2
├── tests/              # Testes unitários
└── _OUTPUT/            # Arquivos gerados (criado automaticamente)
    ├── _SQL/
    ├── _SCHEMA/
    └── _YAML/
```

## 📊 Formato dos Arquivos CSV

Os arquivos CSV de configuração devem seguir o formato:

| Coluna | Descrição | Obrigatório |
|--------|-----------|-------------|
| table_name | Nome da tabela | ✅ |
| field_name | Nome do campo | ✅ |
| field_type | Tipo do campo | ✅ |
| constraints | Constraints (PRIMARY KEY, UNIQUE, etc.) | ❌ |
| description | Descrição do campo | ❌ |
| mask | Máscara/formato | ❌ |
| filter_flag | Flag de filtro (X para particionamento) | ❌ |

### Exemplo:
```csv
"users","id","int","PRIMARY KEY","User ID","",""
"users","name","varchar","","User name","",""
"users","email","varchar","UNIQUE","User email","",""
"users","created_at","timestamp","","Creation date","%Y-%m-%d %H:%i:%s","X"
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
export SQL_GENERATOR_LOG_LEVEL=INFO
export SQL_GENERATOR_DEFAULT_DB=MySQL
```

### Arquivo de Configuração
Edite `config.py` para personalizar:
- Diretórios padrão
- Tipos de banco suportados
- Configurações de logging

## 🧪 Testes

```bash
# Executar todos os testes
python -m unittest discover tests/

# Teste específico
python -m unittest tests.test_type_mapper

# Com cobertura (se instalado pytest-cov)
pytest --cov=libs tests/
```

## 📈 Saídas Geradas

### 1. SQLs (_SQL/)
Queries SELECT com CASTs apropriados para cada campo:
```sql
SELECT 
    CAST(id AS CHAR) AS id,
    CAST(name AS CHAR) AS name
FROM database.table
```

### 2. Schemas JSON (_SCHEMA/)
Schemas BigQuery/JSON com metadados de auditoria:
```json
{
    "fields": [
        {
            "name": "id",
            "type": "INTEGER",
            "mode": "NULLABLE",
            "description": "User ID"
        }
    ]
}
```

### 3. Configurações YAML (_YAML/)
Configurações para pipelines de dados:
```yaml
tables:
  - name: users
    query_file: users.sql
    schema_file: users.json
    merge_config:
      strategy: 'upsert'
      keys: ['id']
```

## 🚀 Extensibilidade

### Adicionando Novo Banco de Dados
1. Crie nova classe em `libs/sql_generator.py`:
```python
class OracleDialect(DatabaseDialect):
    def cast_field(self, field_name, field_type, field_mask=None):
        # Implementar lógica Oracle
        pass
```

2. Registre no factory method
3. Adicione mapeamentos de tipos em `TypeMapper`

### Adicionando Novo Gerador
1. Crie nova classe seguindo o padrão
2. Integre em `SQLSchemaGeneratorApp`
3. Adicione testes unitários

## 🐛 Troubleshooting

### Problemas Comuns

**Erro: "Nenhum arquivo CSV encontrado"**
- Verifique se os CSVs estão em `files/tables-config/`
- Use `--input-dir` para especificar diretório personalizado

**Erro: "Linha com poucas colunas"**
- Verifique formato do CSV (mínimo 3 colunas)
- Use `--validate-only` para ver erros detalhados

**Erro de permissão**
- Verifique permissões de escrita no diretório de saída
- Use `--output-dir` para especificar local alternativo

## 📝 Changelog

### v2.0.0 (2025-01-21)
- ✨ Refatoração completa da arquitetura
- ✨ Suporte multi-banco de dados
- ✨ Sistema de validação robusto
- ✨ Logging configurável
- ✨ Tratamento de erros melhorado
- ✨ Testes unitários
- ✨ CLI com argumentos
- 🐛 Correções de bugs na importação CSV

### v1.0.0 (2025-01-01)
- 🎉 Versão inicial

## 🤝 Contribuindo

1. Fork o projeto
2. Crie branch para feature (`git checkout -b feature/nova-feature`)
3. Commit mudanças (`git commit -am 'Add nova feature'`)
4. Push para branch (`git push origin feature/nova-feature`)
5. Abra Pull Request

## 📄 Licença

Copyright 2025 TecOnca Data Solutions. Todos os direitos reservados.

## 👥 Suporte

- 📧 Email: suporte@teconca.com
- 📖 Documentação: [docs/](./docs/)
- 🐛 Issues: [GitHub Issues](./issues)