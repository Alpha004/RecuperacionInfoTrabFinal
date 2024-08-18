import pandas as pd
import streamlit as st
import plotly.express as px

# Configuración inicial del layout de la página
st.set_page_config(
    page_title="Graficas de Medicion",
    page_icon="ahorra-energia.png",
    layout="wide"
)

st.title("Graficas y KPIs")
col1, col2 = st.columns([2, 2])
# Leer los datos
data = pd.read_csv("final_df_labels.csv", low_memory=False, sep=',', encoding='utf-8')

data['datetime'] = pd.to_datetime(data['datetime'])
df_failures = data[data['failure'] != 'none']
df_failures['month'] = df_failures['datetime'].dt.to_period('M')
failures_per_month = df_failures.groupby('month').size()
failures_per_month.index = failures_per_month.index.strftime('%B %Y')
# failures_per_month['month'] = pd.to_datetime(failures_per_month['month']).strftime("%B")
#$ print(failures_per_month)

# KPI 2: FALLAS POR MAQUINA
failures_per_machine = df_failures['machineID'].value_counts().sort_index()
# KPI 3: FALLAS POR PARTES
part_means = data.groupby('failure')[['Part_1', 'Part_2', 'Part_3', 'Part_4']].mean()

# Mostrar el KPI 1: Tasa de Crecimiento Anual de la Población
with col1:
    st.subheader("KPI 1: Tasa de Fallas por Mes")
    st.bar_chart(failures_per_month, color="#52eb34")
    st.write("**Nota:** Los valores del eje Y representan cantidad.")
    
with col2:
    st.subheader("KPI 2: Tasa de Fallas por Maquina")
    st.line_chart(failures_per_machine, color="#17ade8")
    st.write("**Nota:** Los valores del eje Y representan cantidad.")
    
st.divider()
col3, col4 = st.columns([4,0.1])
with col3:
    st.subheader("KPI 3: Tasa de Promedios de Fallas en base a las partes de la maquina")
    fig2 = px.bar(part_means, orientation='h', height=370, labels={'value': 'Promedio de fallas por partes'})
    fig2.update_layout(xaxis_showgrid=False)
    st.plotly_chart(fig2)
    st.write("**Nota:** Los valores del eje Y representan promedios.")