import streamlit as st
from google import genai
import os


st.set_page_config(page_title="Sem dúvidas!")


segredo = st.secrets["GEMINI_API_KEY"]
os.environ["GOOGLE_API_KEY"] = segredo

client = genai.Client()

MODEL_ID = "gemini-2.5-flash"

# TÍTULO
st.title("Sem dúvidas!")
st.write("É muito simples de usar!")
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


# FUNÇÃO COM IA
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

    resposta = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )

    escolha = resposta.text.strip()

    st.session_state.ultima_escolha = escolha
    st.session_state.historico.append(escolha)
    st.session_state.modo = "resultado"


# BOTÃO INICIAL
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

        st.warning("Quer tentar de novo?")

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
