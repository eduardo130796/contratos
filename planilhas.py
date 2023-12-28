import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    arquivo1 = 'emergencia 2021.xlsx'
    arquivo2 = 'emergencias 2022.xlsx'
    arquivo3 = 'emergencial 2023.xlsx'

    df1 = pd.read_excel(arquivo1)
    df2 = pd.read_excel(arquivo2)
    df3 = pd.read_excel(arquivo3)

    data = pd.concat([df1, df2, df3], ignore_index=True)
    data['Valor Total'] = pd.to_numeric(data['Valor Total'], errors='coerce')
    data['Vigente até'] = pd.to_datetime(data['Vigente até'], errors='coerce')

    return data

data = load_data()

def formatar_para_real(valor):
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

st.title('Dashboard de Análise de Contratos')

st.sidebar.header('Filtros')
regiao = st.sidebar.multiselect('Selecione a Região', data['Região'].unique())
ano = st.sidebar.multiselect('Selecione o Ano', data['Ano'].unique(), default=[2021, 2022, 2023])
modo_visao = st.sidebar.radio("Modo de Visualização", ["Por Ano", "Por Região"])

filtered_data = data
if regiao:
    filtered_data = filtered_data[filtered_data['Região'].isin(regiao)]
if ano:
    filtered_data = filtered_data[filtered_data['Ano'].isin(ano)]

st.header('Valor Total dos Contratos por Ano (2021-2023)')
contratos_por_ano = filtered_data.groupby('Ano')['Valor Total'].sum().reset_index()
fig1 = px.bar(contratos_por_ano, x='Ano', y='Valor Total', labels={'Valor Total': 'Valor Total (R$)'},text_auto='.2s')
fig1.update_traces(textposition='outside')
fig1.update_layout(yaxis=dict(title='Valor Total (R$)', ticksuffix='R$ '), xaxis=dict(title='Ano', type='category'))
st.plotly_chart(fig1)

contratos_por_ano['Valor Total'] = contratos_por_ano['Valor Total'].apply(formatar_para_real)
st.table(contratos_por_ano)

st.header('Valor Total dos Contratos por Região')

if modo_visao == "Por Ano":
    valor_total_por_regiao = filtered_data.groupby(['Ano', 'Região'])['Valor Total'].sum().reset_index()
    fig = px.bar(valor_total_por_regiao, x='Ano', y='Valor Total', color='Região', barmode='group', labels={'Valor Total': 'Valor Total (R$)'}, text_auto='.2s')
    fig.update_layout(yaxis=dict(title='Valor Total (R$)', ticksuffix='R$ '), xaxis=dict(title='Ano', type='category'))
    st.plotly_chart(fig)
    valor_total_por_regiao['Valor Total'] = valor_total_por_regiao['Valor Total'].apply(formatar_para_real)
    st.table(valor_total_por_regiao)
else:
    valor_total_por_regiao = filtered_data.groupby('Região')['Valor Total'].sum().reset_index()
    fig = px.bar(valor_total_por_regiao, x='Região', y='Valor Total', labels={'Valor Total': 'Valor Total (R$)'}, text_auto='.2s')
    fig.update_layout(yaxis=dict(title='Valor Total (R$)', ticksuffix='R$ '), xaxis=dict(title='Região', type='category'))
    st.plotly_chart(fig)
    valor_total_por_regiao['Valor Total'] = valor_total_por_regiao['Valor Total'].apply(formatar_para_real)
    st.table(valor_total_por_regiao)

st.header('Quantidade de Contratos por Região')
if modo_visao == "Por Ano":
    quantidade_por_regiao_ano = filtered_data.groupby(['Ano', 'Região']).size().reset_index(name='Quantidade')
    fig3 = px.bar(quantidade_por_regiao_ano, x='Ano', y='Quantidade', color='Região', barmode='group',text_auto='.2s')
else:
    quantidade_por_regiao_total = filtered_data.groupby('Região').size().reset_index(name='Quantidade')
    fig3 = px.bar(quantidade_por_regiao_total, x='Região', y='Quantidade')

fig3.update_layout(xaxis=dict(title='Região' if modo_visao == "Por Região" else 'Ano', type='category'), yaxis=dict(title='Quantidade'))
st.plotly_chart(fig3)

if modo_visao == "Por Ano":
    st.table(quantidade_por_regiao_ano)
else:
    st.table(quantidade_por_regiao_total)
