import streamlit as st
import pandas as pd
from google import genai
from dotenv import load_dotenv
import os

# =====================================
# CONFIGURAÇÕES INICIAIS
# =====================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

st.set_page_config(
    page_title="EdF-AI",
    page_icon="💰",
    layout="wide"
)

# =====================================
# PERSONALIDADE DO ASSISTENTE
# =====================================

PERSONALIDADE = """
Você é o FinCoach AI.

Características:

- Especialista em educação financeira.
- Linguagem amigável, calma e seria.
- Nunca critica ou constrange o usuário.
- Explica conceitos financeiros de forma simples.
- Dá exemplos práticos.
- Incentiva organização financeira.
- Incentiva reserva de emergência.
- Incentiva investimentos responsáveis.
- Sempre responde em português do Brasil.

Seu objetivo é ajudar pessoas comuns a desenvolver hábitos financeiros saudáveis, e conscientizar as pessoas.

Ao responder:

- Seja acolhedor.
- Seja serio e profissional.
- Seja objetivo.
- Use exemplos quando necessário.
- Não utilize emojis.
"""

# =====================================
# HISTÓRICO DE CONVERSA
# =====================================

if "historico" not in st.session_state:
    st.session_state.historico = []

# =====================================
# CABEÇALHO
# =====================================

st.title("FinCoach AI")

st.subheader(
    "Seu Assistente Financeiro Inteligente."
)

st.markdown("""
Informe sua renda, seus gastos e converse com o FinCoach AI
para receber orientações financeiras personalizadas.
""")

st.divider()

# =====================================
# META FINANCEIRA
# =====================================

meta = st.text_input(
    "Qual é sua meta financeira?",
    placeholder="Ex: Comprar um carro, criar reserva de emergência, viajar..."
)

# =====================================
# ENTRADAS FINANCEIRAS
# =====================================

col1, col2 = st.columns(2)

with col1:
    salario = st.number_input(
        "Renda Mensal (R$)",
        min_value=0.0,
        step=100.0
    )

with col2:
    aluguel = st.number_input(
        "Aluguel",
        min_value=0.0,
        step=50.0
    )

mercado = st.number_input(
    "Mercado",
    min_value=0.0,
    step=50.0
)

transporte = st.number_input(
    "Transporte",
    min_value=0.0,
    step=50.0
)

lazer = st.number_input(
    "Lazer",
    min_value=0.0,
    step=50.0
)

outros = st.number_input(
    "Outros Gastos",
    min_value=0.0,
    step=50.0
)

# =====================================
# CÁLCULOS
# =====================================

gastos = (
    aluguel +
    mercado +
    transporte +
    lazer +
    outros
)

saldo = salario - gastos

if salario > 0:
    percentual_gastos = (gastos / salario) * 100
else:
    percentual_gastos = 0

# =====================================
# MÉTRICAS
# =====================================

st.divider()

m1, m2, m3 = st.columns(3)

m1.metric(
    "**Renda",
    f"R$ {salario:,.2f}"
)

m2.metric(
    "**Gastos",
    f"R$ {gastos:,.2f}"
)

m3.metric(
    "**Saldo",
    f"R$ {saldo:,.2f}"
)

# =====================================
# GRÁFICO
# =====================================

dados = pd.DataFrame({
    "Categoria": [
        "Aluguel",
        "Mercado",
        "Transporte",
        "Lazer",
        "Outros"
    ],
    "Valor": [
        aluguel,
        mercado,
        transporte,
        lazer,
        outros
    ]
})

st.subheader("Distribuição dos Gastos")

st.bar_chart(
    dados.set_index("Categoria")
)

# =====================================
# ANÁLISE FINANCEIRA
# =====================================

st.divider()

if st.button("Gerar Diagnóstico Financeiro"):

    if salario <= 0:

        st.error("Informe uma renda válida.")

    else:

        with st.spinner("Analisando suas finanças..."):

            prompt = f"""
{PERSONALIDADE}

Dados financeiros do usuário:

Meta Financeira:
{meta}

Renda:
R$ {salario:.2f}

Gastos:

Aluguel: R$ {aluguel:.2f}
Mercado: R$ {mercado:.2f}
Transporte: R$ {transporte:.2f}
Lazer: R$ {lazer:.2f}
Outros: R$ {outros:.2f}

Total gasto:
R$ {gastos:.2f}

Saldo:
R$ {saldo:.2f}

Percentual comprometido:
{percentual_gastos:.2f}%

Gere:

1. Diagnóstico financeiro.
2. Pontos positivos.
3. Pontos de atenção.
4. Sugestões de economia.
5. Plano de ação para 3 meses.
6. Score financeiro de 0 a 100.
7. Recomendações alinhadas à meta financeira.
8. Conclusão motivadora.
"""

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.success(
                    "Diagnóstico concluído!"
                )

                st.markdown("## Resultado")

                st.markdown(response.text)

            except Exception as erro:

                st.error(
                    f"Erro ao acessar IA: {erro}"
                )

# =====================================
# CHAT COM A IA
# =====================================

st.divider()

st.subheader("Converse com o FinCoach AI")

pergunta_usuario = st.text_area(
    "Faça uma pergunta sobre finanças",
    placeholder="Ex: Como posso economizar R$500 por mês?"
)

if st.button("Enviar Pergunta"):

    if pergunta_usuario.strip() == "":

        st.warning(
            "Digite uma pergunta."
        )

    else:

        with st.spinner(
            "FinCoach está pensando..."
        ):

            prompt_chat = f"""
{PERSONALIDADE}

Contexto financeiro do usuário:

Meta:
{meta}

Renda:
R$ {salario:.2f}

Gastos:
R$ {gastos:.2f}

Saldo:
R$ {saldo:.2f}

Pergunta:

{pergunta_usuario}
"""

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_chat
                )

                resposta_ia = response.text

                st.session_state.historico.append(
                    ("Você", pergunta_usuario)
                )

                st.session_state.historico.append(
                    ("FinCoach AI", resposta_ia)
                )

            except Exception as erro:

                st.error(
                    f"Erro ao acessar IA: {erro}"
                )

# =====================================
# HISTÓRICO
# =====================================

if st.session_state.historico:

    st.divider()

    st.subheader("Histórico da Conversa")

    for autor, mensagem in st.session_state.historico:

        if "Você" in autor:

            st.markdown(
                f"**{autor}:** {mensagem}"
            )

        else:

            st.info(
                f"{autor}: {mensagem}"
            )

# =====================================
# RODAPÉ
# =====================================

st.divider()

st.caption(
    "EdF-A.I • Projeto Acadêmico de Inteligência Artificial com Streamlit e Google Gemini"
)