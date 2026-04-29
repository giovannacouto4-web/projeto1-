import streamlit as st
import random

st.set_page_config(page_title="IndecisApp")

st.title("IndecisApp - Deixe o app decidir por você!")

# Entrada de opções
opcoes = st.text_input("Digite opções separadas por vírgula:")

if "historico" not in st.session_state:
    st.session_state.historico = []

if st.button("Decidir"):
    lista = [op.strip() for op in opcoes.split(",") if op.strip() != ""]
    
    if lista:
        escolha = random.choice(lista)
        st.success(f"Escolha: {escolha}")
        
        st.session_state.historico.append(escolha)
    else:
        st.warning("Digite pelo menos uma opção!")


