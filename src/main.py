from Class import CSVReader, ValidaData

# Caminho para o arquivo CSV
file_path = 'FILE_TEST.csv'
file_path_true = 'FILE_VERDADE.csv'


if __name__ == '__main__':
    
    csv_reader = CSVReader()
    
    data_file = csv_reader.read_csv(file_path, ";", "infer")
    data_file_verdade = csv_reader.read_csv(file_path_true, ";", "infer")


    valida_data = ValidaData()    
     
    ## VALIDACOES 
    data_file['VALIDACAO_CPF'] = data_file['CPF_FUNCIONARIO'].apply(valida_data.validar_cpf) 

    data_file['VALIDACAO_CNPJ'] = data_file['CNPJ'].apply(valida_data.validar_cnpj)

    data_file['VALIDACAO_NOME'] = data_file['NOME_FUNCIONARIO'].apply(valida_data.valida_nome)



    ## RELATORIOS 
    rel_data = valida_data.min_max_data(data_file, "DT_REAL_EFETIVACAO_CREDITO")

    #print(rel_data)

    #print(data_file.head())

    ## CONTAGEM DE CPF VALIDOS 
    qtd_validacao_cpf = valida_data.agregar_contar(data_file, 'VALIDACAO_CPF')

    qtd_validacao_cnpj = valida_data.agregar_contar(data_file, 'CNPJ')

    #print(qtd_validacao.head())

    ## VALIDACAO DE JOINS 


    valida_data.valida_relatorio_contrato(data_file, data_file_verdade, "NU_CONTRATO")







