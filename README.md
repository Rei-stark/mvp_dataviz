# NEXORA metrics | C-Level Analytics | Generative BI

Piloto de uma plataforma de analytics executivo para transformar as tabelas publicas do Brazilian E-Commerce by Olist em decisoes de negocio. O projeto combina uma camada semantica de pedidos, dashboards setorizados e uma interface de Generative BI para solicitar novas visualizacoes em linguagem natural.

## O que existe no MVP

- **Executive Pulse:** receita mensal, mix de status e sinais executivos.
- **Receita & Mix:** receita por categoria, ticket medio e arquitetura de pagamentos.
- **Clientes:** valor por cliente, escala por estado e distribuicao de reviews.
- **Operacoes:** tempo de entrega, atraso, status e experiencia.
- **Geografia:** concentracao por estado e mapa de origem dos pedidos.
- **Generative BI:** pergunta em linguagem natural convertida pela OpenAI em uma especificacao de grafico validada contra o modelo carregado.
- Filtros globais por periodo, estado, status, categoria e Top N.

### Como a IA analisa os dados

A Generative BI conhece o catalogo das tabelas Olist e o modelo semantico consolidado. Ela transforma a pergunta em um plano seguro com dimensao, detalhamento, metrica, agregacao e filtros; o Python executa esse plano sobre os dados reais antes de renderizar o grafico. As tabelas completas nao sao enviadas para a API e a IA nao executa codigo.

Ela suporta tendencias por categoria, comparacoes por estado ou cidade, receita, GMV, frete, ticket, contagem de pedidos, clientes, notas, prazo de entrega e percentual de atraso, com graficos de barras, linhas, areas, dispersao e pizza.

## Executar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run mvp_dataviz.py
```

A aplicacao carrega automaticamente as tabelas existentes em `datasets/`.

## Ativar a Generative BI

Nunca coloque a chave no codigo ou no Git. Para uso local, defina a variavel de ambiente:

```powershell
$env:OPENAI_API_KEY = "sua-chave"
streamlit run mvp_dataviz.py
```

Ou crie `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sua-chave"
```

O arquivo de secrets e ignorado pelo Git. Sem a chave, o dashboard continua funcionando em modo demonstracao.

## Dados e modelo

O app combina pedidos, clientes, itens, pagamentos, reviews, produtos, categorias traduzidas e geolocalizacao. O modelo final fica na granularidade de pedido e deriva GMV, frete, ticket, dias de entrega, atraso, review medio, mes, categoria dominante e estado do cliente.

## Estrutura

```text
mvp_dataviz/
|-- datasets/                  # CSVs publicos da Olist
|-- mvp_dataviz.py             # app, modelo semantico e copiloto
|-- requirements.txt
|-- README.md
`-- .gitignore
```