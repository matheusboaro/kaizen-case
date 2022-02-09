from json import load
import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(rc={'figure.figsize':(15,8.27)})
sns.set(font_scale=1)


st.title('Kaizen - Case Análise de dados')

def load_data(path):

    return pd.read_csv(path)




my_cmap_1 = plt.get_cmap("coolwarm")

rescale_1 = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y)+1)


#Inicio do código do visual
df = load_data('cleaned_database.csv')
st.header('Leads (Visão Geral)')

labels = df['Status'].unique().tolist()
st.subheader('Status das negociações (Geral)')
values_count = df['Status'].value_counts().tolist()
sizes = [(int(value)/len(df['Status']))*100 for value in values_count]
explode = (0.1,0,0,0)
fig, ax = plt.subplots()
ax.pie(sizes, explode=explode,labels = labels, autopct='%1.1f%%',shadow=True,startangle=90,textprops={'fontsize': 28},colors=my_cmap_1(rescale_1([i for i in range(len(labels))])))
#ax.set_title('Status das leads (Geral)',fontsize= 34)
ax.axis('equal')
st.pyplot(fig)
st.text(" ")
st.text(" ")
st.subheader('Status das leads por vendedor')
st.text(" ")
st.pyplot(sns.catplot(y='Vendedor',kind='count',hue='Status',data=df).set_xlabels('Quantidade'))

st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")



st.header('Objeções das negociações não concluídas ou não pagas.')
st.subheader('Objeções dos leads com status "Pendente"')
nao_concluidos = df[df['Status']=='Pendente']
values_count = nao_concluidos['Objeção'].value_counts().tolist()
labels = nao_concluidos['Objeção'].unique().tolist()
sizes = [(int(value)/len(nao_concluidos['Objeção']))*100 for value in values_count]
fig2, ax2 = plt.subplots()
ax2.pie(sizes, labels = labels, autopct='%1.1f%%',shadow=True,startangle=90,textprops={'fontsize': 28},colors=my_cmap_1(rescale_1([i for i in range(len(labels))])))
#ax2.set_title('Objeções dos leads',fontsize= 34)
ax2.axis('equal')

st.pyplot(fig2)
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.subheader('Objeções dos leads com status "Contatado"')
st.text(" ")

nao_concluidos = df[df['Status']=='Contatado']
values_count = nao_concluidos['Objeção'].value_counts().tolist()
labels = nao_concluidos['Objeção'].unique().tolist()
sizes = [(int(value)/len(nao_concluidos['Objeção']))*100 for value in values_count]
fig3, ax3 = plt.subplots()
ax3.pie(sizes, labels = labels, autopct='%1.1f%%',shadow=True,startangle=90,textprops={'fontsize': 28},colors=my_cmap_1(rescale_1([i for i in range(len(labels))])))
#ax3.set_title('Objeções dos leads',fontsize= 34)
ax3.axis('equal')
st.pyplot(fig3)
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")

st.header('Informações de vendedores')
st.text(" ")

status_names = df.Status.unique().tolist()

option = st.selectbox('Status da negociação',['Todas']+status_names )
if option =='Todas':
    total_receita_por_vendedor = df.groupby(['Vendedor'],as_index=False).sum()
else:
    total_receita_por_vendedor = df[df['Status']==option].groupby(['Vendedor'],as_index=False).sum()
#ax = sns.barplot(sns.barplot(x="Vendedor",y="Valor", data = total_receita_por_vendedor).set_title('Receita gerada por vendedor',fontsize=28))
names = total_receita_por_vendedor.Vendedor.tolist()
values = total_receita_por_vendedor.Valor.tolist()

my_cmap = plt.get_cmap("coolwarm")
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
fig4,ax4 = plt.subplots()
ax4.bar(names,values,color=my_cmap(rescale(values)))


ax4.set_title('Valores das negociações por vendedor',fontsize= 34)
st.pyplot(fig4)


with st.container():
    option = st.selectbox('Vendedor',df['Vendedor'].unique())
    dados_vendedor = df[df['Vendedor']==option]
    st.header('Negociações - {}'.format(option))
    col4, col1, col2, col3,col5 = st.columns(5)
    col4.metric('Qtd. de leads',df.Valor[df['Vendedor']==option].count())
    col1.metric("Valor Médio", df.Valor[df['Vendedor']==option].mean())
    col2.metric("Maior Valor", df.Valor[df['Vendedor']==option].max())
    col3.metric("Valor Total",df.Valor[df['Vendedor']==option].sum())
    col5.metric("Taxa de conclusão (%)",str(float(dados_vendedor.Status[dados_vendedor['Status']=='Concluído'].count()/dados_vendedor.Status.count())*100)+'%')
 

    dados_vendedor = df[df['Vendedor']==option]
    names = dados_vendedor.Status.value_counts().tolist()
    values = dados_vendedor.Status.unique().tolist()

    st.subheader('')
    my_cmap = plt.get_cmap("coolwarm")
    rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y)+1)
    fig5,ax5 = plt.subplots()
    ax5.pie(names, labels = values, autopct='%1.1f%%',shadow=True,startangle=90,textprops={'fontsize': 20},colors=my_cmap(rescale(names)))
    ax5.set_title('Status das negociações do vendedor {}'.format(option),fontsize= 28)
    
    st.pyplot(fig5)

    option_2 = st.selectbox('Clientes',dados_vendedor['Nome do lead'].unique())

    col1, col2,col3 = st.columns(3)
    col1.metric("Nomes", option_2)
    col2.metric("E-mail", dados_vendedor['E-mail do lead'][df['Nome do lead']==option_2].iloc[0])
    col3.metric("Telefone",dados_vendedor['Telefone do lead'][df['Nome do lead']==option_2].iloc[0])

    col4, col5,col6 = st.columns(3)
    col1.metric("Valor", dados_vendedor['Valor'][df['Nome do lead']==option_2].iloc[0])
    col2.metric("Status", dados_vendedor['Status'][df['Nome do lead']==option_2].iloc[0])
    col3.metric("Objeção",dados_vendedor['Objeção'][df['Nome do lead']==option_2].iloc[0])
    #col5.metric("Taxa de conclusão (%)",str(float(dados_vendedor.Status[dados_vendedor['Status']=='Concluído'].count()/dados_vendedor.Status.count())*100)+'%')