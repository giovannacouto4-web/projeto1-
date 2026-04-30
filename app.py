import streamlit as st
import random

st.set_page_config(page_title="Sem dúvidas!")

st.title("Sem dúvidas!")
st.text("É muito simples de usar!")
st.text("Apenas digite quantas e quais opções você está em dúvida e nós decidiremos por você!")

# Entrada de opções
opcoes = st.text_input("Digite aqui:")

# Estados
if "historico" not in st.session_state:
    st.session_state.historico = []

if "ultima_escolha" not in st.session_state:
    st.session_state.ultima_escolha = None

# Botão decidir
if st.button("Decidir"):
    lista = [op.strip() for op in opcoes.split(",") if op.strip() != ""]
    
    if lista:
        escolha = random.choice(lista)
        
        st.session_state.ultima_escolha = escolha
        st.session_state.historico.append(escolha)

    else:
        st.warning("Digite pelo menos uma opção!")

# Mostrar resultado + feedback
if st.session_state.ultima_escolha:
    st.success(f"Escolha: {st.session_state.ultima_escolha}")

    st.write("Gostou da sua escolha?")

    resposta = st.radio(
        "Selecione uma opção:",
        ["Sim", "Não"],
        index=None,
        key="radio_feedback"
    )

    if resposta == "Sim":
        st.success("Que bom!")
    elif resposta == "Não":
        st.info("Tente novamente, na próxima pode ser que seja melhor!")
  
# Histórico
if st.session_state.historico:
    st.subheader("Histórico de escolhas")
    st.write(st.session_state.historico)
    
    if st.button("Limpar histórico"):
        st.session_state.historico = []
        st.success("Histórico limpo!")
        st.rerun()
