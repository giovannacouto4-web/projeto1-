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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(180deg, #E8F4FB 0%, #F0F8FD 40%, #FFFFFF 100%);
    }

    /* ── Header ── */
    .app-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0 0 0.5rem 0;
        margin-bottom: 0.25rem;
    }
    .app-logo {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #7BBDE8, #4A90D9);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem; color: white; font-weight: 800;
        flex-shrink: 0;
    }
    .app-header-text { line-height: 1.2; }
    .app-header-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1rem; font-weight: 700; color: #1E2733; margin: 0;
    }
    .app-header-sub { font-size: 0.78rem; color: #6B7E8F; margin: 0; }

    /* ── Hero ── */
    .hero-section { margin: 0.5rem 0 1.2rem 0; }
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.75rem; font-weight: 800;
        color: #1E2733; line-height: 1.25; margin-bottom: 0.5rem;
    }
    .hero-title .highlight { color: #4A90D9; }
    .hero-subtitle { color: #6B7E8F; font-size: 0.92rem; line-height: 1.55; margin-bottom: 0; }

    /* ── Step cards ── */
    .step-card {
        background: #FFFFFF;
        border: 1.5px solid #BDD9F2;
        border-radius: 18px;
        padding: 1.2rem 1.4rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(74, 144, 217, 0.08);
    }
    .step-label {
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 1rem;
    }
    .step-number {
        width: 30px; height: 30px;
        background: linear-gradient(135deg, #7BBDE8, #4A90D9);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.82rem; font-weight: 700; color: white;
        flex-shrink: 0;
    }
    .step-title {
        font-family: 'Poppins', sans-serif;
        font-size: 0.95rem; font-weight: 700; color: #1E2733;
        margin: 0; line-height: 1.2;
    }
    .step-desc { font-size: 0.8rem; color: #7A94A8; margin: 2px 0 0 0; }

    /* ── Upload zone ── */
    section[data-testid="stFileUploaderDropzone"] {
        background: #F0F8FD !important;
        border: 2px dashed #7BBDE8 !important;
        border-radius: 16px !important;
    }

    /* ── Selectboxes ── */
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border-color: #BDD9F2 !important;
        background: #F7FBFE !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #4A90D9 !important;
    }
    textarea {
        border-radius: 12px !important;
        border-color: #BDD9F2 !important;
        background: #F7FBFE !important;
    }
    textarea:focus { border-color: #4A90D9 !important; }

    /* ── Slider ── */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #4A90D9 !important;
    }
    div[data-testid="stSlider"] div[data-testid="stSliderThumb"] {
        background-color: #4A90D9 !important;
    }
    div[data-testid="stSlider"] > div > div > div {
        background-color: #4A90D9 !important;
    }

    /* ── Botão Gerar (primário) ── */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7BBDE8, #4A90D9) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.65rem 0 !important;
        box-shadow: 0 4px 14px rgba(74, 144, 217, 0.38) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 18px rgba(74, 144, 217, 0.48) !important;
        transform: translateY(-1px);
    }

    /* ── Botão secundário ── */
    div.stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #4A90D9 !important;
        border: 1.5px solid #7BBDE8 !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: #EEF7FD !important;
        border-color: #4A90D9 !important;
    }

    /* ── Botão download ── */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #7BBDE8, #4A90D9) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(74, 144, 217, 0.35) !important;
    }

    /* ── Expander ── */
    div[data-testid="stExpander"] {
        border: 1.5px solid #BDD9F2 !important;
        border-radius: 16px !important;
        background: #FFFFFF;
        box-shadow: 0 2px 10px rgba(74, 144, 217, 0.07);
    }

    /* ── Progress ── */
    div[data-testid="stProgress"] > div > div {
        background-color: #4A90D9 !important;
    }

    /* ── Resultado cards ── */
    .result-number {
        display: inline-flex; align-items: center; justify-content: center;
        width: 36px; height: 36px; border-radius: 10px;
        background: linear-gradient(135deg, #7BBDE8, #4A90D9);
        color: white; font-weight: 700; font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    .hashtag-pill {
        display: inline-block; background: #E4F2FB; color: #2E6CA8;
        font-size: 0.78rem; font-weight: 600; padding: 4px 13px;
        border-radius: 99px; margin: 3px; border: 1px solid #B8D8F5;
    }
    .result-card {
        background: #FFFFFF;
        border: 1.5px solid #BDD9F2;
        border-radius: 16px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 10px rgba(74, 144, 217, 0.07);
    }
    .result-estilo {
        font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.07em; color: #4A90D9; margin-bottom: 0.4rem;
    }
    .result-texto { font-size: 0.9rem; color: #1E2733; line-height: 1.55; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E4F2FB 0%, #F0F8FD 100%) !important;
    }

    /* ── Divider ── */
    hr { border-color: #D0E8F7 !important; }

    /* ── Info tip ── */
    .info-tip {
        background: #EEF7FD;
        border: 1px solid #BDD9F2;
        border-radius: 12px;
        padding: 10px 14px;
        font-size: 0.82rem;
        color: #4A7FA8;
        display: flex;
        gap: 8px;
        align-items: flex-start;
        margin-top: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("###  Gerador de Legendas ")
    st.markdown("*Crie legendas incríveis para suas redes sociais com IA ✦*")
    st.markdown("---")
    st.markdown("*Como usar:*")
    st.markdown("1. Envie uma imagem (opcional)")
    st.markdown("2. Responda o questionário")
    st.markdown("3. Escolha quantas versões quer")
    st.markdown("4. Clique em *Gerar Legendas*")
    st.markdown("5. Copie a legenda favorita!")
    st.markdown("---")
    st.markdown("Feito com Streamlit + Groq")

# ── Header ──
st.markdown("""
<div class="app-header">
    <div class="app-logo">#</div>
    <div class="app-header-text">
        <p class="app-header-title"> Gerador de Legendas </p>
</div>
""", unsafe_allow_html=True)

# ── Hero ──
st.markdown("""
<div class="hero-section">
    <p class="hero-title">Crie legendas incríveis para suas redes sociais <span class="highlight">com IA✨</span></p>
    <p class="hero-subtitle">Envie uma imagem, responda algumas perguntas e receba sugestões de legendas personalizadas para o seu conteúdo.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Controle de versão para resetar widgets ──
if "form_version" not in st.session_state:
    st.session_state["form_version"] = 0
if "resultados" not in st.session_state:
    st.session_state["resultados"] = None

v = st.session_state["form_version"]

# ── Passo 1 — Upload ──
st.markdown("""
<div class="step-label">
    <div class="step-number">1</div>
    <div style="display:flex;flex-direction:column;justify-content:center;">
        <p class="step-title">Imagem do post</p>
        <p class="step-desc">Envie a imagem que vai usar no post (opcional)</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    uploaded_file = st.file_uploader(
        "Arraste e solte sua imagem aqui ou clique para selecionar",
        type=["jpg", "jpeg", "png", "webp"],
        key=f"uploader_{v}",
    )

    image_b64 = None
    if uploaded_file is not None:
        image_obj = Image.open(uploaded_file)
        st.image(image_obj, caption="Imagem carregada", use_column_width=True)
        buf = io.BytesIO()
        image_obj.save(buf, format="PNG")
        image_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    else:
        st.markdown("""
        <div class="info-tip">
            💡 Nossa IA vai analisar sua imagem e suas respostas para criar legendas que combinam com o seu estilo!
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Passo 2 — Quiz ──
st.markdown("""
<div class="step-label">
    <div class="step-number">2</div>
    <div style="display:flex;flex-direction:column;justify-content:center;">
        <p class="step-title">Responda algumas perguntas</p>
        <p class="step-desc">Isso vai nos ajudar a criar legendas perfeitas para você!</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        objetivo = st.selectbox(
            "Qual o objetivo da publicação?",
            options=[
                "Vender ou promover um produto/serviço",
                "Engajar e interagir com a audiência",
                "Educar ou informar o público",
                "Inspirar e motivar",
            ],
            index=None,
            placeholder="Escolha uma opção",
            key=f"objetivo_{v}",
        )
    with col2:
        rede_social = st.selectbox(
            "Rede social",
            options=[
                "Instagram",
                "TikTok",
                "LinkedIn",
                "Twitter/X",
            ],
            index=None,
            placeholder="Escolha uma opção",
            key=f"rede_{v}",
        )

    col3, col4 = st.columns(2)
    with col3:
        tom = st.selectbox(
            "Qual o estilo da legenda?",
            options=[
                "Engraçado e descontraído",
                "Profissional e formal",
                "Motivacional e inspirador",
                "Casual e amigável",
            ],
            index=None,
            placeholder="Escolha uma opção",
            key=f"tom_{v}",
        )
    with col4:
        publico = st.selectbox(
            "Qual é o seu público-alvo?",
            options=[
                "Jovens (18–25 anos)",
                "Adultos (26–40 anos)",
                "Empreendedores e profissionais",
                "Público geral",
            ],
            index=None,
            placeholder="Escolha uma opção",
            key=f"publico_{v}",
        )

    contexto = st.text_area(
        "Contexto extra (opcional)",
        placeholder="Ex: lançamento de produto, promoção de fim de semana...",
        height=90,
        key=f"contexto_{v}",
    )

st.divider()

# ── Passo 3 — Quantidade ──
st.markdown("""
<div class="step-label">
    <div class="step-number">3</div>
    <div style="display:flex;flex-direction:column;justify-content:center;">
        <p class="step-title">Quantas versões de legendas?</p>
        <p class="step-desc">Cada versão traz 3 legendas com estilos diferentes</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    quantidade = st.slider("Versões", min_value=1, max_value=5, value=1, key=f"qtd_{v}")
    st.caption(f"Você vai receber *{quantidade * 3}* legendas no total.")

st.divider()

# ── Funções ──
def render_post_preview(legenda_texto, hashtags, image_b64=None, username="seu_perfil"):
    hashtags_str = " ".join(hashtags) if hashtags else ""
    if image_b64:
        img_html = f'<img style="width:100%;aspect-ratio:1;object-fit:cover;display:block;" src="data:image/png;base64,{image_b64}" />'
    else:
        img_html = '<div style="width:100%;aspect-ratio:1;background:linear-gradient(135deg,#E4F2FB,#B8D8F5);display:flex;align-items:center;justify-content:center;font-size:3rem;">🖼️</div>'
    st.markdown(f"""
    <div style="background:#fff;border:1.5px solid #BDD9F2;border-radius:16px;overflow:hidden;max-width:380px;margin:0 auto 1.2rem auto;box-shadow:0 2px 12px rgba(74,144,217,0.12);">
        <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid #D8EEF9;">
            <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#7BBDE8,#4A90D9);"></div>
            <span style="font-weight:600;font-size:0.85rem;color:#1E2733;">{username}</span>
        </div>
        {img_html}
        <div style="padding:12px 14px;font-size:0.85rem;line-height:1.55;color:#1E2733;border-top:1px solid #D8EEF9;">
            <b>{username}</b> {legenda_texto}
        </div>
        <div style="padding:0 14px 12px;font-size:0.8rem;color:#4A90D9;">{hashtags_str}</div>
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
objetivo_ok = objetivo is not None
rede_ok     = rede_social is not None
tom_ok      = tom is not None
publico_ok  = publico is not None

if not (objetivo_ok and rede_ok and tom_ok and publico_ok):
    st.info("Preencha todas as opções do questionário para gerar as legendas.")

gerar_btn = st.button(
    "Gerar legendas",
    type="primary",
    use_container_width=True,
    disabled=not (objetivo_ok and rede_ok and tom_ok and publico_ok),
)

if gerar_btn:
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
    st.session_state["resultados"] = todos_resultados

# ── Exibir resultados ──
todos_resultados = st.session_state.get("resultados") or []

if todos_resultados:
    st.divider()
    st.markdown("""
    <div style="margin-bottom:1rem;">
        <p style="font-family:'Poppins',sans-serif;font-size:1.2rem;font-weight:800;color:#1E2733;margin-bottom:0.2rem;">
            Suas legendas estão prontas! 🎉
        </p>
        <p style="font-size:0.85rem;color:#6B7E8F;">Confira as sugestões criadas especialmente para você.</p>
    </div>
    """, unsafe_allow_html=True)

    for v_idx, resultado in enumerate(todos_resultados):
        hashtags = resultado.get("hashtags", [])
        legendas = resultado.get("legendas", [])

        if len(todos_resultados) > 1:
            st.markdown(f"<p style='font-family:Poppins,sans-serif;font-weight:700;color:#1E2733;font-size:1rem;margin:0.5rem 0 0.8rem'>Versão {v_idx + 1}</p>", unsafe_allow_html=True)

        for i, leg in enumerate(legendas):
            num = str(v_idx * 3 + i + 1).zfill(2)
            with st.expander(f"{num}  ·  {leg['estilo']}", expanded=(v_idx == 0 and i == 0)):
                render_post_preview(leg["texto"], hashtags, image_b64)
                legenda_completa = leg["texto"] + "\n\n" + " ".join(hashtags)
                st.text_area(label="", value=legenda_completa, height=120, key=f"leg_{v}{v_idx}{i}")
                st.code(legenda_completa, language=None)

        if hashtags:
            st.markdown("<p style='font-size:0.82rem;font-weight:700;color:#4A90D9;margin:0.8rem 0 0.4rem'> Hashtags sugeridas</p>", unsafe_allow_html=True)
            pills_html = "".join(f'<span class="hashtag-pill">{h}</span>' for h in hashtags)
            st.markdown(f'<div style="margin-bottom:1rem">{pills_html}</div>', unsafe_allow_html=True)

        st.divider()

    # CSV
    todas_legendas = []
    for v_idx, resultado in enumerate(todos_resultados):
        for leg in resultado.get("legendas", []):
            todas_legendas.append({
                "versao": v_idx + 1,
                "estilo": leg.get("estilo", ""),
                "texto": leg.get("texto", ""),
                "rede_social": rede_social,
                "tom": tom,
                "objetivo": objetivo,
            })

    df = pd.DataFrame(todas_legendas)
    csv = df.to_csv(index=False).encode("utf-8")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Recomeçar", use_container_width=True):
            st.session_state["resultados"] = None
            st.session_state["form_version"] += 1
            st.rerun()
    with col_b:
        st.download_button(
            label=" Copiar todas (CSV)",
            data=csv,
            file_name="legendas_geradas.csv",
            mime="text/csv",
            use_container_width=True,
        )
