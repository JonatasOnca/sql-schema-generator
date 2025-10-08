# Copyright 2025 TecOnca Data Solutions.


import logging

from decimal import Decimal
from datetime import datetime, timedelta

def converter_data(valor_data, formato_entrada, formato_saida='%Y-%m-%d %H:%M:%S.%f'):
    # Formato de destino: Ano-Mês-Dia Hora:Minuto:Segundo.Microssegundo
    try:
        # Tenta a conversão para string de data/tempo
        data_convertida = None
        
        # 1. Tenta converter de número serial do Excel (OLE Automation Date)
        # O número serial é uma string que pode conter vírgula para separar a parte fracionária
        if isinstance(valor_data, str):
            # Substitui a vírgula por ponto para garantir a correta conversão para float
            valor_data_formatado = valor_data.replace(',', '.')
            if valor_data_formatado.replace('.', '', 1).isdigit(): # Verifica se é um número (float ou int)
                data_serial = float(valor_data_formatado)
                
                # OLE Automation Date começa em 30 de dezembro de 1899
                # 25569 é o número serial para 1 de janeiro de 1970 (para referência)
                
                # Base de data do Excel (30 de dezembro de 1899)
                data_base_excel = datetime(1899, 12, 30)
                
                # Converte a parte serial em um objeto timedelta
                # A parte inteira é o número de dias, a parte fracionária é a fração de um dia
                dias = int(data_serial)
                fracao_tempo_dias = data_serial - dias
                
                # O número de segundos é a fração do dia * (24 * 60 * 60)
                segundos_do_dia = fracao_tempo_dias * 86400  # 86400 segundos em um dia
                
                # Cria o timedelta
                delta = timedelta(days=dias, seconds=segundos_do_dia)
                
                data_convertida = data_base_excel + delta
                
        # 2. Tenta converter a partir de string de data usando diversos formatos
        if data_convertida is None:
            # Lista de formatos possíveis baseada na lista fornecida
            formatos_string = [
                '%Y-%m-%d %H:%M:%S.%f %Z',  # Ex: 2025-10-07 20:04:19.596331
                '%Y-%m-%d %H:%M:%S %Z',    # Ex: 2024-12-28 13:46:29
                '%Y-%m-%dT%H:%M:%S.%f',    # Ex: 2025-10-08 00:52:14.112527 (ISO-like sem fuso)
                '%Y-%m-%d %H:%M:%S',       # Ex: 47068 (aqui seria um serial, mas para ser exaustivo)
                '%Y-%m-%d',                # Ex: 45938
                # Nota: Os formatos com %Z (timezone) podem falhar se a string não tiver o fuso horário.
                # Nesses casos, a conversão é tentada sem o %Z para obter um objeto datetime naive.
            ]
            
            # Tenta converter a string com e sem %Z
            for fmt in list(set(formatos_string)): # Usamos set para evitar duplicações
                try:
                    # Tenta a conversão
                    data_convertida = datetime.strptime(valor_data, fmt)
                    break
                except ValueError:
                    # Se falhar, tenta remover %Z, se presente
                    if '%Z' in fmt:
                        try:
                            fmt_sem_tz = fmt.replace(' %Z', '')
                            data_convertida = datetime.strptime(valor_data, fmt_sem_tz)
                            break
                        except ValueError:
                            continue # Passa para o próximo formato

            
        # 3. Formata a data convertida para a string de formato padrão
        if data_convertida:
            # Retorna a nova tupla com a data formatada
            return data_convertida.strftime(formato_saida)

        # Se a conversão for um número inteiro que não é um serial Excel, pode ser um dia.
        # Mas sem informação mais precisa, manteremos a lógica acima como prioritária.
        
        # Se nenhuma conversão funcionar, retorna o valor original.
        return valor_data

    except Exception as e:
        # Em caso de qualquer erro inesperado, retorna a tupla original
        logging.warning(f"ERRO ao analisar: {e} | Valor original: '{valor_data}' com formato '{formato_entrada}'")
        return valor_data


def generic_transform(row_dict):
    return row_dict

{% for table in database['tables'] -%}
def transform_{{ table['table'] }}_table(row_dict):
    transformed_row = row_dict.copy()
        {% for fields in table['fields_details'] -%}
        {%- if fields[1] in string %}
    if not transformed_row.get('{{fields[0]}}') is None:
        transformed_row['{{fields[0]}}'] = str(transformed_row.get('{{fields[0]}}'))
        {%- endif -%}
        {%- if fields[1] in date %}
    if not transformed_row.get('{{fields[0]}}') is None:
        transformed_row['{{fields[0]}}'] = converter_data(
            valor_data=transformed_row.get('{{fields[0]}}'),
            formato_entrada='{{ fields[4] }}',
            formato_saida='%Y-%m-%d %H:%M:%S.%f' # Formato DATETIME para o BigQuery
        )
        {%- endif -%}
        {%- if fields[1] in integer %}
    if not transformed_row.get('{{fields[0]}}') is None:
        transformed_row['{{fields[0]}}'] = int(transformed_row.get('{{fields[0]}}'))
        {%- endif -%}
        {%- if fields[1] in decimal %}
    if not transformed_row.get('{{fields[0]}}') is None:
        transformed_row['{{fields[0]}}'] = Decimal(transformed_row.get('{{fields[0]}}'))
        {%- endif -%}
        {%- if fields[1] in json %}
    if not transformed_row.get('{{fields[0]}}') is None:
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