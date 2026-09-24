import io

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="MVP DataViz", page_icon="📊", layout="wide")

st.title("MVP DataViz")
st.caption("Carregue um CSV, explore os dados e gere uma visualizacao rapidamente.")

uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])

if uploaded_file is None:
	st.info("Envie um arquivo CSV para iniciar a analise.")
	st.stop()

try:
	data = pd.read_csv(io.BytesIO(uploaded_file.getvalue()))
except Exception as error:
	st.error(f"Nao foi possivel ler o CSV: {error}")
	st.stop()

if data.empty:
	st.warning("O arquivo nao possui registros.")
	st.stop()

metric_columns = st.columns(3)
metric_columns[0].metric("Linhas", f"{len(data):,}".replace(",", "."))
metric_columns[1].metric("Colunas", len(data.columns))
metric_columns[2].metric("Valores ausentes", int(data.isna().sum().sum()))

st.subheader("Amostra dos dados")
st.dataframe(data.head(100), use_container_width=True)

numeric_columns = data.select_dtypes(include="number").columns.tolist()
if len(numeric_columns) < 2:
	st.warning("O CSV precisa ter pelo menos duas colunas numericas para gerar um grafico.")
	st.stop()

st.subheader("Visualizacao")
axis_columns = st.columns(2)
x_column = axis_columns[0].selectbox("Eixo X", numeric_columns)
y_column = axis_columns[1].selectbox(
	"Eixo Y",
	numeric_columns,
	index=1 if len(numeric_columns) > 1 else 0,
)

chart_type = st.radio("Tipo de grafico", ["Dispersao", "Linha", "Barras"], horizontal=True)

if chart_type == "Dispersao":
	figure = px.scatter(data, x=x_column, y=y_column, title=f"{y_column} por {x_column}")
elif chart_type == "Linha":
	figure = px.line(data, x=x_column, y=y_column, title=f"{y_column} ao longo de {x_column}")
else:
	figure = px.bar(data, x=x_column, y=y_column, title=f"{y_column} por {x_column}")

figure.update_layout(hovermode="closest")
st.plotly_chart(figure, use_container_width=True)
