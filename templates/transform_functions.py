# Copyright 2025 TecOnca Data Solutions.


import logging
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

def formatar_data(valor_data: str, formato_entrada: str, formato_saida: str) -> str | None:
    # Se o valor de entrada não for uma string ou estiver vazio, retorna None
    if not isinstance(valor_data, str) or not valor_data:
        return None

    # if 'Timestamp' in valor_data:
    #     try:
    #         numero_em_string = valor_data[10:-1]
    #         timestamp_numerico = float(numero_em_string)
    #         objeto_data = datetime.fromtimestamp(timestamp_numerico)
    #         # Formata o objeto datetime para a string de saída
    #         return objeto_data.strftime(formato_saida)
    #     except (ValueError, TypeError) as e:
    #         logging.warning(f"Não foi possível formatar a data '{valor_data}' com o formato de entrada '{formato_entrada}'. Erro: {e}")
    #         return None # Retorna None em caso de erro
    # else:

    # Analisa a string para um objeto datetime
    # %Y - Ano com 4 dígitos
    # %m - Mês com 2 dígitos
    # %d - Dia do mês com 2 dígitos
    # %H - Hora (00-23)
    # %M - Minuto (00-59)
    # %S - Segundo (00-59)
    # %f - Microssegundo
    # %Z - Nome do fuso horário
    try:
        objeto_datetime = datetime.strptime(valor_data, formato_entrada)
        data_final_string = objeto_datetime.strftime(formato_saida)
        return data_final_string
    except (ValueError, TypeError) as e:
        logging.warning(f"Não foi possível formatar a data '{valor_data}' com o formato de entrada '{formato_entrada}'. Erro: {e}")
        return None

def generic_transform(row_dict):
    return row_dict

{% for table in database['tables'] -%}
def transform_{{ table['table'] }}_table(row_dict):
    transformed_row = row_dict.copy()
        {% for fields in table['fields_details'] -%}
        {%- if fields[1] in string %}
    transformed_row['{{fields[0]}}'] = str(transformed_row.get('{{fields[0]}}'))
        {%- endif -%}
        {%- if fields[1] in date %}
    transformed_row['{{fields[0]}}'] = formatar_data(
        valor_data=transformed_row.get('{{fields[0]}}'),
        formato_entrada='{{ fields[4] }}',
        formato_saida='%Y-%m-%d %H:%M:%S.%f' # Formato DATETIME para o BigQuery
    )   
        {%- endif -%}
        {%- if fields[1] in integer %}
    if transformed_row.get('{{fields[0]}}') is None:
        transformed_row['{{fields[0]}}'] = None
    else:
        transformed_row['{{fields[0]}}'] = int(transformed_row.get('{{fields[0]}}'))
        {%- endif -%}
        {%- if fields[1] in decimal %}
    transformed_row['{{fields[0]}}'] = Decimal(transformed_row.get('{{fields[0]}}'))
        {%- endif -%}
        {%- if fields[1] in json %}
    transformed_row['{{fields[0]}}'] = transformed_row.get('{{fields[0]}}')
        {%- endif -%}
        {%- endfor %}

    return transformed_row

{% endfor -%}


TRANSFORM_MAPPING = {
    {% for table in database['tables'] -%}
    '{{ table['table'] }}': transform_{{ table['table'] }}_table,
    {% endfor -%}
}

