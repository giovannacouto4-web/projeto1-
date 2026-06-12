import streamlit as st
from groq import Groq
import pandas as pd
from PIL import Image
import json
import io
import base64

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

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

    /* Preview do post estilo Instagram */
    .post-preview-card {
        background: #fff;
        border: 1px solid #dbdbdb;
        border-radius: 12px;
        overflow: hidden;
        max-width: 400px;
        margin: 0 auto 1.5rem auto;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    .post-preview-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        border-bottom: 1px solid #f0f0f0;
    }
    .post-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7F77DD, #c084fc);
    }
    .post-username {
        font-weight: 600;
        font-size: 0.85rem;
        color: #1a1a1a;
    }
    .post-preview-image {
        width: 100%;
        aspect-ratio: 1;
        object-fit: cover;
        display: block;
    }
    .post-preview-caption {
        padding: 12px 14px;
        font-size: 0.85rem;
        line-height: 1.5;
        color: #1a1a1a;
        border-top: 1px solid #f0f0f0;
    }
    .post-preview-caption b {
        font-weight: 600;
    }
    .post-preview-hashtags {
        padding: 0 14px 12px;
        font-size: 0.8rem;
        color: #534AB7;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Sidebar — informações
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✦ Gerador de Legendas")
    st.markdown("---")
    st.markdown("**Como usar:**")
    st.markdown("1. Envie uma imagem (opcional)")
    st.markdown("2. Responda o questionário")
    st.markdown("3. Clique em **Gerar Legendas**")
    st.markdown("4. Copie a legenda favorita!")
    st.markdown("---")
    st.markdown("*Feito com Streamlit + Groq*")


# ─────────────────────────────────────────────
# Título
# ─────────────────────────────────────────────
st.markdown('<p class="main-title">✦ Gerador de Legendas</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Envie sua imagem e responda o questionário para receber legendas personalizadas com IA</p>', unsafe_allow_html=True)

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
image_b64 = None

if uploaded_file:
    image_obj = Image.open(uploaded_file)
    st.image(image_obj, caption="Imagem carregada", use_column_width=True)
    buf = io.BytesIO()
    image_obj.save(buf, format="PNG")
    image_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

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
    "Contexto extra (opcional)",
    placeholder="Ex: lançamento de produto, promoção de fim de semana, dia do cliente...",
    height=90,
)

st.divider()


# ─────────────────────────────────────────────
# Função auxiliar — preview do post
# ─────────────────────────────────────────────
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
        <div class="post-preview-caption">
            <b>{username}</b> {legenda_texto}
        </div>
        <div class="post-preview-hashtags">{hashtags_str}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Função principal — gerar legendas
# ─────────────────────────────────────────────
def gerar_legendas(objetivo, rede_social, tom, publico, contexto, image_b64):

    prompt = f"""
Você é um especialista em marketing digital e copywriting.

Crie 3 legendas para redes sociais.

Objetivo: {objetivo}
Rede social: {rede_social}
Tom: {tom}
Público-alvo: {publico}
Contexto: {contexto}

Retorne SOMENTE JSON válido.

Formato:

{{
  "legendas": [
    {{
      "estilo": "Direto ao ponto",
      "texto": "Legenda aqui"
    }},
    {{
      "estilo": "Storytelling",
      "texto": "Legenda aqui"
    }},
    {{
      "estilo": "Engajamento",
      "texto": "Legenda aqui"
    }}
  ],
  "hashtags": [
    "#hashtag1",
    "#hashtag2",
    "#hashtag3",
    "#hashtag4",
    "#hashtag5",
    "#hashtag6"
  ]
}}
"""

    if image_b64:
        content = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_b64}"
                }
            },
            {
                "type": "text",
                "text": prompt
            }
        ]
        model = "meta-llama/llama-4-scout-17b-16e-instruct"
    else:
        content = prompt
        model = "llama-3.3-70b-versatile"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": content}
        ],
        temperature=0.8,
        max_tokens=1500,
        response_format={"type": "json_object"}
    )

    raw = response.choices[0].message.content

    try:
        return json.loads(raw)
    except Exception:
        st.write("Resposta recebida:")
        st.code(raw)
        raise


# ─────────────────────────────────────────────
# Botão gerar + exibição dos resultados
# ─────────────────────────────────────────────
if "resultado" not in st.session_state:
    st.session_state.resultado = None

if st.session_state.resultado is None:
    gerar_clicado = st.button("✨ Gerar Legendas", type="primary", use_container_width=True)
    regenerar_clicado = False
    recomecar_clicado = False
else:
    col_regenerar, col_recomecar = st.columns(2)
    with col_regenerar:
        regenerar_clicado = st.button("🔁 Gerar Outras Legendas (mesma foto)", type="primary", use_container_width=True)
    with col_recomecar:
        recomecar_clicado = st.button("🔄 Recomeçar", use_container_width=True)
    gerar_clicado = False

if recomecar_clicado:
    st.session_state.resultado = None
    st.rerun()

if gerar_clicado or regenerar_clicado:
    with st.spinner("Gerando suas legendas com IA..."):
        try:
            resultado = gerar_legendas(
                objetivo, rede_social, tom, publico, contexto, image_b64
            )
            st.session_state.resultado = resultado
        except json.JSONDecodeError:
            st.error("❌ Erro ao interpretar a resposta da IA. Tente novamente.")
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

if st.session_state.resultado:
    try:
            resultado = st.session_state.resultado
            hashtags = resultado.get("hashtags", [])
            legendas = resultado.get("legendas", [])

            st.divider()
            st.markdown('<p class="step-header">Passo 4 — Suas legendas</p>', unsafe_allow_html=True)

            # ── Exibir cada legenda com preview e botão copiar ──
            for i, leg in enumerate(legendas):
                with st.expander(f"✦ {leg['estilo']}", expanded=True):

                    # Preview do post
                    st.markdown("**Pré-visualização do post**")
                    render_post_preview(leg["texto"], hashtags, image_b64)

                    # Caixa de texto com a legenda (fácil de copiar)
                    st.markdown("**Legenda completa**")
                    legenda_completa = leg["texto"] + "\n\n" + " ".join(hashtags)
                    st.text_area(
                        label="",
                        value=legenda_completa,
                        height=130,
                        key=f"legenda_{i}",
                        help="Selecione o texto e copie (Ctrl+A, Ctrl+C)"
                    )

                    # Botão de copiar (via st.code — clique no ícone de cópia)
                    st.caption("Ou use o botão de cópia abaixo:")
                    st.code(legenda_completa, language=None)

            # ── Hashtags separadas ──
            if hashtags:
                st.markdown("---")
                st.markdown("**#️⃣ Hashtags sugeridas**")
                pills_html = "".join(
                    f'<span class="hashtag-pill">{h}</span>' for h in hashtags
                )
                st.markdown(f'<div style="margin:0.5rem 0 1rem">{pills_html}</div>', unsafe_allow_html=True)
                st.code(" ".join(hashtags), language=None)

            # ── Histórico / CSV ──
            st.divider()
            st.markdown("**Histórico desta geração**")
            df = pd.DataFrame(legendas)
            df.insert(0, "Rede Social", rede_social)
            df.insert(1, "Tom", tom)
            df.insert(2, "Objetivo", objetivo)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Baixar como CSV",
                data=csv,
                file_name="legendas_geradas.csv",
                mime="text/csv",
            )

    except json.JSONDecodeError:
        st.error("❌ Erro ao interpretar a resposta da IA. Tente novamente.")
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")

