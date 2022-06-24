import streamlit as st
import pandas as pd
import numpy_financial as npf
import numpy as np
from numpy import number
from requests import options

header = st.container()
dataset = st.container()
#features = st.container()
#model_training = st.container()

with header:
    st.title('Create an amortization table for your loan')
    st.write("""Here you can find out what the interest and payments are during the term of your loan. 
    Remember that it is the analysis when your credit is fixed rate and fixed payment""")
    sel_col, disp_col = st.columns(2)
    n_pay = int(sel_col.number_input('How many periods?'))
    type_periods = disp_col.selectbox("Period type?", options=['A','M'], index=0)
    rate = sel_col.number_input('what is the interest rate? (%)')
    type_rate = disp_col.selectbox("Rate type?", options=['EM','EA','NM','NA'], index=0)
    loan = int(sel_col.number_input('what is the value of the loan?'))

    rate = rate/100

    if type_periods == 'A':
        n_pay = n_pay * 12
    else: 
        n_pay = n_pay
    

    if type_rate == 'EA':
        rate_EA = rate
        rate_EM = ((1+rate_EA)**(1/12))-1
        rate_NA = (((1+rate_EA)**(1/1))-1)*1
        rate_NM = rate_NA/12

    elif type_rate == 'NA':
        rate_NA = rate
        rate_NM = rate_NA/12
        rate_EA = (1+(rate_NA/12))**12-1
        rate_EM = ((1+rate_EA)**(1/12))-1

    elif type_rate == 'NM': 
        rate_NM = rate
        rate_NA = rate_NM*12
        rate_EA = (1+(rate_NA/12))**12-1
        rate_EM = ((1+rate_EA)**(1/12))-1
    
    else:
        rate_EM = rate
        rate_EA = ((1+rate_EM)**(12/1))-1
        rate_NA = (((1+rate_EA)**(1/1))-1)*1
        rate_NM = rate_NA/12

    loan_final = round(loan*(1+rate_EM)**n_pay,0)
    pay = round(npf.pmt(rate_EM, n_pay, -loan, 0), 0)

with dataset:
    if st.button('calculate'):
        st.write('at the end of the period, this will be the total amount paid',loan_final)
        st.write('the monthly fee payable is' , pay)
        st.write('#### Amortization table')
        
        datos=[]
        balance = loan

        for i in range(1, n_pay+1):
            pay_capital = npf.ppmt(rate_EM, i, n_pay, -loan, 0)
            interest = pay - pay_capital
            balance -= pay_capital  
            line = [i, format(pay, '0,.0f'), format(pay_capital, '0,.0f'), format(interest, '0,.0f'), format(balance, '0,.0f')]
            datos.append(line)
        
        df_datos = pd.DataFrame(datos)
        df_datos.columns = ['Periods', 'Payment', 'Capital', 'interest', 'balance']
        df_datos = df_datos.set_index('Periods')
        st.dataframe(df_datos, width=None, height=None)

        st.write('#### Rate conversions')
        st.write('EM' , round(rate_EM*100,2),'%')
        st.write('EA' , round(rate_EA*100,2),'%')
        st.write('NM' , round(rate_NM*100,2),'%')
        st.write('NA' , round(rate_NA*100,2),'%')
    


# with features:
#     st.header('contenedor features')

# with model_training:
#     st.header('contenedor model traning')