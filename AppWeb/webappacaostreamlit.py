# ok - Abrindo no Chorme o App Web
# streamlit run webappacaostreamlit.py

## Instalações
# pip install streamlit
# pip install gspread

# Biblioteca
from AnaliseComYahoo import Analise
from RoboEmail import Robo
import streamlit as st

# %%writefile app.py

LANGUAGE_CODE = 'pt-br'
USE_I18N = True

st.sidebar.title('Menu')
paginaSelecionada = st.sidebar.selectbox('Selecione uma opção',
                                         ['Analise Com Yahoo', 'Robô que envia Email'])
st.title('**Web App de Analise de Ações**')


if paginaSelecionada == 'Analise Com Yahoo':
    Yahoo = Analise()
elif paginaSelecionada == 'Robô que envia Email':
    Email = Robo()