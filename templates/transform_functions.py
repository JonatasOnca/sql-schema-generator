# Copyright 2025 TecOnca Data Solutions.


import logging

from decimal import Decimal
from datetime import datetime, timedelta

def converter_data(valor_data, formato):
    """
    Converte uma string de data (ou número OLE) para um objeto datetime.
    """
    
    # 1. Tentar converter números OLE (Excel Serial Date)
    try:
        # Tenta substituir vírgula por ponto para garantir o formato flutuante
        valor_str = str(valor_data).replace(',', '.')
        valor_flutuante = float(valor_str)
        
        # O número de dias é a parte inteira. 
        # A parte decimal é a fração do dia.
        
        # Data de referência do Excel: 30 de dezembro de 1899
        # (O Excel conta 1900-02-29, que não existe, por isso o offset é 2)
        base_date = datetime(1899, 12, 30)
        
        # O offset de 2 dias é para compensar o erro de bissexto do Excel.
        # Se for um inteiro, não precisamos do timedelta (só se for data pura)
        # Se for decimal, o timedelta lida com a parte fracionária
        if valor_flutuante < 60: # Assume que se for menor que 60 é uma data no século 20, 
                                 # compensando a contagem errada do Excel para 1900.
            dias = valor_flutuante - 2
        else:
            dias = valor_flutuante
            
        data_convertida = base_date + timedelta(days=dias)
        
        # O formato de saída para números OLE geralmente será mais simples, 
        # já que o formato na lista para eles não é o 'verdadeiro' formato strptime
        # e é só o formato esperado APÓS a conversão OLE.
        return data_convertida.strftime('%Y-%m-%d %H:%M:%S.%f')
        
    except ValueError:
        # Se falhar a conversão para float, tenta a conversão normal strptime
        pass

    # 2. Tentar conversão strptime padrão
    try:
        # O formato '%f %Z' pode causar problemas se a string não tem o TZ no final.
        # Muitas vezes, o '%Z' no formato só funciona se a string tem a zona explícita, 
        # ou se o valor for um "placeholder" para datas sem TZ.
        
        # Simplificando a lógica, vamos tentar o formato com %f (milissegundos)
        # e ignorar o %Z se não estiver na string.
        # Este é um exemplo simplificado, na prática você precisaria de mais tratativas.
        
        # Removendo %Z e %f do formato se o valor_data não tiver milissegundos/TZ
        formato_limpo = formato.replace(' %Z', '').replace('T', ' ').replace('.%f', '')
        if '.' in str(valor_data):
            # Se tiver milissegundos, use o formato original (ou com T trocado por espaço)
            if 'T' in formato:
                formato = formato.replace('T', ' ')
            
            # Se o valor não tiver o %Z (ex: a turma_aluno['updatedAt']), precisa limpar o formato
            if formato.endswith(' %Z') and ' ' not in str(valor_data).split(' ')[-1]:
                formato = formato.replace(' %Z', '')

        elif valor_data.count(':') < 2: # Se não tem segundos/horas, tenta formatos mais simples
            return datetime.strptime(str(valor_data), '%Y-%m-%d')
            
        # Tenta a conversão com o formato completo
        return datetime.strptime(str(valor_data), formato)
        
    except ValueError as e:
        logging.warning(f"ERRO ao analisar: {e} | Valor original: '{valor_data}' com formato '{formato}'")
        return f"ERRO ao analisar: {e} | Valor original: '{valor_data}' com formato '{formato}'"


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
    transformed_row['{{fields[0]}}'] = converter_data(
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

