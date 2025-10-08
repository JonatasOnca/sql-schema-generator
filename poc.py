from datetime import datetime, timedelta

formatos_de_datas = [
    (
        'aluno', 
        'ALU_DT_CRIACAO', 
        '2025-10-07 20:04:19.596331', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'aluno', 
        'ALU_DT_ATUALIZACAO', 
        '45938,0084143519', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'aluno_teste', 
        'ALT_DT_CRIACAO', 
        '2025-10-08 00:16:15.196241', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'aluno_teste', 
        'ALT_DT_ATUALIZACAO', 
        '2025-10-08 00:16:15.196241', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'aluno_teste_resposta', 
        'ATR_DT_CRIACAO', 
        '2025-10-08 00:52:14.112527', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'aluno_teste_resposta_historico', 
        'ATH_DT_CRIACAO', 
        '2025-04-22 21:19:40.656666', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'ano_letivo', 
        'ANO_DT_CRIACAO', 
        '43430,7940856482', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'ano_letivo', 
        'ANO_DT_ATUALIZACAO', 
        '2024-12-28 13:46:29.733451', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'area', 
        'ARE_DT_CRIACAO', 
        '2025-09-24 20:38:03.588377', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'area', 
        'ARE_DT_ATUALIZACAO', 
        '2025-09-24 20:38:03.588377', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'avaliacao', 
        'AVA_DT_CRIACAO', 
        '2025-10-01 15:00:18.892141', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'avaliacao', 
        'AVA_DT_ATUALIZACAO', 
        '2025-10-01 15:00:18.892141', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'avaliacao_municipio', 
        'AVM_DT_CRIACAO', 
        '2025-10-07 18:27:32.128810', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'avaliacao_municipio', 
        'AVM_DT_ATUALIZACAO', 
        '2025-10-07 18:27:32.128810', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'avaliacao_municipio', 
        'AVM_DT_INICIO', 
        '45952,9999884259', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'avaliacao_municipio', 
        'AVM_DT_FIM', 
        '45961,9999884259', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'avaliacao_municipio', 
        'AVM_DT_DISPONIVEL', 
        '45945,9999884259', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'avaliacao_online', 
        'createdAt', 
        '2024-02-11 12:21:36.658537', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'avaliacao_online', 
        'updatedAt', 
        '2024-02-11 12:21:36.658537', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'avaliacao_online_page', 
        'createdAt', 
        '2024-02-11 12:21:37.508845', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'avaliacao_online_page', 
        'updatedAt', 
        '2024-02-11 12:21:37.508845', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'avaliacao_online_question', 
        'createdAt', 
        '2024-02-11 12:21:37.516373', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'avaliacao_online_question', 
        'updatedAt', 
        '2024-02-11 12:21:37.516373', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'avaliacao_online_question_alternative', 
        'createdAt', 
        '2024-02-11 12:21:37.558969', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'avaliacao_online_question_alternative', 
        'updatedAt', 
        '2024-02-11 12:21:37.558969', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'disciplina', 
        'DIS_DT_CRIACAO', 
        '2025-01-24 20:47:55.918240', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'disciplina', 
        'DIS_DT_ATUALIZACAO', 
        '2025-01-24 20:47:55.918240', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'escola', 
        'ESC_DT_CRIACAO', 
        '2025-08-25 14:04:29.328064', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'escola', 
        'ESC_DT_ATUALIZACAO', 
        '45937,6540972222', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'estados', 
        'createdAt', 
        '2024-06-29 20:14:54.549212', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'estados', 
        'updatedAt', 
        '2024-06-29 20:14:54.549212', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'forget_password', 
        'createdAt', 
        '2025-10-07 18:18:01.009027', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'forget_password', 
        'updatedAt', 
        '45938,0052199074', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'formacao', 
        'FOR_DT_CRIACAO', 
        '45861', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'formacao', 
        'FOR_DT_ATUALIZACAO', 
        '45861', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'genero', 
        'GEN_DT_CRIACAO', 
        '2023-02-01 00:50:35.330161', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'genero', 
        'GEN_DT_ATUALIZACAO', 
        '2023-02-01 00:50:35.330161', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'infrequencia', 
        'IFR_DT_CRIACAO', 
        '2025-10-07 20:00:03.136082', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'infrequencia', 
        'IFR_DT_ATUALIZACAO', 
        '45937,8762384259', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'job', 
        'startDate', 
        '45937,8750231481', 
        '%Y-%m-%d %H:%M:%S'
    ),
    (
        'job', 
        'endDate', 
        '45937,9244212963', 
        '%Y-%m-%d %H:%M:%S'
    ),
    (
        'job', 
        'createdAt', 
        '2025-10-07 21:00:02.059694', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'job', 
        'updatedAt', 
        '45937,9244212963', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'matriz_referencia', 
        'MAR_DT_CRIACAO', 
        '2025-04-10 21:08:37.781835', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'matriz_referencia', 
        'MAR_DT_ATUALIZACAO', 
        '45884,772962963', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'matriz_referencia_topico', 
        'MTO_DT_CRIACAO', 
        '2025-04-10 21:08:37.801774', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'matriz_referencia_topico', 
        'MTO_DT_ATUALIZACAO', 
        '2025-04-10 21:08:37.801774', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'matriz_referencia_topico_items', 
        'MTI_DT_CRIACAO', 
        '2025-08-15 18:33:04.406466', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'matriz_referencia_topico_items', 
        'MTI_DT_ATUALIZACAO', 
        '2025-08-15 18:33:04.406466', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'messages', 
        'MEN_DT_CRIACAO', 
        '2025-10-07 12:12:29.354230', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'messages', 
        'MEN_DT_ATUALIZACAO', 
        '2025-10-07 12:12:29.354230', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'municipio', 
        'MUN_DT_INICIO', 
        '45863,9999884259', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'municipio', 
        'MUN_DT_FIM', 
        '47581,9999884259', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'municipio', 
        'MUN_DT_CRIACAO', 
        '2025-08-25 12:35:46.256545', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'municipio', 
        'MUN_DT_ATUALIZACAO', 
        '45929,5254282407', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'pcd', 
        'PCD_DT_CRIACAO', 
        '2021-02-24 13:51:44.925000', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'pcd', 
        'PCD_DT_ATUALIZACAO', 
        '2021-02-24 13:51:44.925000', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'perfil_base', 
        'PER_DT_CRIACAO', 
        '2023-02-07 11:52:45.796161', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'perfil_base', 
        'PER_DT_ATUALIZACAO', 
        '2023-02-07 11:52:45.796161', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'professor', 
        'PRO_DT_NASC', 
        '47068', 
        '%Y-%m-%d %H:%M:%S'
    ),
    (
        'professor', 
        'PRO_DT_CRIACAO', 
        '2025-10-07 17:51:55.672728', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'professor', 
        'PRO_DT_ATUALIZACAO', 
        '2025-10-07 17:51:55.672728', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'raca', 
        'PEL_DT_CRIACAO', 
        '44818,8823263889', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'raca', 
        'PEL_DT_ATUALIZACAO', 
        '44818,8823263889', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'regionais', 
        'createdAt', 
        '2025-09-16 06:31:37.024283', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'regionais', 
        'updatedAt', 
        '2025-09-16 06:31:37.024283', 
        '%Y-%m-%d %H:%M:%S.%f %Z'

    ),
    (
        'report_descriptor', 
        'createdAt', 
        '2025-10-07 22:11:09.986854', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'report_descriptor', 
        'updatedAt', 
        '2025-10-07 22:11:09.986854', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'report_edition', 
        'createdAt', 
        '2025-10-07 03:25:44.603737', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'report_edition', 
        'updatedAt', 
        '2025-10-07 03:25:44.603737', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'report_not_evaluated', 
        'createdAt', 
        '2025-10-07 22:11:10.140317', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'report_not_evaluated', 
        'updatedAt', 
        '2025-10-07 22:11:10.140317', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'report_race', 
        'createdAt', 
        '2025-10-07 22:11:09.302546', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'report_race', 
        'updatedAt', 
        '2025-10-07 22:11:09.302546', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'report_subject', 
        'createdAt', 
        '2025-10-07 22:11:08.670194', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'report_subject', 
        'updatedAt', 
        '2025-10-07 22:11:08.670194', 
        '%Y-%m-%dT%H:%M:%S.%f'
    ),
    (
        'series', 
        'SER_DT_CRIACAO', 
        '44735,0915046296', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'series', 
        'SER_DT_ATUALIZACAO', 
        '44964,7521296296', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'sub_perfil', 
        'SPE_DT_CRIACAO', 
        '2025-08-12 19:05:02.935962', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'sub_perfil', 
        'SPE_DT_ATUALIZACAO', 
        '2025-08-12 19:05:02.935962', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'teste', 
        'TES_DT_CRIACAO', 
        '2025-10-01 15:06:15.073511', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'teste', 
        'TES_DT_ATUALIZACAO', 
        '45937,8279050926', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'teste_gabarito', 
        'TEG_DT_CRIACAO', 
        '2025-10-01 14:59:25.105152', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'teste_gabarito', 
        'TEG_DT_ATUALIZACAO', 
        '45937,8233680556', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'transferencia', 
        'TRF_DT_CRIACAO', 
        '2025-10-07 23:38:22.918988', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'transferencia', 
        'TRF_DT_ATUALIZACAO', 
        '45937,9849768519', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'turma', 
        'TUR_DT_CRIACAO', 
        '2025-10-06 19:24:17.859408', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'turma', 
        'TUR_DT_ATUALIZACAO', 
        '45937,8166898148', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),
    (
        'turma_aluno', 
        'startDate', 
        '45938', 
        '%Y-%m-%d'
    ),
    (
        'turma_aluno', 
        'endDate', 
        '45938', 
        '%Y-%m-%d'
    ),
    (
        'turma_aluno', 
        'createdAt', 
        '2025-10-08 00:22:09.871911', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'turma_aluno', 
        'updatedAt', 
        '45938,0199537037', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'usuario', 
        'USU_DT_CRIACAO', 
        '2025-10-07 18:18:00.978442', 
        '%Y-%m-%d %H:%M:%S.%f %Z'
    ),
    (
        'usuario', 
        'USU_DT_ATUALIZACAO', 
        '45937,9959722222', 
        '%Y-%m-%d %H:%M:%S %Z'
    ),

]

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

    except Exception:
        # Em caso de qualquer erro inesperado, retorna a tupla original
        return valor_data


# Demonstração
print("--- Testando conversões ---")
for tabela, campo, valor, formato in formatos_de_datas:
    data_convertida = converter_data(
        valor_data=valor,
        formato_entrada=formato, 
        formato_saida='%Y-%m-%d %H:%M:%S.%f'
        )
    print(f"[{tabela}].[{campo}]: '{valor}' -> {data_convertida}")