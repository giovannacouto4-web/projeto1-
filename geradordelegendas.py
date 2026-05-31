import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import json
import io

# ─────────────────────────────────────────────
# Configuração da página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Gerador de Legendas IA",
    page_icon="✦",
    layout="centered",
)

st.markdown("""
<style>
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #888;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .legenda-box {
        background: #f8f7ff;
        border-left: 4px solid #7F77DD;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .legenda-estilo {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #7F77DD;
        margin-bottom: 0.4rem;
    }
    .legenda-texto {
        font-size: 1rem;
        line-height: 1.6;
        color: #1a1a1a;
    }
    .hashtag-pill {
        display: inline-block;
        background: #EEEDFE;
        color: #534AB7;
        font-size: 0.8rem;
        font-weight: 500;
        padding: 3px 12px;
        border-radius: 99px;
        margin: 3px;
    }
    .step-header {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #aaa;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Sidebar — configuração da API
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Configuração")
    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="Cole sua chave aqui...",
        help="Obtenha sua chave em: https://aistudio.google.com/app/apikey"
    )
    st.markdown("---")
    st.markdown("**Como usar:**")
    st.markdown("1. Insira sua API Key do Gemini")
    st.markdown("2. Envie uma imagem (opcional)")
    st.markdown("3. Responda o quiz")
    st.markdown("4. Clique em **Gerar Legendas**")
    st.markdown("---")
    st.markdown("*Feito com Streamlit + Google Gemini*")


# ─────────────────────────────────────────────
# Título
# ─────────────────────────────────────────────
st.markdown('<p class="main-title">✦ Gerador de Legendas</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Envie sua imagem e responda o quiz para receber legendas personalizadas com IA</p>', unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────
# Passo 1 — Upload de imagem
# ─────────────────────────────────────────────
st.markdown('<p class="step-header">Passo 1 — Imagem do post</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Envie uma imagem do seu post (opcional)",
    type=["jpg", "jpeg", "png", "webp"],
    help="A IA irá analisar a imagem para gerar legendas mais contextuais"
)

image_obj = None
if uploaded_file:
    image_obj = Image.open(uploaded_file)
    st.image(image_obj, caption="Imagem carregada", use_column_width=True)

st.divider()


# ─────────────────────────────────────────────
# Passo 2 — Quiz
# ─────────────────────────────────────────────
st.markdown('<p class="step-header">Passo 2 — Sobre o post</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    objetivo = st.selectbox(
        "Objetivo da publicação",
        options=[
            "Vender ou promover um produto/serviço",
            "Engajar e interagir com a audiência",
            "Educar ou informar o público",
            "Inspirar e motivar",
        ]
    )

with col2:
    rede_social = st.selectbox(
        "Rede social",
        options=["Instagram", "TikTok", "LinkedIn", "Twitter/X"]
    )

st.divider()


# ─────────────────────────────────────────────
# Passo 3 — Tom e público
# ─────────────────────────────────────────────
st.markdown('<p class="step-header">Passo 3 — Tom e público</p>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    tom = st.selectbox(
        "Tom desejado",
        options=[
            "Engraçado e descontraído",
            "Profissional e formal",
            "Motivacional e inspirador",
            "Casual e amigável",
        ]
    )

with col4:
    publico = st.selectbox(
        "Público-alvo",
        options=[
            "Jovens (18–25 anos)",
            "Adultos (26–40 anos)",
            "Empreendedores e profissionais",
            "Público geral",
        ]
    )

contexto = st.text_area(
    "💬 Contexto extra (opcional)",
    placeholder="Ex: lançamento de produto, promoção de fim de semana, dia do cliente...",
    height=90,
)

st.divider()


# ─────────────────────────────────────────────
# Função principal — gerar legendas
# ─────────────────────────────────────────────
def gerar_legendas(api_key, objetivo, rede_social, tom, publico, contexto, image_obj):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""Você é um especialista em marketing digital e redes sociais.
Com base nas informações abaixo{' e na imagem fornecida' if image_obj else ''}, gere 3 legendas criativas e personalizadas para um post.

Objetivo: {objetivo}
Rede social: {rede_social}
Tom: {tom}
Público-alvo: {publico}
{f'Contexto adicional: {contexto}' if contexto.strip() else ''}

Responda APENAS em JSON válido, sem markdown, sem explicações extras. Formato exato:
{{
  "legendas": [
    {{ "estilo": "Nome do estilo (ex: Direto ao ponto)", "texto": "Texto da legenda" }},
    {{ "estilo": "Nome do estilo (ex: Storytelling)", "texto": "Texto da legenda" }},
    {{ "estilo": "Nome do estilo (ex: Com chamada para ação)", "texto": "Texto da legenda" }}
  ],
  "hashtags": ["#exemplo1", "#exemplo2", "#exemplo3", "#exemplo4", "#exemplo5", "#exemplo6"]
}}"""

    if image_obj:
        response = model.generate_content([prompt, image_obj])
    else:
        response = model.generate_content(prompt)

    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


# ─────────────────────────────────────────────
# Botão gerar + exibição dos resultados
# ─────────────────────────────────────────────
if st.button("✨ Gerar Legendas", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Insira sua Google Gemini API Key na barra lateral para continuar.")
    else:
        with st.spinner("Gerando suas legendas com IA..."):
            try:
                resultado = gerar_legendas(
                    api_key, objetivo, rede_social, tom, publico, contexto, image_obj
                )

                st.divider()
                st.markdown('<p class="step-header">Passo 4 — Suas legendas</p>', unsafe_allow_html=True)

                # Exibir legendas
                for leg in resultado.get("legendas", []):
                    st.markdown(f"""
                    <div class="legenda-box">
                        <div class="legenda-estilo">{leg['estilo']}</div>
                        <div class="legenda-texto">{leg['texto']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.code(leg["texto"], language=None)

                # Exibir hashtags
                hashtags = resultado.get("hashtags", [])
                if hashtags:
                    st.markdown("**#️⃣ Hashtags sugeridas**")
                    pills_html = "".join(
                        f'<span class="hashtag-pill">{h}</span>' for h in hashtags
                    )
                    st.markdown(f'<div style="margin:0.5rem 0 1rem">{pills_html}</div>', unsafe_allow_html=True)

                    hashtags_text = " ".join(hashtags)
                    st.code(hashtags_text, language=None)

                # Salvar histórico em DataFrame (Pandas)
                st.divider()
                st.markdown("**📊 Histórico desta geração**")
                df = pd.DataFrame(resultado.get("legendas", []))
                df.insert(0, "Rede Social", rede_social)
                df.insert(1, "Tom", tom)
                df.insert(2, "Objetivo", objetivo)
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Baixar como CSV",
                    data=csv,
                    file_name="legendas_geradas.csv",
                    mime="text/csv",
                )

            except json.JSONDecodeError:
                st.error("❌ Erro ao interpretar a resposta da IA. Tente novamente.")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")

