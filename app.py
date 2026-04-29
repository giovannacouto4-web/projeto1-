import streamlit as st
from anthropic import Anthropic
 
st.set_page_config(page_title="Guia de Viagem ✈️", page_icon="✈️", layout="centered")
 
st.title("✈️ Guia de Viagem")
st.caption("Digite um país e receba as melhores dicas de viagem")
 
client = Anthropic()
 
pais = st.text_input("🌍 Para onde você quer ir?", placeholder="Ex: Japão, Portugal, Peru...")
 
if st.button("Buscar dicas", use_container_width=True, type="primary"):
    if not pais.strip():
        st.warning("Digite o nome de um país primeiro!")
    else:
        with st.spinner(f"Pesquisando dicas para {pais}..."):
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Me dê um guia rápido de viagem para {pais} com estas seções:
 
🏆 Por que visitar (3 razões)
📅 Melhor época para ir
📍 Top 3 destinos imperdíveis
🍽️ Pratos típicos que precisa provar
💡 Dica de ouro do viajante
 
Seja direto, animado e útil. Use emojis. Responda em português."""
                    }
                ]
            )
            st.markdown(response.content[0].text)
