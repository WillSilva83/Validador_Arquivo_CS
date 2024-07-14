import pandas as pd 

class CSVReader:
    def __init__(self) -> None:
        pass

    def read_csv(self, file_path: str, delimiter: str, header: str):
        try:
            data = pd.read_csv(filepath_or_buffer = file_path,
                               delimiter = delimiter, 
                               header = header)
            return data 
        except Exception as e: 
            print(f"Erro ao ler o arquivo: {e}")
            return None
        
class ValidaData:
    def __init__(self) -> None:
        pass

    def validar_cpf(self, cpf: str) -> bool:
    
        # Remover caracteres não numéricos
        cpf = ''.join([c for c in cpf if c.isdigit()])

        # Verificar se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return False

        # Verificar se todos os dígitos são iguais (CPFs inválidos conhecidos)
        if cpf == cpf[0] * 11:
            return False

        # Validar primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        primeiro_dv = (soma * 10 % 11) % 10
        if primeiro_dv != int(cpf[9]):
            return False

        # Validar segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        segundo_dv = (soma * 10 % 11) % 10
        if segundo_dv != int(cpf[10]):
            return False

        return True

    def valida_nome(self, nome: str) -> bool: 
        return not any(char.isdigit() for char in nome)

    def validar_cnpj(self, cnpj: str) -> bool:
        # Remover caracteres não numéricos
        cnpj = ''.join([c for c in cnpj if c.isdigit()])

        # Verificar se o CNPJ tem 14 dígitos
        if len(cnpj) != 14:
            return False

        # Verificar se todos os dígitos são iguais (CNPJs inválidos conhecidos)
        if cnpj == cnpj[0] * 14:
            return False

        def calcular_digito(cnpj, pos):
            if pos == 1:
                pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            elif pos == 2:
                pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

            soma = sum(int(cnpj[i]) * pesos[i] for i in range(len(pesos)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        # Validar primeiro dígito verificador
        primeiro_dv = calcular_digito(cnpj, 1)
        if primeiro_dv != int(cnpj[12]):
            return False

        # Validar segundo dígito verificador
        segundo_dv = calcular_digito(cnpj, 2)
        if segundo_dv != int(cnpj[13]):
            return False

        return True

    def agregar_contar(self, dataframe: pd.DataFrame, coluna: str) -> pd.DataFrame:
        """
        Agrega o DataFrame por uma coluna específica e faz a contagem dos valores.

        Parameters:
        dataframe (pd.DataFrame): O DataFrame a ser agregado.
        coluna (str): O nome da coluna para agrupar.

        Returns:
        pd.DataFrame: DataFrame agregado com contagem dos valores.
        """
        # Verifica se a coluna existe no DataFrame
        if coluna not in dataframe.columns:
            raise ValueError(f"A coluna '{coluna}' não existe no DataFrame.")
        
        # Agrupa o DataFrame pela coluna especificada e conta os valores
        resultado = dataframe.groupby(coluna).size().reset_index(name='contagem')
        
        return resultado

    def min_max_data(self, dataframe: pd.DataFrame, coluna: str):
        """
        Retorna o valor mínimo (MIN) e máximo (MAX) de uma coluna de data em um DataFrame.

        Parameters:
        dataframe (pd.DataFrame): O DataFrame que contém a coluna.
        coluna (str): O nome da coluna de data.

        Returns:
        tuple: Uma tupla contendo as datas mínima e máxima no formato de string.
        """
            # Verifica se a coluna existe no DataFrame
        if coluna not in dataframe.columns:
            raise ValueError(f"A coluna '{coluna}' não existe no DataFrame.")
        
        # Converte a coluna para o tipo datetime, se necessário
        if not pd.api.types.is_datetime64_any_dtype(dataframe[coluna]):
            dataframe[coluna] = pd.to_datetime(dataframe[coluna], dayfirst=True)
        
        # Calcula o valor mínimo e máximo
        data_min = dataframe[coluna].min()
        data_max = dataframe[coluna].max()
        saida = f'''
            Data Min da coluna {coluna}: {data_min.strftime('%d/%m/%Y')}
            Data Max da coluna {coluna}: {data_max.strftime('%d/%m/%Y')}
        '''
        return saida

    def join_e_diferenca(self, df1: pd.DataFrame, df2: pd.DataFrame, chave: str, tipo_join: str = 'left') -> pd.DataFrame:
        """
        Faz um join entre dois DataFrames e retorna as diferenças.

        Parameters:
        df1 (pd.DataFrame): O primeiro DataFrame.
        df2 (pd.DataFrame): O segundo DataFrame.
        chave (str): A coluna chave para o join.
        tipo_join (str): O tipo de join a ser realizado (default: 'left').

        Returns:
        pd.DataFrame: DataFrame contendo as diferenças.
        """
        # Realiza o join entre os dois DataFrames
        df_joined = pd.merge(df1, df2, on=chave, how=tipo_join, suffixes=('_df1', '_df2'))

        # Identifica as colunas que não são a chave
        colunas_comuns = set(df1.columns).intersection(set(df2.columns)) - {chave}

        # Inicializa uma lista para armazenar as diferenças
        diferencas = []

        # Compara as colunas comuns e armazena as diferenças
        for coluna in colunas_comuns:
            col_df1 = f"{coluna}_df1"
            col_df2 = f"{coluna}_df2"
            diferentes = df_joined[df_joined[col_df1] != df_joined[col_df2]]
            diferencas.append(diferentes)

        # Concatena todas as diferenças encontradas
        resultado = pd.concat(diferencas).drop_duplicates()

        return resultado
    
    def valida_relatorio_contrato(self, df_origem: pd.DataFrame, df_verdade: pd.DataFrame, chave: str) -> list: 
        '''
        
        '''
        df_join = pd.merge(df_origem, df_verdade, on=chave, how="right", suffixes=("_df_origem", "_df_verdade"))

        df_join_nulos = df_join[df_join['CPF_FUNCIONARIO'].isnull()]

        return df_join_nulos

