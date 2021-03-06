import streamlit as st
from joblib import load
import pandas as pd
from utils import Transformador



def avaliar_mau(dict_respostas):
	modelo = load('objetos/modelo.joblib')
	features = load('objetos/features.joblib')

	if dict_respostas['Anos_desempregado'] > 0:
		dict_respostas['Anos_empregado'] = dict_respostas['Anos_desempregado'] * -1 
	
	respostas = []
	for coluna in features:
		respostas.append(dict_respostas[coluna])

	df_novo_cliente = pd.DataFrame(data=[respostas], columns=features)

	mau = modelo.predict(df_novo_cliente)[0]

	return mau


# Imagem com o logo do formulário
st.image('img/rodrigobank.png')
# Titulo do formulário
#st.write('# Simulador de Avaliação de Crédito')

st.markdown("<h1 style='text-align: center; color: white;'>Simulador de Avaliação de Crédito</h1>", unsafe_allow_html=True)

# Criando o objeto expander
my_expander_1 = st.beta_expander('Trabalho')
my_expander_2 = st.beta_expander('Pessoal')
my_expander_3 = st.beta_expander('Familia')

# Carregando o dicionario de campos para o expander
# Formato do dicionario: {nome da coluna : lista com todos os possiveis valores que essa coluna pode ter}
lista_campos = load('objetos/lista_campos.joblib')

# Criando um dicionario para salvar as respostas
dict_respostas = {}

# Abrindo o objeto expander para editar dentro
with my_expander_1:
    # Criando duas colunas dentro do objeto
    col1_form, col2_form = st.beta_columns(2)
    # Manipulando a primeira coluna e criando uma caixa de seleção
    dict_respostas['Categoria_de_renda'] = col1_form.selectbox('Qual a categoria de renda ?', lista_campos['Categoria_de_renda'])
    # Manipulando a primeira coluna e criando um slider
    dict_respostas['Ocupacao'] = col1_form.selectbox('Qual a Ocupação ?', lista_campos['Ocupacao'])
    # Manipulando a segunda coluna e criando uma caixa de seleção
    dict_respostas['Tem_telefone_trabalho'] = 1 if col1_form.selectbox('Tem um telefone do trabalho ?' , ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Rendimento_Anual'] = col2_form.slider('Qual o salario mensal ?', help='Podemos mover a barra usando as setas do teclado', min_value=0, max_value=35000, step=500) * 12
    
    dict_respostas['Anos_empregado'] = col2_form.slider('Quantos anos empregado ?', help='Podemos mover a barra usando as setas do teclado', min_value=0, max_value=50, step=1)

    dict_respostas['Anos_desempregado'] = col2_form.slider('Quantos anos desempregado ?', help='Podemos mover a barra usando as setas do teclado', min_value=0, max_value=50, step=1)



with my_expander_2:

    col3_form, col4_form = st.beta_columns(2)

    dict_respostas['Grau_Escolaridade'] = col3_form.selectbox('Qual o Grau de Escolaridade ?', lista_campos['Grau_Escolaridade'])

    dict_respostas['Estado_Civil'] = col3_form.selectbox('Qual o Estado Civil ?', lista_campos['Estado_Civil'])

    dict_respostas['Tem_Carro'] = 1 if col3_form.selectbox('Tem um Carro ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tem_telefone_fixo'] = 1 if col4_form.selectbox('Tem um telefone fixo ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tem_email'] = 1 if col4_form.selectbox('Tem um email ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Idade'] = col4_form.slider('Qual a idade ?', help='Podemos mover a barra usando as setas do teclado', min_value=0, max_value=100, step=1)

with my_expander_3:

    col4_form, col5_form = st.beta_columns(2)

    dict_respostas['Moradia'] = col4_form.selectbox('Qual o tipo de moradia ?', lista_campos['Moradia'])

    dict_respostas['Tem_Casa_Propria'] = 1 if col4_form.selectbox('Tem Casa Propria ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tamanho_Familia'] = col5_form.slider('Qual o tamanho da familia ?', help='Podemos mover a barra usando as setas do teclado', min_value=1, max_value=20, step=1)

    dict_respostas['Qtd_Filhos'] = col5_form.slider('Quantos filhos ?', help='Podemos mover a barra usando as setas do teclado', min_value=0, max_value=20, step=1)


if st.button('Avaliar crédito'):
    if avaliar_mau(dict_respostas):
        st.error('Crédito Negado')
    else:
        st.success('Crédito Aprovado')

 


