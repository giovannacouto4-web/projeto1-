import streamlit as st
from groq import Groq
import pandas as pd
from PIL import Image
import json
import io
import base64

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Gerador de Legendas IA", page_icon="✦", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main-title { font-size: 2rem; font-weight: 700; margin-bottom: 0.2rem; }
    .subtitle { color: #888; font-size: 1rem; margin-bottom: 1.5rem; }
    .hashtag-pill {
        display: inline-block; background: #EEEDFE; color: #534AB7;
        font-size: 0.8rem; font-weight: 500; padding: 3px 12px;
        border-radius: 99px; margin: 3px;
    }
    .step-header {
        font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em;
        text-transform: uppercase; color: #aaa; margin-bottom: 0.5rem;
    }
    .post-preview-card {
        background: #fff; border: 1px solid #dbdbdb; border-radius: 12px;
        overflow: hidden; max-width: 400px; margin: 0 auto 1.5rem auto;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    .post-preview-header {
        display: flex; align-items: center; gap: 10px;
        padding: 10px 14px; border-bottom: 1px solid #f0f0f0;
    }
    .post-avatar { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #7F77DD, #c084fc); }
    .post-username { font-weight: 600; font-size: 0.85rem; color: #1a1a1a; }
    .post-preview-image { width: 100%; aspect-ratio: 1; object-fit: cover; display: block; }
    .post-preview-caption { padding: 12px 14px; font-size: 0.85rem; line-height: 1.5; color: #1a1a1a; border-top: 1px solid #f0f0f0; }
    .post-preview-caption b { font-weight: 600; }
    .post-preview-hashtags { padding: 0 14px 12px; font-size: 0.8rem; color: #534AB7; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ✦ Gerador de Legendas")
    st.markdown("---")
    st.markdown("**Como usar:**")
    st.markdown("1. Envie uma imagem (opcional)")
    st.markdown("2. Responda o questionário")
    st.markdown("3. Escolha quantas versões quer")
    st.markdown("4. Clique em **Gerar Legendas**")
    st.markdown("5. Copie a legenda favorita!")
    st.markdown("---")
    st.markdown("*Feito com Streamlit + Groq*")

st.markdown('<p class="main-title">✦ Gerador de Legendas</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Envie sua imagem e responda o questionário para receber legendas personalizadas com IA</p>', unsafe_allow_html=True)
st.divider()

# ── Passo 1 — Upload ──
st.markdown('<p class="step-header">Passo 1 — Imagem do post</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Envie uma imagem do seu post (opcional)",
    type=["jpg", "jpeg", "png", "webp"],
)

image_b64 = None
if uploaded_file is not None:
    image_obj = Image.open(uploaded_file)
    st.image(image_obj, caption="Imagem carregada", use_column_width=True)
    buf = io.BytesIO()
    image_obj.save(buf, format="PNG")
    image_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

st.divider()

# ── Passo 2 ──
st.markdown('<p class="step-header">Passo 2 — Sobre o post</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    objetivo = st.selectbox("Objetivo da publicação", options=[
        "Vender ou promover um produto/serviço",
        "Engajar e interagir com a audiência",
        "Educar ou informar o público",
        "Inspirar e motivar",
    ])
with col2:
    rede_social = st.selectbox("Rede social", options=["Instagram", "TikTok", "LinkedIn", "Twitter/X"])

st.divider()

# ── Passo 3 ──
st.markdown('<p class="step-header">Passo 3 — Tom e público</p>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    tom = st.selectbox("Tom desejado", options=[
        "Engraçado e descontraído", "Profissional e formal",
        "Motivacional e inspirador", "Casual e amigável",
    ])
with col4:
    publico = st.selectbox("Público-alvo", options=[
        "Jovens (18–25 anos)", "Adultos (26–40 anos)",
        "Empreendedores e profissionais", "Público geral",
    ])

contexto = st.text_area("Contexto extra (opcional)",
    placeholder="Ex: lançamento de produto, promoção de fim de semana...", height=90)

st.divider()

# ── Passo 4 — Quantidade ──
st.markdown('<p class="step-header">Passo 4 — Quantas versões de legendas?</p>', unsafe_allow_html=True)
quantidade = st.slider("Versões", min_value=1, max_value=5, value=1)
st.caption("Cada versão traz 3 legendas com estilos diferentes.")

st.divider()

# ── Funções ──
def render_post_preview(legenda_texto, hashtags, image_b64=None, username="seu_perfil"):
    hashtags_str = " ".join(hashtags) if hashtags else ""
    if image_b64:
        img_html = f'<img class="post-preview-image" src="data:image/png;base64,{image_b64}" />'
    else:
        img_html = '<div style="width:100%;aspect-ratio:1;background:linear-gradient(135deg,#EEEDFE,#c4b5fd);display:flex;align-items:center;justify-content:center;font-size:3rem;">🖼️</div>'
    st.markdown(f"""
    <div class="post-preview-card">
        <div class="post-preview-header">
            <div class="post-avatar"></div>
            <span class="post-username">{username}</span>
        </div>
        {img_html}
        <div class="post-preview-caption"><b>{username}</b> {legenda_texto}</div>
        <div class="post-preview-hashtags">{hashtags_str}</div>
    </div>
    """, unsafe_allow_html=True)


def chamar_api(objetivo, rede_social, tom, publico, contexto, image_b64, legendas_anteriores):
    import random
    seed = random.randint(100000, 999999)

    instrucao = f"\n(Seed: {seed})\n"
    if legendas_anteriores:
        textos = "\n".join(f"- {t}" for t in legendas_anteriores)
        instrucao += (
            f"\nATENÇÃO: As legendas abaixo JÁ EXISTEM. Crie legendas 100% diferentes delas:\n{textos}\n"
        )

    prompt = f"""Você é especialista em marketing digital e copywriting.

Crie 3 legendas ÚNICAS para redes sociais.

Objetivo: {objetivo}
Rede social: {rede_social}
Tom: {tom}
Público-alvo: {publico}
Contexto: {contexto}
{instrucao}

Retorne SOMENTE JSON válido.

{{
  "legendas": [
    {{"estilo": "Direto ao ponto", "texto": "Legenda aqui"}},
    {{"estilo": "Storytelling", "texto": "Legenda aqui"}},
    {{"estilo": "Engajamento", "texto": "Legenda aqui"}}
  ],
  "hashtags": ["#hashtag1","#hashtag2","#hashtag3","#hashtag4","#hashtag5","#hashtag6"]
}}"""

    if image_b64:
        content = [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
            {"type": "text", "text": prompt}
        ]
        model = "meta-llama/llama-4-scout-17b-16e-instruct"
    else:
        content = prompt
        model = "llama-3.3-70b-versatile"

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        temperature=1.0,
        max_tokens=1500,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


# ── Botão Gerar ──
if st.button("✨ Gerar Legendas", type="primary", use_container_width=True):
    todos_resultados = []
    todos_textos = []

    progress = st.progress(0, text="Iniciando...")

    for i in range(quantidade):
        progress.progress(i / quantidade, text=f"Gerando versão {i+1} de {quantidade}...")
        try:
            resultado = chamar_api(
                objetivo, rede_social, tom, publico, contexto,
                image_b64,
                todos_textos
            )
            todos_resultados.append(resultado)
            for leg in resultado.get("legendas", []):
                todos_textos.append(leg.get("texto", ""))
        except Exception as e:
            st.error(f"❌ Erro na versão {i+1}: {str(e)}")

    progress.progress(1.0, text="Concluído!")

    if todos_resultados:
        st.divider()
        st.markdown('<p class="step-header">Suas legendas</p>', unsafe_allow_html=True)

        for v, resultado in enumerate(todos_resultados):
            hashtags = resultado.get("hashtags", [])
            legendas = resultado.get("legendas", [])

            st.markdown(f"### Versão {v+1}")

            for i, leg in enumerate(legendas):
                with st.expander(f"✦ {leg['estilo']}", expanded=(v == 0)):
                    render_post_preview(leg["texto"], hashtags, image_b64)
                    legenda_completa = leg["texto"] + "\n\n" + " ".join(hashtags)
                    st.text_area(label="", value=legenda_completa, height=130, key=f"leg_{v}_{i}")
                    st.code(legenda_completa, language=None)

            if hashtags:
                pills_html = "".join(f'<span class="hashtag-pill">{h}</span>' for h in hashtags)
                st.markdown(f'<div style="margin:0.5rem 0 1rem">{pills_html}</div>', unsafe_allow_html=True)

            st.divider()

        # CSV
        todas_legendas = []
        for v, resultado in enumerate(todos_resultados):
            for leg in resultado.get("legendas", []):
                todas_legendas.append({
                    "versao": v + 1,
                    "estilo": leg.get("estilo", ""),
                    "texto": leg.get("texto", ""),
                    "rede_social": rede_social,
                    "tom": tom,
                    "objetivo": objetivo,
                })

        df = pd.DataFrame(todas_legendas)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(label="⬇️ Baixar todas como CSV", data=csv,
                           file_name="legendas_geradas.csv", mime="text/csv")

        st.divider()
        if st.button("🔄 Recomeçar", use_container_width=True):
            st.rerun()
