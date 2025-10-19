# Copyright 2025 TecOnca Data Solutions.


from datetime import datetime, timezone

formatos_de_datas = [
    (
        'aluno', 
        'ALU_DT_CRIACAO', 
        '2025-10-07 20:04:19.596331', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
]

for indice, tabela, campo, valor, formato in enumerate(formatos_de_datas, start=1):


        # formato_saida = '%Y-%m-%dT%H:%M:%S.%f'
        formato_saida = '%Y-%m-%d %H:%M:%S.%f'
        # formato_saida = '%Y-%m-%d %H:%M:%S.%f %Z'

        # Analisa a string para um objeto datetime
        # %Y - Ano com 4 dígitos
        # %m - Mês com 2 dígitos
        # %d - Dia do mês com 2 dígitos
        # %H - Hora (00-23)
        # %M - Minuto (00-59)
        # %S - Segundo (00-59)
        # %f - Microssegundo
        # %Z - Nome do fuso horário

        objeto_datetime = datetime.strptime(valor, formato)
        data_final_string = objeto_datetime.strftime(formato_saida)

        print(f"Linha: { indice }")
        print(f"Tabela: { tabela }")
        print(f"Coluna: { campo }")
        print(f"A string original é: { valor }")
        print(f"O timestamp correspondente é: { objeto_datetime }")
        print(f"O timestamp correspondente em str: { data_final_string }")
