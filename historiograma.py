import pandas as pd
from matplotlib import pyplot as plt

# ==========================================
# DADOS DO SITE SPOTIFY NEWSROOM
# ==========================================

# Top artistas mais streamados
artistas = [
    "Taylor Swift",
    "Bad Bunny",
    "Drake",
    "The Weeknd",
    "Ariana Grande",
    "Ed Sheeran",
    "Justin Bieber",
    "Billie Eilish",
    "Eminem",
    "Kanye West"
]

# posição no ranking
ranking_artistas = [1,2,3,4,5,6,7,8,9,10]

# Criar DataFrame artistas
df_artistas = pd.DataFrame({
    "Artist": artistas,
    "Rank": ranking_artistas
})

# ==========================================
# TOP MÚSICAS MAIS STREAMADAS
# ==========================================

musicas = [
    "Blinding Lights",
    "Shape of You",
    "Sweater Weather",
    "Starboy",
    "As It Was"
]

ranking_musicas = [1,2,3,4,5]

# Criar DataFrame músicas
df_musicas = pd.DataFrame({
    "Music": musicas,
    "Rank": ranking_musicas
})

# ==========================================
# SALVAR CSVs
# ==========================================

df_artistas.to_csv("top_artistas_spotify.csv", index=False)
df_musicas.to_csv("top_musicas_spotify.csv", index=False)

print("CSVs salvos com sucesso!")

# ==========================================
# GRÁFICO ARTISTAS
# ==========================================

ax = df_artistas.plot(
    kind='bar',
    x='Artist',
    y='Rank',
    figsize=(12,5),
    legend=False,
    title='Top 10 artistas mais streamados do Spotify'
)

# inverter eixo (#1 no topo)
ax.invert_yaxis()

plt.xlabel("Artistas")
plt.ylabel("Posição no ranking")

# remover bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# girar nomes
plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ==========================================
# GRÁFICO MÚSICAS
# ==========================================

ax = df_musicas.plot(
    kind='bar',
    x='Music',
    y='Rank',
    figsize=(10,5),
    legend=False,
    title='Top músicas mais streamadas do Spotify'
)

# inverter eixo
ax.invert_yaxis()

plt.xlabel("Músicas")
plt.ylabel("Posição no ranking")

# remover bordas
plt.gca().spines[['top', 'right']].set_visible(False)

# girar nomes
plt.xticks(rotation=20)

plt.tight_layout()

plt.show()
