import streamlit as st
from groq import Groq

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Sem dúvidas!")

# TÍTULO
st.title("Sem dúvidas!")

st.write(
    "Digite opções separadas por vírgula e a IA escolherá por você!"
)

# INPUT
opcoes = st.text_input(
    "Digite aqui:",
    placeholder="Ex: Pizza, Hambúrguer, Sushi"
)

# SESSION STATE
if "historico" not in st.session_state:
    st.session_state.historico = []

if "ultima_escolha" not in st.session_state:
    st.session_state.ultima_escolha = None

if "modo" not in st.session_state:
    st.session_state.modo = "inicio"


# FUNÇÃO IA
def escolher_com_ia():

    lista = [op.strip() for op in opcoes.split(",") if op.strip()]

    if not lista:
        st.warning("Digite pelo menos uma opção!")
        return

    prompt = f"""
Escolha apenas UMA opção dessa lista:

{lista}

Responda SOMENTE com a opção escolhida.
"""

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=100,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        escolha = resposta.choices[0].message.content.strip()

        st.session_state.ultima_escolha = escolha
        st.session_state.historico.append(escolha)
        st.session_state.modo = "resultado"

    except Exception as e:
        st.error(f"Erro: {e}")


# BOTÃO
if st.session_state.modo == "inicio":

    if st.button("Decidir"):
        escolher_com_ia()


# RESULTADO
if st.session_state.modo == "resultado":

    st.success(f"Escolha: {st.session_state.ultima_escolha}")

    resposta_usuario = st.radio(
        "Gostou da escolha?",
        ["Sim", "Não"],
        index=None
    )

    if resposta_usuario == "Sim":
        st.success("Que bom!")

    elif resposta_usuario == "Não":

        if st.button("Tentar novamente"):
            escolher_com_ia()
            st.rerun()


# HISTÓRICO
if st.session_state.historico:

    st.subheader("Histórico")

    st.write(st.session_state.historico)

    if st.button("Limpar histórico"):
        st.session_state.historico = []
        st.rerun()
