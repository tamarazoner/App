## Instalações
# pip install matplotlib
# pip install plotly
# pip install plot
# pip install yfinance
# pip install pandas_datareader
# pip install numpy
# pip install seaborn

## Importações
import pandas as pd  # Le Arquivos
import streamlit as st  # Framework de Data Science
import datetime #Pegar data e hora
import yfinance as y #Importar dados do Yahoo
import matplotlib.pyplot as plt # Gráficos
import seaborn as sns
import numpy as np

#%matplotlib inline

def Analise():
    # Nome do Página
    st.header('***Analise de Com Yahoo***')

    start = datetime.date(2021,1,1)
    end = datetime.date.today()

    start = datetime.date.strftime(start, "%d/%m/%Y")
    end = datetime.date.strftime(end, "%d/%m/%Y")

    start_date = st.sidebar.text_input('Digite uma dada de início', start)
    end_date = st.sidebar.text_input('Digite uma dada de fim', end)

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    # Escolhendo o Ativo para o Robô
    ativo_escolha1 = st.sidebar.text_input('Escolha sua primeira ação', 'petr4.sa')
    petr = y.download(ativo_escolha1, start, end)

    ativo_escolha2 = st.sidebar.text_input('Escolha sua segunda ação', 'vale3.sa')
    vale = y.download(ativo_escolha2, start, end)

    ativo_escolha3 = st.sidebar.text_input('Escolha sua terceira ação', 'itub4.sa')
    itub = y.download(ativo_escolha3, start, end)

    ativo_escolha4 = st.sidebar.text_input('Escolha sua quarta ação', 'wege3.sa')
    wege = y.download(ativo_escolha4, start, end)

    ibov = y.download('^bvsp', start, end)

    st.markdown(f"<h3 style='color:#F00;'>Tabelas com o último dia da cada ação</h3>", unsafe_allow_html=True)
    st.markdown(f"<h5>{ativo_escolha1}</h5>", unsafe_allow_html=True)
    petr.columns = ['Abertura','Alto', 'Baixo', 'Fechamento', 'Adj Close', 'Volume']
    st.write(petr.tail(1))
    st.markdown(f"<h5>{ativo_escolha2}</h5>", unsafe_allow_html=True)
    vale.columns = ['Abertura', 'Alto', 'Baixo', 'Fechamento', 'Adj Close', 'Volume']
    st.write(vale.tail(1))
    st.markdown(f"<h5>{ativo_escolha3}</h5>", unsafe_allow_html=True)
    itub.columns = ['Abertura', 'Alto', 'Baixo', 'Fechamento', 'Adj Close', 'Volume']
    st.write(itub.tail(1))
    st.markdown(f"<h5>{ativo_escolha4}</h5>", unsafe_allow_html=True)
    wege.columns = ['Abertura', 'Alto', 'Baixo', 'Fechamento', 'Adj Close', 'Volume']
    st.write(wege.tail(1))

    #Criando um For para normalização dos Retornos da Carteira
    #Normalizando os Preços - |  - Retorno Acumulado
    #na base 100 ou na base 1
    # Normalização permite comparar uma ação com outra ou outras pois normalizar é colocar na mesma base.
    # retorno_acm = (1+btg_retorno).cumprod()   -   retorno_acm.ploy()
    # df_geral = pd.merge(ibov_retorno_acm, retorno_acm, how='inner', on = 'Date').plot(figsize=(10,10)
    #st.markdown(f"<h4 style='color:#F00;'>Normalização permite comparar uma ação com outra ou outras pois normalizar é colocar na mesma base</h4>", unsafe_allow_html=True)
    for papeis in (petr, vale, itub, wege):
      papeis['Retorno Normalizado'] = papeis['Adj Close'] / papeis['Adj Close'].iloc[0]  #Normalizando os Retornos
    #st.write(papeis['Retorno Normalizado'])
    #st.line_chart(papeis['Retorno Normalizado'])

    #st.line_chart((carteira / carteira.iloc[0]))
    #Alocando R$$ de acordo com o peso das carteira Capital Inicial de R$10.000,00
    #25% petr, 25% vale, 25% itub, 25% wege
    #Alocando o peso de cada papel

    #-----------------------------------------------------------------------------------------------------
    #Mapa de Correlação
    st.markdown(f"<h3 style='color:#F00;'>Gráfico de Correlação da Carteira</h3>", unsafe_allow_html=True)
    papeisbolsa = [ativo_escolha1, ativo_escolha2, ativo_escolha3, ativo_escolha4]
    carteirabolsa = y.download(papeisbolsa, start, end)['Adj Close']
    sns.heatmap(carteirabolsa.corr(), annot=True, cmap="Wistia")
    plt.show()
    st.pyplot(plt)

    #--------------------------------------------------------------------------------------------------------------
    st.markdown(
        f"<h4 >Normalização permite comparar uma ação com outra ou outras pois normalizar é colocar na mesma base</h4>",
        unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:#F00;'>Para um investimento de R$ 10.00,00 vamos distribuir os peso da carteira ficando 25% por ação</h4>", unsafe_allow_html=True)
    for papeis, peso in zip((petr, vale, itub, wege), [.25, .25, .25, .25]):
      papeis['Alocacao'] = papeis['Retorno Normalizado'] * peso
    petr.columns = ['Abertura', 'Alto', 'Baixo', 'Fechamento', 'Fechamento Ajustado', 'Volume', 'Retorno Normatizado', 'Alocacao']
    #novo = petr['Alocacao']
    #st.write(novo)
    #st.line_chart(novo)
    #Calculando o Valor de acordo com seu peso de cada papel na carteira
    # Valor de Patrimonio por papel
    # 1.000,00 de investimento por papel

    for papeis in (petr, vale, itub, wege):
      papeis['Valor Posicao'] = papeis ['Alocacao'] * 10000
    #st.write(papeis['Valor Posicao'])

    #Calculando o Retorno em R$$ da carteira de acordo com cada peso
    # Cada busca feita em um papel é igual a uma aba do excel
    # Para apurarmos o retorno da carteira de acordo com o seu peso que será o valor aplicado. Temos que unir tudo isso
    # em uma aba só e para isso vamos usar o Concat
    st.markdown(f"<h4 style='color:#F00;'>Retorno Acumulado da Carteira por Ação</h4>", unsafe_allow_html=True)
    valor_posicoes = [petr['Valor Posicao'], vale['Valor Posicao'], itub['Valor Posicao'], wege['Valor Posicao']]
    valor_carteira = pd.concat(valor_posicoes, axis= 1)
    st.line_chart(valor_carteira)


    # axis pega somente a linha, sem ele vai pegar a coluna inteira

    #----------------------------------------------------------------------------------------------------------

    #st.markdown("<h3 style='color:#F00;'>Renomeando os Titulos dos Ativos ou Colunas</h3>", unsafe_allow_html=True)
    #Renomeando os Titulos dos Ativos ou Colunas
    #valor_carteira.columns = ['Petro', 'Vale', 'Itub', 'Wege']
    valor_carteira.columns = [ativo_escolha1, ativo_escolha2, ativo_escolha3, ativo_escolha4]
    #st.write(valor_carteira)

    #-------------------------------------------------------------------------------------------------------
    st.markdown("<h4 style='color:#F00;'>Retorno Acumulado da Carteira e Retorno Acumulado Total Investido Não Normalizado</h3>", unsafe_allow_html=True)
    #Calculando o Retorno da Carteira
    valor_carteira['Total R$'] = valor_carteira.sum(axis=1)
    valor_carteira.columns = [ativo_escolha1, ativo_escolha2, ativo_escolha3, ativo_escolha4, 'Total R$']
    st.line_chart(valor_carteira)


    #---------------------------------------------------------------------------------------------------------

    st.markdown("<h4 style='color:#F00;'>Tabela com Retorno Acumulado da Carteira Normalizado</h4>", unsafe_allow_html=True)
    (valor_carteira['Total R$'] / valor_carteira['Total R$'].iloc[0]).plot(figsize=(10,8), label="Carteira")
    (ibov['Adj Close'] /  ibov['Adj Close'].iloc[0]).plot(label="Ibovespa")
   # plt.legend()
    st.write(valor_carteira)
    #Exibir Gráficamente de foma Normalizada Todos os Ativos da Carteira
    st.markdown("<h4 style='color:#F00;'>Gráfico com Retorno Acumulado da Carteira Normalizado</h4>", unsafe_allow_html=True)
    st.line_chart(valor_carteira / valor_carteira.iloc[0])#.plot(figsize=(10,6))

    #-------------------------------------------------------------------------------------------------------
    # Aula 35
    st.markdown("<h4 style='color:#F00;'>Calculo do Retorno Diário da Carteira</h4>", unsafe_allow_html=True)
    #Calculo do Retorno Diário da Carteira Últimos 5
    valor_carteira['Retorno Diário'] = valor_carteira['Total R$'].pct_change() * 100
    #st.write(valor_carteira['Retorno Diário'])
    st.area_chart(valor_carteira['Retorno Diário'])

    #st.markdown("<h3 style='color:#F00;'>Calculo do Retorno Diário da Carteira Últimos 5</h3>", unsafe_allow_html=True)
    valor_carteira.columns = [ativo_escolha1, ativo_escolha2, ativo_escolha3, ativo_escolha4, 'Total R$', 'Retorno Diário']
    #st.write(valor_carteira.tail(5))
    # --------------------------------------------------------------------------------------------------------

    st.markdown("<h4 style='color:#F00;'>Retorno Médio Diário da Carteira em Porcentagem</h4>", unsafe_allow_html=True)
    #Calculo do Retorno Médio Diário da Carteira
    retorno_diario=valor_carteira['Retorno Diário'].mean()
    retorno_diario_medio = round(retorno_diario,4)
    retorno_diario_medio_porcentagem = str(retorno_diario_medio).replace('.', ',')
    st.markdown(f"<h5>{retorno_diario_medio_porcentagem} %</h5>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------------------------------------------

    st.markdown("<h4 style='color:#F00;'>DESVIO PADÃO Diário da Carteira</h4>", unsafe_allow_html=True)
    #Calculo do DESVIO PADÃO Diário da Carteira
    desvio_padrao = valor_carteira['Retorno Diário'].std()
    desvio_padrao_diario = round(desvio_padrao, 4)
    desvio_padrao_ = str(desvio_padrao_diario).replace('.', ',')
    st.markdown(f"<h5>{desvio_padrao_} %</h5>", unsafe_allow_html=True)

    #---------------------------------------------------------------------------------------------------------

    #Calculo da Distribuição Diário da Carteira. Usando um Gráfico de Linha no modelo Histograma.
    valor_carteira['Retorno Diário'].plot(kind='kde', figsize=(8,5))

    #Calculando o Retorno ACUMULADO da carteira
    st.markdown("<h4 style='color:#F00;'>Retorno da Carteira em Porcentagem</h4>", unsafe_allow_html=True)
    retorno_aplicacao = (valor_carteira['Total R$'][-1] / valor_carteira['Total R$'][0] -1) * 100
    # retorno em Porcentagem
    retorno = round(retorno_aplicacao,4)
    retorno_percentagem = str(retorno).replace('.', ',')
    st.markdown(f"<h5 >{retorno_percentagem} %</h5>", unsafe_allow_html=True)
    # ---------------------------------------------------------------------------------------------------------

    st.markdown(f"<h3 style='color:#F00;'>Comprarando o Retorno da Carteira com o Ibovespa</h3>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='color:#F00;'>Gráfico Normalizado da Carteira com o Ibovespa</h5>", unsafe_allow_html=True)
    papeis = [ativo_escolha1, ativo_escolha2, ativo_escolha3,  ativo_escolha4, '^bvsp']
    # Comprarando o Retorno da Carteira com o Ibovespa e Exibindo no Gráfico Normalizado (Todos Ativos da Carteira em um único Ativo, Média dos ativos)
   #st.markdown("<h1 style='color:#F00;'>Pegando Fechamento Ajustado da Carteira no Yahoo dos últimos 5 dias</h1>", unsafe_allow_html=True)
    #Pegando Dados da Carteira no Yahoo
    carteira = y.download(papeis, start, end)['Adj Close']
    #carteira.columns = ['B2W Digital', 'Lojas Americanas', 'Saraiva', 'Ibovespa']
    #carteira.columns = [ativo_escolha1, ativo_escolha2, ativo_escolha3,  ativo_escolha4, 'Ibovespa']
    #st.write(carteira.tail())

    #Mostrando o Resultado da Carteira no Gráfico NORMALIZADO
    #st.line_chart((carteira / carteira.iloc[0]).plot(figsize=(10,8)))
    st.line_chart((carteira / carteira.iloc[0]))



if __name__ == "__main__":
    Analise()