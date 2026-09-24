# NEXORA metrics | C-Level Analytics | Generative BI

Piloto de uma plataforma de analytics executivo para transformar as tabelas publicas do Brazilian E-commerce em decisoes de negocio. O projeto combina uma camada semantica de pedidos, dashboards setorizados e uma interface de Generative BI para solicitar novas visualizacoes em linguagem natural.

**Periodo dos dados:** 04/09/2016 a 17/10/2018.

## O que existe no MVP

- **Executive Pulse:** receita mensal, mix de status e sinais executivos.
- **Receita & Mix:** receita por categoria, ticket medio e arquitetura de pagamentos.
- **Clientes:** valor por cliente, escala por estado e distribuicao de reviews.
- **Operacoes:** tempo de entrega, atraso, status e experiencia.
- **Geografia:** concentracao por estado e mapa de origem dos pedidos.
- **Previsões ML:** projeção mensal de receita, pedidos, clientes, prazo de entrega e avaliações, com horizonte ajustável e erro MAE.
- **Generative BI:** pergunta em linguagem natural convertida pela OpenAI em uma especificacao de grafico validada contra o modelo carregado.
- Filtros globais por periodo, estado, status, categoria e Top N.

### Como a IA analisa os dados

A Generative BI conhece o catalogo das tabelas do Brazilian E-commerce e o modelo semantico consolidado. Ela transforma a pergunta em um plano seguro com dimensao, detalhamento, metrica, agregacao e filtros; o Python executa esse plano sobre os dados reais antes de renderizar o grafico. As tabelas completas nao sao enviadas para a API e a IA nao executa codigo.

Ela suporta tendencias por categoria, comparacoes por estado ou cidade, receita, GMV, frete, ticket, contagem de pedidos, clientes, notas, prazo de entrega e percentual de atraso, com graficos de barras, linhas, areas, dispersao e pizza.

### Motor de previsão

O módulo de previsões usa regressão Ridge regularizada com tendência temporal e sazonalidade mensal. A aba **Previsões ML** permite selecionar a métrica, o recorte (total, estado ou categoria) e o horizonte; o **Pulso executivo** também oferece a opção de sobrepor a previsão de receita ao gráfico mensal. O MAE é calculado em uma janela temporal de validação antes do cenário futuro ser exibido.

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

O arquivo `.streamlit/secrets.toml.example` é apenas um modelo e não é carregado pelo Streamlit. Crie o arquivo real `secrets.toml` ou defina a variável no mesmo terminal que inicia a aplicação:

```powershell
$env:OPENAI_API_KEY = "sua-chave"
python -m streamlit run mvp_dataviz.py
```

O arquivo de secrets e ignorado pelo Git. Sem a chave, o dashboard continua funcionando em modo local, mas não faz chamadas à OpenAI.

## Dados e modelo

O app combina pedidos, clientes, itens, pagamentos, reviews, produtos, categorias traduzidas e geolocalizacao do Brazilian E-commerce. O modelo final fica na granularidade de pedido e deriva GMV, frete, ticket, dias de entrega, atraso, review medio, mes, categoria dominante e estado do cliente.

## Estrutura

```text
mvp_dataviz/
|-- datasets/                  # CSVs publicos do Brazilian E-commerce
|-- mvp_dataviz.py             # app, modelo semantico e copiloto
|-- requirements.txt
|-- README.md
`-- .gitignore
```