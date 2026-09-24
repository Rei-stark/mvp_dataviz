import json
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATASETS_PATH = Path(__file__).parent / "datasets"
APP_TITLE = "NEXORA metrics | C-Level Analytics | Generative BI"

COLUMN_LABELS = {
    "order_id": "ID do pedido", "customer_id": "ID do cliente", "customer_unique_id": "ID único do cliente",
    "customer_zip_code_prefix": "CEP do cliente", "customer_city": "Cidade do cliente", "customer_state": "Estado do cliente",
    "order_status": "Status do pedido", "order_purchase_timestamp": "Data e hora da compra", "order_approved_at": "Data de aprovação",
    "order_delivered_carrier_date": "Data de envio à transportadora", "order_delivered_customer_date": "Data de entrega",
    "order_estimated_delivery_date": "Data estimada de entrega", "product_id": "ID do produto", "seller_id": "ID do vendedor",
    "price": "Preço do item", "freight_value": "Valor do frete", "payment_value": "Valor pago", "payment_type": "Forma de pagamento",
    "payment_sequential": "Sequência do pagamento", "payment_installments": "Parcelas", "installments": "Parcelas",
    "review_score": "Nota da avaliação", "category": "Categoria", "item_count": "Itens por pedido", "seller_count": "Vendedores por pedido",
    "gmv": "Receita de produtos", "purchase_date": "Data da compra", "month": "Mês", "purchase_week": "Semana da compra",
    "delivery_days": "Prazo de entrega (dias)", "delay_days": "Atraso (dias)", "is_late": "Entrega atrasada",
    "revenue": "Receita", "orders": "Pedidos", "customers": "Clientes", "value": "Valor", "size": "Quantidade",
    "ticket_medio": "Ticket médio", "revenue_per_customer": "Receita por cliente", "review": "Nota média",
    "avg_review": "Nota média", "late_rate": "Taxa de atraso", "revenue_trend": "Tendência da receita",
}

STATE_LABELS = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia", "CE": "Ceará",
    "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul", "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
    "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins",
    "Unknown": "Não informado",
}

STATUS_LABELS = {
    "Delivered": "Entregue", "Shipped": "Enviado", "Canceled": "Cancelado", "Unavailable": "Indisponível",
    "Invoiced": "Faturado", "Processing": "Em processamento", "Created": "Criado", "Approved": "Aprovado",
}

PAYMENT_LABELS = {
    "credit_card": "Cartão de crédito", "boleto": "Boleto", "voucher": "Vale-presente",
    "debit_card": "Cartão de débito", "not_defined": "Não definido",
}

CATEGORY_LABELS = {
    "beleza saude": "Beleza e saúde", "cama mesa banho": "Cama, mesa e banho", "informatica acessorios": "Informática e acessórios",
    "telefonia": "Telefonia", "moveis decoracao": "Móveis e decoração", "esporte lazer": "Esporte e lazer",
    "utilidades domesticas": "Utilidades domésticas", "automotivo": "Automotivo", "brinquedos": "Brinquedos",
    "perfumaria": "Perfumaria", "bebes": "Bebês", "eletronicos": "Eletrônicos", "ferramentas jardim": "Ferramentas e jardim",
    "construcao ferramentas construcao": "Construção e ferramentas", "pet shop": "Pet shop", "papelaria": "Papelaria",
    "relogios presentes": "Relógios e presentes", "artes": "Artes", "livros": "Livros", "musica": "Música",
}

DATASET_CATALOG = {
    "olist_orders_dataset.csv": "Pedidos, status e datas de compra, aprovação e entrega",
    "olist_customers_dataset.csv": "Clientes, cidades, estados e identificadores de recorrência",
    "olist_order_items_dataset.csv": "Itens, produtos, vendedores, preços e fretes",
    "olist_order_payments_dataset.csv": "Pagamentos, formas de pagamento, valores e parcelas",
    "olist_order_reviews_dataset.csv": "Avaliações dos pedidos em escala de 1 a 5",
    "olist_products_dataset.csv": "Produtos e categorias originais",
    "olist_sellers_dataset.csv": "Vendedores, cidades e estados de origem",
    "olist_geolocation_dataset.csv": "Coordenadas geográficas por CEP",
    "product_category_name_translation.csv": "Tradução de categorias do catálogo",
}

