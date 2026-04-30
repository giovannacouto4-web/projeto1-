import streamlit as st
import random

st.set_page_config(page_title="Sem dúvidas!")

st.title("Sem dúvidas!")
st.write("É muito simples de usar!")
st.write("Apenas digite opções separadas por vírgula e nós decidiremos por você!")

# Entrada
opcoes = st.text_input("Digite aqui:")

# Estados
if "historico" not in st.session_state:
    st.session_state.historico = []

if "ultima_escolha" not in st.session_state:
    st.session_state.ultima_escolha = None

if "modo" not in st.session_state:
    st.session_state.modo = "inicio"

# Função escolher
def escolher():
    lista = [op.strip() for op in opcoes.split(",") if op.strip()]
    if lista:
        escolha = random.choice(lista)
        st.session_state.ultima_escolha = escolha
        st.session_state.historico.append(escolha)
        st.session_state.modo = "resultado"
    else:
        st.warning("Digite pelo menos uma opção!")

# BOTÃO INICIAL
if st.session_state.modo == "inicio":
    if st.button("Decidir"):
        escolher()
        st.rerun()

# RESULTADO (AGORA SEMPRE VEM PRIMEIRO)
if st.session_state.modo == "resultado":
    st.success(f"Escolha: {st.session_state.ultima_escolha}")

    resposta = st.radio(
        "Gostou da escolha?",
        ["Sim", "Não"],
        index=None
    )

    if resposta == "Sim":
        st.success("Boa! 😄")

    elif resposta == "Não":
        st.warning("Vamos tentar outra então!")

        if st.button("Tentar novamente"):
            escolher()
            st.rerun()

# HISTÓRICO (SEMPRE DEPOIS DO RESULTADO)
if st.session_state.historico:
    st.subheader("Histórico")
    st.write(st.session_state.historico)

    if st.button("Limpar histórico"):
        st.session_state.historico = []
        st.rerun()
