## Instalações
#pip install workadays

## Importaçõe
import smtplib
import email.message
#from datetime import datetime
from datetime import datetime, timedelta #Pegar data e hora
from workadays import workdays as wd
import streamlit as st  # Daskboard
import pandas as pd  # Le Arquivos
import yfinance as y #Importar dados do Yahoo

def Robo():
    st.header('***Robô que envia email com o valor do dolar***')

    """end_date = datetime.date.today()
    data_e_hora_atuais = datetime.now()
    data_em_texto = end_date.strftime('%d/%m/%Y')
    hora_em_texto = end_date.strftime('%H:%M')
    end_date2 = datetime.date.today()
    end = pd.to_datetime(end_date2)"""



    presente = datetime.now()
    ontem = presente - timedelta(1)
    anteontem = presente - timedelta(2)
    data_em_texto = presente.strftime('%d/%m/%Y')
    hora_em_texto = presente.strftime('%H:%M')


    dolarfechamento = y.download("USDBRL=X", presente, presente)

    if((wd.is_weekend(presente) is True) and (wd.is_weekend(ontem) is True)):#Se hoje é domingo e ontem é sabado pega dados de sexta
        dolarfechamentoAnteontem = y.download("USDBRL=X", anteontem, anteontem)
        FechamentodolarAnteontem = dolarfechamentoAnteontem["Close"].iloc[0]
        dolar = round(FechamentodolarAnteontem, 4)
    if((wd.is_weekend(presente) is True) and (wd.is_weekend(ontem) is False)):#Se hoje é sabado e ontem foi sexta pega dados de sexta
        dolarfechamentoontem = y.download("USDBRL=X", ontem, ontem)
        FechamentodolarOntem = dolarfechamentoontem["Close"].iloc[0]
        dolar = round(FechamentodolarOntem, 4)
    if(wd.is_workday(presente) is True):
        FechamentoDolar = dolarfechamento["Close"].iloc[0]
        dolar = round(FechamentoDolar,4)

    DolarEmReais = str(dolar).replace('.', ',')

    emailuser = st.sidebar.text_input('Digite seu email', 'seuemail@gmail.com')

    st.markdown("<h4 style='color:#F00;'>Funcionalidades do Robo</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:#F00;'>O robo recebe o email digitado pelo usuario e envia um email com a data, hora e o valor do dolar em real.</h4>", unsafe_allow_html=True)
   # st.write('O robo recebe o email digitado pelo usuario e envia um email com a data, hora e o valor do dolar em real.')
    st.markdown(f"<h5>Hoje é dia: {data_em_texto}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5>E agora são: {hora_em_texto}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5>O valor do dolar em real: {DolarEmReais}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5>Para testar o robo basta digitar seu email no campo ao lado.</h5>", unsafe_allow_html=True)

    corpo_email = f"""
    <p>Hoje é dia: {data_em_texto}</p>
    <p>E agora são: {hora_em_texto}</p>
    <p>O valor do dolar em real: {dolar}</p>
    """

    msg = email.message.Message()
    msg['Subject'] = "Email Automático"
    msg['From'] = 'tamara.zoner@gmail.com'
    msg['To'] = emailuser
    password = 'twbpevvsbnbjhpnr'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    if emailuser != "seuemail@gmail.com":
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        st.markdown(f"<h3 style='color:#F00;'>Email enviado com suscesso para {emailuser} </h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    Robo()