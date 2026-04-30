import streamlit as st
import random

st.set_page_config(page_title="Sem dúvidas!")

st.title("Sem dúvidas!")
st.text("O app funciona assim:")
st.text(" digite quantas e quais opções você está em dúvida e nós decidiremos por você")

# Entrada de opções
opcoes = st.text_input("O app funciona assim: digite quantas e quais opções você está em dúvida e nós decidiremos por você")

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


if st.session_state.historico:
    st.subheader("Histórico de escolhas")
    st.write(st.session_state.historico)
    
    if st.button("Limpar histórico"):
        st.session_state.historico = []
        st.success("Histórico limpo!")
        st.rerun()