METRIC_DEFINITIONS = {
    "payment_value": "valor total pago pelo pedido em reais",
    "gmv": "soma dos preços dos produtos em reais",
    "freight_value": "soma do frete em reais",
    "order_id": "quantidade de pedidos distintos",
    "customer_unique_id": "quantidade de clientes distintos",
    "review_score": "nota média das avaliações de 1 a 5",
    "delivery_days": "mediana de dias entre compra e entrega",
    "delay_days": "mediana de dias de atraso em relação à previsão",
    "is_late": "percentual de pedidos entregues após a previsão",
    "item_count": "quantidade média ou total de itens por pedido",
}

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink: #e8edf3; --muted: #8d9aaa; --line: #263241; --teal: #5de1c7; --gold: #f0bb63; --navy: #0c1118; }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: radial-gradient(circle at 80% -10%, #163142 0, #0c1118 38%); color: var(--ink); }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.02em; }
    h1 { font-size: 2.2rem !important; }
    [data-testid="stMetric"] { background: linear-gradient(135deg, #14202a, #10171f); border: 1px solid var(--line); padding: 15px 18px; border-radius: 8px; }
    [data-testid="stMetricValue"] { color: var(--teal); }
    [data-testid="stSidebar"] { background: #0b1016; border-right: 1px solid var(--line); }
    .eyebrow { color: var(--teal); font-size: .75rem; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; }
    .insight { border-left: 3px solid var(--gold); background: #151d25; padding: 12px 16px; border-radius: 0 7px 7px 0; margin: 8px 0 16px; }
    .source-note { color: var(--muted); font-size: .8rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Construindo o modelo analitico Olist...")
def carregar_modelo_olist():
    def read(name, **kwargs):
        return pd.read_csv(DATASETS_PATH / name, **kwargs)

    orders = read("olist_orders_dataset.csv", parse_dates=[
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_customer_date", "order_estimated_delivery_date",
    ])
    customers = read("olist_customers_dataset.csv")
    items = read("olist_order_items_dataset.csv")
    payments = read("olist_order_payments_dataset.csv")
    reviews = read("olist_order_reviews_dataset.csv", usecols=["order_id", "review_score"])
    products = read("olist_products_dataset.csv", usecols=["product_id", "product_category_name"])
    categories = read("product_category_name_translation.csv")

    category_lookup = categories.rename(columns={
        "product_category_name": "category_original",
        "product_category_name_english": "category",
    })
    products = products.merge(
        category_lookup, left_on="product_category_name", right_on="category_original", how="left"
    )
    products["category"] = products["product_category_name"].fillna(products["category"])
    item_details = items.merge(products[["product_id", "category"]], on="product_id", how="left")
    item_rollup = item_details.groupby("order_id", as_index=False).agg(
        item_count=("order_item_id", "count"),
        gmv=("price", "sum"),
        freight_value=("freight_value", "sum"),
        seller_count=("seller_id", "nunique"),
    )
    item_category = (
        item_details.groupby(["order_id", "category"], dropna=False)["price"].sum()
        .reset_index()
        .sort_values(["order_id", "price"], ascending=[True, False])
        .drop_duplicates("order_id")
        [["order_id", "category"]]
    )
    item_rollup = item_rollup.merge(item_category, on="order_id", how="left")

    payment_rollup = payments.groupby("order_id", as_index=False).agg(
        payment_value=("payment_value", "sum"),
        payment_type=("payment_type", "first"),
        installments=("payment_installments", "max"),
    )
    review_rollup = reviews.groupby("order_id", as_index=False).agg(review_score=("review_score", "mean"))

    fact = orders.merge(customers, on="customer_id", how="left")
    fact = fact.merge(item_rollup, on="order_id", how="left")
    fact = fact.merge(payment_rollup, on="order_id", how="left")
    fact = fact.merge(review_rollup, on="order_id", how="left")
    fact["category"] = fact["category"].fillna("nao_informado")
    fact["payment_value"] = fact["payment_value"].fillna(fact["gmv"] + fact["freight_value"])
    fact["gmv"] = fact["gmv"].fillna(0)
    fact["freight_value"] = fact["freight_value"].fillna(0)
    fact["item_count"] = fact["item_count"].fillna(0)
    fact["purchase_date"] = fact["order_purchase_timestamp"].dt.date
    fact["month"] = fact["order_purchase_timestamp"].dt.to_period("M").astype(str)
    fact["purchase_week"] = fact["order_purchase_timestamp"].dt.to_period("W").astype(str).str[:10]
    fact["delivery_days"] = (
        fact["order_delivered_customer_date"] - fact["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    fact["delay_days"] = (
        fact["order_delivered_customer_date"] - fact["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400
    fact["is_late"] = fact["delay_days"].fillna(0) > 0
    fact["order_status"] = fact["order_status"].str.title()
    fact["payment_type"] = fact["payment_type"].fillna("not_defined")
    fact["customer_state"] = fact["customer_state"].fillna("Unknown")
    fact["customer_city"] = fact["customer_city"].fillna("Unknown")
    fact["category"] = fact["category"].fillna("nao_informado").str.replace("_", " ").str.lower()
    fact["category"] = fact["category"].map(lambda value: CATEGORY_LABELS.get(value, value.capitalize()))
    return fact.sort_values("order_purchase_timestamp")


@st.cache_data(show_spinner="Preparando mapa de origem...")
def carregar_geografia():
    geo = pd.read_csv(
        DATASETS_PATH / "olist_geolocation_dataset.csv",
        usecols=["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"],
    )
    return geo.groupby("geolocation_zip_code_prefix", as_index=False).agg(
        lat=("geolocation_lat", "median"), lon=("geolocation_lng", "median")
    )


def moeda(value):
    return f"R$ {value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def percentual(value):
    return f"{value:.1f}%".replace(".", ",")


def rotulo_coluna(column):
    return COLUMN_LABELS.get(column, str(column).replace("_", " ").capitalize())


def traduzir_serie(series, labels):
    return series.map(lambda value: labels.get(value, value))


def traduzir_tabela(data):
    translated = data.rename(columns={column: rotulo_coluna(column) for column in data.columns}).copy()
    for column, labels in (("Estado do cliente", STATE_LABELS), ("Status do pedido", STATUS_LABELS), ("Forma de pagamento", PAYMENT_LABELS)):
        if column in translated.columns:
            translated[column] = traduzir_serie(translated[column], labels)
    if "Entrega atrasada" in translated.columns:
        translated["Entrega atrasada"] = translated["Entrega atrasada"].map({True: "Sim", False: "Não"})
    return translated


def get_openai_key():
    try:
        return st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    except Exception:
        return os.getenv("OPENAI_API_KEY")


def resumo_ia(data):
    numeric = data.select_dtypes("number").columns.tolist()
    context_dimensions = [
        "month", "customer_state", "customer_city", "category",
        "payment_type", "order_status", "purchase_date",
    ]
    return {
        "rows": len(data),
        "columns": data.columns.tolist(),
        "catalogo_tabelas": DATASET_CATALOG,
        "metricas_disponiveis": METRIC_DEFINITIONS,
        "numeric_summary": data[numeric].describe().round(2).to_dict() if numeric else {},
        "dimension_values": {
            column: {
                str(value): int(count)
                for value, count in data[column].astype("string").value_counts().head(12).items()
            }
            for column in context_dimensions
            if column in data.columns
        },
    }


def normalizar_especificacao(specification, question):
    normalized = dict(specification)
    filters = dict(normalized.get("filters") or {})
    question_lower = question.lower()
    state_aliases = {
        "minas gerais": "MG", "sao paulo": "SP", "são paulo": "SP",
        "rio de janeiro": "RJ", "espirito santo": "ES", "espírito santo": "ES",
        "parana": "PR", "paraná": "PR", "rio grande do sul": "RS",
    }
    for state_name, state_code in state_aliases.items():
        if state_name in question_lower:
            filters["customer_state"] = state_code
            break
    if isinstance(filters.get("customer_state"), str):
        filters["customer_state"] = state_aliases.get(
            filters["customer_state"].lower(), filters["customer_state"].upper()
        )
    normalized["chart_type"] = normalized.get("chart_type", "bar").lower()
    if normalized["chart_type"] not in {"bar", "line", "area", "pie", "scatter"}:
        normalized["chart_type"] = "bar"
    normalized["aggregation"] = normalized.get("aggregation", "sum").lower()
    if normalized["aggregation"] not in {"sum", "mean", "count"}:
        normalized["aggregation"] = "sum"
    normalized["filters"] = filters
    return normalized


def aplicar_filtros_especificacao(data, specification):
    scoped = data
    for column, value in (specification.get("filters") or {}).items():
        if column not in scoped.columns:
            continue
        values = value if isinstance(value, list) else [value]
        scoped = scoped[scoped[column].isin(values)]
    if scoped.empty:
        raise ValueError("A pergunta nao encontrou registros no recorte solicitado.")
    return scoped


def gerar_grafico_ia(data, specification):
    data = aplicar_filtros_especificacao(data, specification)
    dimension = specification.get("dimension", "month")
    breakdown = specification.get("breakdown")
    metric = specification.get("metric", "payment_value")
    chart_type = specification.get("chart_type", "bar")
    aggregation = specification.get("aggregation", "sum")
    limit = max(3, min(int(specification.get("limit", 12)), 30))
    if dimension not in data.columns or metric not in data.columns:
        raise ValueError("A IA escolheu uma coluna que nao esta disponivel no modelo.")
    if breakdown and breakdown not in data.columns:
        breakdown = None

    if breakdown and breakdown != dimension:
        top_breakdowns = (
            data.groupby(breakdown, dropna=False)[metric].sum()
            .nlargest(limit)
            .index
        )
        data = data[data[breakdown].isin(top_breakdowns)]
    group_columns = [dimension] + ([breakdown] if breakdown and breakdown != dimension else [])

    if aggregation == "mean":
        grouped = data.groupby(group_columns, dropna=False)[metric].mean().reset_index(name="value")
    elif aggregation == "count":
        grouped = data.groupby(group_columns, dropna=False).size().reset_index(name="value")
    else:
        grouped = data.groupby(group_columns, dropna=False)[metric].sum().reset_index(name="value")
    if metric == "is_late" and aggregation == "mean":
        grouped["value"] *= 100
    grouped = grouped.dropna(subset=[dimension, "value"])
    if not breakdown:
        grouped = grouped.sort_values("value", ascending=False).head(limit)
    dimension_label = rotulo_coluna(dimension)
    breakdown_label = rotulo_coluna(breakdown) if breakdown else None
    rename_map = {dimension: dimension_label, "value": rotulo_coluna(metric)}
    if breakdown:
        rename_map[breakdown] = breakdown_label
    grouped = grouped.rename(columns=rename_map)
    metric_label = rotulo_coluna(metric)
    title = specification.get("title", "Visualizacao gerada pela IA")
    chart_labels = {dimension_label: dimension_label, metric_label: metric_label}
    if breakdown_label:
        chart_labels[breakdown_label] = breakdown_label

    if chart_type == "line":
        figure = px.line(grouped.sort_values(dimension_label), x=dimension_label, y=metric_label, color=breakdown_label, markers=True, title=title, labels=chart_labels)
    elif chart_type == "area":
        figure = px.area(grouped.sort_values(dimension_label), x=dimension_label, y=metric_label, color=breakdown_label, markers=True, title=title, labels=chart_labels)
    elif chart_type == "pie":
        figure = px.pie(grouped, names=dimension_label, values=metric_label, hole=.48, title=title, labels=chart_labels)
    elif chart_type == "scatter":
        figure = px.scatter(grouped, x=dimension_label, y=metric_label, color=breakdown_label, title=title, labels=chart_labels)
    else:
        figure = px.bar(grouped, x=dimension_label, y=metric_label, color=breakdown_label, title=title, labels=chart_labels, color_continuous_scale="Tealgrn")
    if metric == "is_late" and aggregation == "mean":
        figure.update_yaxes(ticksuffix="%")
    figure.update_layout(margin=dict(l=10, r=10, t=60, b=10), height=440)
    return figure


def responder_ia(question, data):
    key = get_openai_key()
    if not key:
        return None, "Configure OPENAI_API_KEY para ativar a Generative BI. A aplicacao ja esta pronta para receber a chave com seguranca."
    try:
        from openai import OpenAI
    except ImportError:
        return None, "Instale a dependencia openai com `pip install openai` para ativar a aba de IA."

    client = OpenAI(api_key=key)
    prompt = f"""
Voce e o copiloto de analytics da NEXORA. Converta o pedido do gestor em uma consulta visual estruturada sobre os dados reais.
Responda SOMENTE JSON valido com as chaves: title, chart_type, dimension, breakdown, metric, aggregation, limit, filters, insight.
chart_type deve ser bar, line, area, pie ou scatter. aggregation deve ser sum, mean ou count.
Use breakdown para uma segunda dimensao (ex.: receita mensal por categoria -> dimension=month e breakdown=category).
metric deve usar uma coluna real ou uma metrica do dicionario. Para percentual de atraso, use metric=is_late e aggregation=mean.
filters deve ser um objeto com filtros exatos por coluna, usando os valores listados no contexto. Para perguntas sobre cidades de um estado, SEMPRE inclua customer_state com a sigla correta (ex.: Minas Gerais = MG).
Use apenas colunas presentes no contexto. Escolha a melhor visualizacao para a decisao e escreva um insight baseado no recorte.
Pedido do gestor: {question}
Contexto do modelo: {json.dumps(resumo_ia(data), default=str, ensure_ascii=False)}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Voce responde em portugues do Brasil e nunca inventa colunas."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        specification = normalizar_especificacao(
            json.loads(response.choices[0].message.content), question
        )
        return specification, None
    except Exception as error:
        return None, f"Nao foi possivel consultar a IA: {error}"


def metricas_executivas(data):
    total = data["payment_value"].sum()
    order_count = len(data)
    late_rate = data["is_late"].mean() * 100 if order_count else 0
    avg_delivery = data["delivery_days"].median()
    return total, order_count, late_rate, avg_delivery


df = carregar_modelo_olist()

st.sidebar.markdown('<div class="eyebrow">NEXORA / PILOTO</div>', unsafe_allow_html=True)
st.sidebar.title("Central de controle")
st.sidebar.caption("Analytics executivo com Generative BI")

min_date = df["purchase_date"].min()
max_date = df["purchase_date"].max()
date_range = st.sidebar.slider("Janela de pedidos", min_date, max_date, (min_date, max_date), format="DD/MM/YYYY")
states = st.sidebar.multiselect(
    "Estados", sorted(df["customer_state"].dropna().unique()), default=[],
    format_func=lambda state: STATE_LABELS.get(state, state), placeholder="Selecione uma ou mais opções",
)
statuses = st.sidebar.multiselect(
    "Status do pedido", sorted(df["order_status"].dropna().unique()), default=[],
    format_func=lambda status: STATUS_LABELS.get(status, status), placeholder="Selecione uma ou mais opções",
)
categories = st.sidebar.multiselect(
    "Categorias", sorted(df["category"].dropna().unique()), default=[],
    placeholder="Selecione uma ou mais opções",
)
top_n = st.sidebar.slider("Principais itens nas visões", min_value=5, max_value=20, value=10)
st.sidebar.markdown("[Desenvolvido por Reinaldo Galvão](mailto:reinaldogalvao@gmail.com)")

filtered = df[df["purchase_date"].between(date_range[0], date_range[1])].copy()
if states:
    filtered = filtered[filtered["customer_state"].isin(states)]
if statuses:
    filtered = filtered[filtered["order_status"].isin(statuses)]
if categories:
    filtered = filtered[filtered["category"].isin(categories)]

st.markdown('<div class="eyebrow">NEXORA METRICS</div>', unsafe_allow_html=True)
st.title(APP_TITLE)
st.caption("Uma lente operacional para transformar o ecossistema Olist em decisões de negócio.")
st.markdown(f'<p class="source-note">{len(filtered):,} pedidos no recorte atual · dados Olist · periodo {date_range[0].strftime("%d/%m/%Y")} a {date_range[1].strftime("%d/%m/%Y")}</p>', unsafe_allow_html=True)

total_revenue, order_count, late_rate, avg_delivery = metricas_executivas(filtered)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("GMV transacionado", moeda(total_revenue))
kpi2.metric("Pedidos", f"{order_count:,}".replace(",", "."))
kpi3.metric("Atraso logistico", percentual(late_rate), delta_color="inverse")
kpi4.metric("Mediana de entrega", f"{avg_delivery:.1f} dias" if pd.notna(avg_delivery) else "n/a")

executive_tab, revenue_tab, customer_tab, operations_tab, geo_tab, ai_tab = st.tabs([
    "Pulso executivo", "Receita e mix", "Clientes", "Operações", "Geografia", "Generative BI",
])

with executive_tab:
    st.subheader("O pulso do negocio")
    monthly = filtered.groupby("month", as_index=False).agg(revenue=("payment_value", "sum"), orders=("order_id", "nunique"))
    trend_window_max = max(1, min(6, len(monthly)))
    trend_window = st.slider("Suavizacao da tendencia (meses)", 1, trend_window_max, 1, key="executive_trend_window")
    monthly["revenue_trend"] = monthly["revenue"].rolling(trend_window, min_periods=1).mean()
    left, right = st.columns([1.45, 1])
    with left:
        fig = px.area(monthly, x="month", y="revenue_trend", markers=True, title="Receita mensal ajustável", color_discrete_sequence=["#5de1c7"], labels={"month": "Mês", "revenue_trend": "Tendência da receita"})
        fig.update_layout(height=390, margin=dict(l=10, r=10, t=55, b=10), yaxis_title="Receita (R$)", xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        status = filtered.groupby("order_status", as_index=False).size().sort_values("size", ascending=False)
        status_limit_max = max(1, len(status))
        status_limit = st.slider("Status exibidos", 1, status_limit_max, min(4, status_limit_max), key="executive_status_limit")
        status = status.head(status_limit)
        status["status_label"] = traduzir_serie(status["order_status"], STATUS_LABELS)
        fig = px.pie(status, names="status_label", values="size", hole=.62, title="Mix de status", color_discrete_sequence=px.colors.qualitative.Safe, labels={"status_label": "Status do pedido", "size": "Quantidade"})
        fig.update_layout(height=390, margin=dict(l=10, r=10, t=55, b=10), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    top_category = filtered.groupby("category")["payment_value"].sum().nlargest(1)
    if not top_category.empty:
        st.markdown(f'<div class="insight"><strong>Sinal executivo:</strong> {top_category.index[0]} lidera o recorte com {moeda(top_category.iloc[0])} em receita. Use as abas de Receita e Operacoes para decompor o movimento.</div>', unsafe_allow_html=True)

with revenue_tab:
    st.subheader("Receita, ticket e concentracao")
    category_count = max(1, filtered["category"].nunique())
    category_limit = st.slider("Categorias exibidas", 1, min(20, category_count), min(top_n, category_count), key="revenue_category_limit")
    left, right = st.columns(2)
    with left:
        category_revenue = filtered.groupby("category", as_index=False).agg(revenue=("payment_value", "sum"), orders=("order_id", "nunique"))
        category_revenue = category_revenue.nlargest(category_limit, "revenue")
        fig = px.bar(category_revenue.sort_values("revenue"), x="revenue", y="category", orientation="h", title="Receita por categoria", color="revenue", color_continuous_scale="Tealgrn", labels={"revenue": "Receita (R$)", "category": "Categoria"})
        fig.update_layout(height=460, margin=dict(l=10, r=10, t=55, b=10), yaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        payment_mix = filtered.groupby("payment_type", as_index=False).agg(value=("payment_value", "sum"))
        payment_limit_max = max(1, len(payment_mix))
        payment_limit = st.slider("Formas de pagamento exibidas", 1, payment_limit_max, payment_limit_max, key="revenue_payment_limit")
        payment_mix = payment_mix.nlargest(payment_limit, "value")
        payment_mix["payment_label"] = traduzir_serie(payment_mix["payment_type"], PAYMENT_LABELS)
        fig = px.funnel(payment_mix.sort_values("value", ascending=False), x="value", y="payment_label", title="Arquitetura de pagamento", labels={"value": "Valor pago (R$)", "payment_label": "Forma de pagamento"})
        fig.update_layout(height=460, margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(traduzir_tabela(category_revenue.assign(ticket_medio=category_revenue["revenue"] / category_revenue["orders"])), use_container_width=True, hide_index=True)

with customer_tab:
    st.subheader("Clientes e valor percebido")
    customer_value = filtered.groupby("customer_state", as_index=False).agg(
        revenue=("payment_value", "sum"), customers=("customer_unique_id", "nunique"), orders=("order_id", "nunique"), review=("review_score", "mean")
    )
    customer_value["revenue_per_customer"] = customer_value["revenue"] / customer_value["customers"].clip(lower=1)
    state_limit_max = max(1, len(customer_value))
    state_limit = st.slider("Estados exibidos", 1, state_limit_max, min(top_n, state_limit_max), key="customer_state_limit")
    customer_value = customer_value.nlargest(state_limit, "revenue")
    left, right = st.columns(2)
    with left:
        customer_plot = customer_value.copy()
        customer_plot["state_label"] = traduzir_serie(customer_plot["customer_state"], STATE_LABELS)
        fig = px.scatter(customer_plot, x="customers", y="revenue_per_customer", size="revenue", color="review", hover_name="state_label", title="Valor por cliente e escala", color_continuous_scale="Viridis", labels={"customers": "Clientes", "revenue_per_customer": "Receita por cliente (R$)", "revenue": "Receita (R$)", "review": "Nota média"})
        fig.update_layout(height=430, margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        review_floor = st.slider("Nota minima exibida", 1, 5, 1, key="customer_review_floor")
        review = filtered[filtered["review_score"] >= review_floor].groupby("review_score", as_index=False).size()
        fig = px.bar(review, x="review_score", y="size", title="Distribuição de avaliações", color="size", color_continuous_scale="Sunset", labels={"review_score": "Nota da avaliação", "size": "Quantidade de avaliações"})
        fig.update_layout(height=430, margin=dict(l=10, r=10, t=55, b=10), xaxis_title="Nota da avaliação")
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(traduzir_tabela(customer_value.sort_values("revenue", ascending=False)), use_container_width=True, hide_index=True)

with operations_tab:
    st.subheader("Operacoes e experiencia de entrega")
    operations = filtered.dropna(subset=["delivery_days"]).groupby("month", as_index=False).agg(
        delivery_days=("delivery_days", "median"), delay_days=("delay_days", "median"), late_rate=("is_late", "mean")
    )
    operations["late_rate"] *= 100
    operations_window_max = max(1, len(operations))
    operations_window = st.slider("Meses de operacao exibidos", 1, operations_window_max, min(12, operations_window_max), key="operations_month_limit")
    operations = operations.tail(operations_window)
    left, right = st.columns(2)
    with left:
        fig = px.line(operations, x="month", y=["delivery_days", "delay_days"], markers=True, title="Prazo de entrega e atraso", color_discrete_sequence=["#5de1c7", "#f0bb63"], labels={"month": "Mês", "delivery_days": "Prazo de entrega (dias)", "delay_days": "Atraso (dias)"})
        fig.update_layout(height=430, margin=dict(l=10, r=10, t=55, b=10), yaxis_title="Dias")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        carrier = filtered.groupby("order_status", as_index=False).agg(orders=("order_id", "nunique"), avg_review=("review_score", "mean"))
        carrier_limit_max = max(1, len(carrier))
        carrier_limit = st.slider("Status operacionais exibidos", 1, carrier_limit_max, carrier_limit_max, key="operations_status_limit")
        carrier = carrier.nlargest(carrier_limit, "orders")
        carrier["status_label"] = traduzir_serie(carrier["order_status"], STATUS_LABELS)
        fig = px.bar(carrier, x="status_label", y="orders", title="Volume por status", color="avg_review", color_continuous_scale="RdYlGn", labels={"status_label": "Status do pedido", "orders": "Pedidos", "avg_review": "Nota média"})
        fig.update_layout(height=430, margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(traduzir_tabela(operations), use_container_width=True, hide_index=True)

with geo_tab:
    st.subheader("Onde a operacao ganha escala")
    state_summary = filtered.groupby("customer_state", as_index=False).agg(revenue=("payment_value", "sum"), orders=("order_id", "nunique"), late_rate=("is_late", "mean"))
    state_summary["late_rate"] *= 100
    geo_state_count = max(1, len(state_summary))
    geo_state_limit = st.slider("Estados no ranking", 1, min(27, geo_state_count), min(top_n, geo_state_count), key="geo_state_limit")
    state_summary["state_label"] = traduzir_serie(state_summary["customer_state"], STATE_LABELS)
    fig = px.bar(state_summary.nlargest(geo_state_limit, "revenue").sort_values("revenue"), x="revenue", y="state_label", orientation="h", color="late_rate", title="Receita por estado com atraso em destaque", color_continuous_scale="RdYlGn_r", labels={"revenue": "Receita (R$)", "state_label": "Estado", "late_rate": "Taxa de atraso"})
    fig.update_layout(height=430, margin=dict(l=10, r=10, t=55, b=10), yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
    map_data = filtered.dropna(subset=["customer_zip_code_prefix"]).copy()
    map_points = st.slider("Pontos no mapa", 1000, 12000, 5000, step=1000, key="geo_map_points")
    map_height = st.slider("Altura do mapa", 500, 800, 640, step=20, key="geo_map_height")
    if len(map_data) > map_points:
        map_data = map_data.sample(map_points, random_state=7)
    map_data = map_data.merge(carregar_geografia(), left_on="customer_zip_code_prefix", right_on="geolocation_zip_code_prefix", how="inner")
    if not map_data.empty:
        fig = px.scatter_map(
            map_data,
            lat="lat",
            lon="lon",
            size="payment_value",
            color="customer_state",
            hover_name="customer_city",
            zoom=3.3,
            center={"lat": -14.2, "lon": -51.9},
            height=map_height,
            map_style="carto-darkmatter",
            title="Origem geográfica dos pedidos",
            labels={"customer_state": "Estado", "customer_city": "Cidade"},
        )
        fig.update_layout(margin=dict(l=0, r=0, t=48, b=0), autosize=True)
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"responsive": True, "displaylogo": False, "scrollZoom": True},
        )

with ai_tab:
    st.subheader("Generative BI")
    st.write("Descreva a decisao que voce quer investigar. A IA transforma a pergunta em uma visualizacao usando apenas o modelo Olist carregado.")
    st.caption("Exemplos: 'Quais estados combinam maior receita e pior experiencia?' · 'Mostre a tendencia mensal de receita por categoria' · 'Compare o ticket medio por tipo de pagamento'.")
    st.info("A IA interpreta sua pergunta e cria um plano estruturado. O Python aplica os filtros e calcula o resultado diretamente sobre os dados Olist; a IA não executa código nem inventa linhas.")
    with st.expander("Ver fontes e métricas disponíveis"):
        catalog_table = pd.DataFrame(
            [{"Tabela": table, "Conteúdo": description} for table, description in DATASET_CATALOG.items()]
        )
        st.dataframe(catalog_table, use_container_width=True, hide_index=True)
        st.caption("O modelo semântico consolida essas fontes na granularidade de pedido e deriva receita, ticket, prazo, atraso, avaliação, clientes, estados e categorias.")
    ai_limit = st.slider("Categorias ou cidades exibidas pela IA", 3, 30, 10, key="ai_chart_limit")

    question = st.chat_input("Pergunte algo sobre receita, clientes ou operacoes...")
    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Convertendo sua pergunta em uma visao executiva..."):
                specification, error = responder_ia(question, filtered)
            if error:
                st.warning(error)
            else:
                try:
                    specification["limit"] = ai_limit
                    st.plotly_chart(gerar_grafico_ia(filtered, specification), use_container_width=True)
                    st.markdown(f'**Leitura da IA:** {specification.get("insight", "Visualizacao pronta para exploracao.")}')
                    with st.expander("Ver especificacao gerada"):
                        st.json(specification)
                except Exception as error:
                    st.error(f"A IA respondeu, mas a visualizacao nao pode ser montada: {error}")

st.divider()
st.caption("NEXORA metrics · Generative BI pilot · Modelo construido a partir das tabelas publicas do Brazilian E-Commerce by Olist")
