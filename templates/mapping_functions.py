# Copyright 2025 TecOnca Data Solutions.

import logging
from datetime import datetime

def formatar_data(valor_data: str, formato_entrada: str, formato_saida: str) -> str | None:
    """
    Função genérica para converter uma string de data de um formato para outro.

    Args:
        valor_data (str): A string da data a ser convertida (ex: '04/10/2025').
        formato_entrada (str): O formato da string de entrada (ex: '%d/%m/%Y').
        formato_saida (str): O formato desejado para a string de saída (ex: '%Y-%m-%d').

    Returns:
        str: A string da data formatada, ou None se a entrada for inválida ou vazia.
    """
    # Se o valor de entrada não for uma string ou estiver vazio, retorna None
    if not isinstance(valor_data, str) or not valor_data:
        return None

    if 'Timestamp' in valor_data:
        try:
            numero_em_string = valor_data[10:-1]
            timestamp_numerico = float(numero_em_string)
            # Converte a string para um objeto datetime usando o formato de entrada
            objeto_data = datetime.fromtimestamp(timestamp_numerico)
            # Formata o objeto datetime para a string de saída
            return objeto_data.strftime(formato_saida)
        except (ValueError, TypeError) as e:
            # Loga um aviso se a conversão falhar
            logging.warning(f"Não foi possível formatar a data '{valor_data}' com o formato de entrada '{formato_entrada}'. Erro: {e}")
            return None # Retorna None em caso de erro
    else:
        try:
            objeto_data = datetime.fromisoformat(valor_data)
            # Formata o objeto datetime para a string de saída
            return objeto_data.strftime(formato_saida)
        except (ValueError, TypeError) as e:
            # Loga um aviso se a conversão falhar
            logging.warning(f"Não foi possível formatar a data '{valor_data}' com o formato de entrada '{formato_entrada}'. Erro: {e}")
            return None # Retorna None em caso de erro

def generic_transform(row_dict):
    return row_dict

{% for table in database['tables'] -%}
def transform_{{ table['table'] }}_table(row_dict):
    transformed_row = row_dict.copy()
        {% for fields in table['fields_details'] -%}
        {%- if fields[1] in data %}
    transformed_row['{{fields[0]}}'] = formatar_data(
        valor_data=transformed_row.get('{{fields[0]}}'),
        formato_entrada='%Y-%m-%d %H:%i:%s.%f',
        formato_saida='%Y-%m-%d %H:%M:%S.%f' # Formato DATETIME para o BigQuery
    )
        {%- endif -%}
        {%- endfor %}

    return transformed_row

{% endfor -%}


TRANSFORM_MAPPING = {
    {% for table in database['tables'] -%}
    '{{ table['table'] }}': transform_{{ table['table'] }}_table,
    {% endfor -%}
}

