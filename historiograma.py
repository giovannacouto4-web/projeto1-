import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

# =========================
# PEGAR DADOS DO SITE
# =========================

url = "https://kworb.net/spotify/listeners.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

# Ler o HTML
soup = BeautifulSoup(response.text, "html.parser")

# Pegar tabela
tabela = soup.find("table")

# Transformar em DataFrame
df = pd.read_html(str(tabela))[0]

# =========================
# LIMPAR DADOS
# =========================

# Mostrar colunas
print(df.columns)

# Renomear colunas (caso necessário)
df.columns = ["Rank", "Artist", "Listeners", "Daily Trend", "Peak", "LW"]

# Remover vírgulas dos números
df["Listeners"] = (
    df["Listeners"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(int)
)

# =========================
# ESCOLHER TOP 10
# =========================

top10 = df.head(10)

# =========================
# SALVAR CSV
# =========================

top10.to_csv("spotify_top10.csv", index=False)

print("CSV salvo com sucesso!")

# =========================
# CRIAR GRÁFICO
# =========================

ax = top10.plot(
    kind="bar",
    x="Artist",
    y="Listeners",
    figsize=(12, 6),
    title="Top 10 artistas com mais ouvintes mensais no Spotify",
    legend=False
)

# Nome dos eixos
plt.xlabel("Artistas")
plt.ylabel("Ouvintes mensais")

# Girar nomes
plt.xticks(rotation=45)

# Tirar bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# Formatar eixo Y em milhões
ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f'{x/1e6:.0f}M')
)

# Ajustar layout
plt.tight_layout()

# Mostrar gráfico
plt.show()
