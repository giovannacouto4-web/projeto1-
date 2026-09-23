# 02 — Limpeza e tratamento

**Quando usar:** base "suja" (`*_brutas.csv`) — duplicata, grafia inconsistente, tipo errado, ausência, valor inválido, coluna calculada. No template: **seções 4 e 5** (a célula `[NÃO COLE]` da seção 4 imprime os números de cada decisão para a resposta).

## As três funções (cole uma vez; são as da seção 4 do template)

As bases de prova do site do professor têm três armadilhas que o jeito "normal" não pega: acento (`saude` × `Saúde`), número com vírgula (`"347,9"`, `"R$ 724,84"`) e data começando pelo ano com barra (`2026/02/06`). Testado nas três bases que estão no site (Festival, Serviços Urbanos e CyberSyn): nenhuma data invertida, nenhum número perdido.

```python
import unicodedata

def padronizar(serie):
    # " Saúde ", "SAUDE", "saude" -> "saude": sem espaço sobrando, minúsculo, sem acento
    t = serie.astype("string").str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
    return t.map(lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode()
                 if isinstance(x, str) else x)

def para_numero(serie):
    # "R$ 1.234,56" -> 1234.56 | "347,9" -> 347.9 | "sem dado" -> vazio (NaN)
    if pd.api.types.is_numeric_dtype(serie):
        return serie
    t = serie.astype("string").str.replace(r"[^0-9,.\-]", "", regex=True)
    virgula = t.str.contains(",", na=False)
    t = t.where(~virgula, t.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    return pd.to_numeric(t, errors="coerce")

def converter_data(serie):
    # aceita 2026-08-05, 2026/08/05, 05/08/2026 (com ou sem hora) sem inverter dia e mês
    texto = serie.astype("string").str.strip()
    eh_iso = texto.str.match(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}").fillna(False).astype(bool)   # começa com o ano
    iso_txt = texto.where(eh_iso).str.replace("/", "-", regex=False)
    if int(pd.__version__.split(".")[0]) >= 2:
        iso = pd.to_datetime(iso_txt, format="ISO8601", errors="coerce")
        outros = pd.to_datetime(texto.where(~eh_iso), format="mixed", dayfirst=True, errors="coerce")
    else:
        iso = pd.to_datetime(iso_txt, errors="coerce")
        outros = pd.to_datetime(texto.where(~eh_iso), dayfirst=True, errors="coerce")
    return iso.fillna(outros)
```

## Ordem

1. duplicata → 2. texto → 3. números → 4. datas → 5. inválidos e ausentes → 6. coluna calculada → 7. **conferir**

Criar a taxa antes de tratar o denominador gera `inf`. Converter antes de tirar duplicata só desperdiça trabalho.

Postura da Aula 10: nunca mexa no bruto — trabalhe numa cópia (`df = df_bruto.copy()`) e registre cada decisão com o número de linhas afetadas.

---

## 1. Duplicata

```python
antes = len(df)
df = df.drop_duplicates(subset="id_publicacao").copy()   # <-- coluna identificadora
print(f"{antes - len(df)} duplicatas removidas")
```

- `subset=` é o que o enunciado pede quando diz "duplicidade **por** id". Sem ele, só saem linhas 100% idênticas (é o que a Aula 5 faz com `df.drop_duplicates()`).
- `.copy()` evita o `SettingWithCopyWarning` nas edições seguintes. Sempre que filtrar e depois escrever no resultado, use `.copy()`.

## 2. Texto categórico

`"Saúde"`, `"saude"` e `" SAÚDE "` contam como três temas no `groupby`. Só `strip` + `lower` **não** junta `saúde` com `saude`: precisa tirar o acento.

```python
df["tema"] = padronizar(df["tema"])                  # tudo vira "saude"
print(sorted(df["tema"].dropna().unique()))          # CONFIRA: sobrou o número certo?
```

Grafias realmente diferentes (sinônimo, abreviação) não se resolvem com caixa — mapeie na mão, como a Aula 10 faz com `"Sci-Fi"` → `"Science Fiction"`:

```python
# Serviços Urbanos: depois do padronizar ainda sobram "poda" e "poda preventiva", "app" e "aplicativo"...
df["servico"] = df["servico"].replace({"poda": "poda preventiva", "coleta": "coleta programada",
                                       "reparo calcada": "reparo de calcada"})
```

Nunca adivinhe o mapa: rode `df["tema"].unique()` antes e escreva com base no que apareceu.

## 3. Números que vieram como texto

```python
for col in ["alcance", "compartilhamentos", "salvamentos"]:        # <-- troque
    df[col] = para_numero(df[col])
```

O que não converte ("sem dado") vira `NaN` em vez de quebrar o código; você trata no passo 5, de forma visível. **Não use `pd.to_numeric` direto** se houver vírgula decimal: `pd.to_numeric("347,9", errors="coerce")` dá `NaN` sem avisar, e na base CyberSyn isso apagaria as colunas `distancia_km`, `estoque_destino_dias` e `prazo_horas` inteiras.

Se tiver símbolo junto (Aula 10: `"£51.77"`), tire antes:

```python
livros["preco"] = livros["preco"].str.replace("£", "", regex=False).str.strip()
livros["preco"] = pd.to_numeric(livros["preco"], errors="coerce")
# formato brasileiro "1.234,56":
# df["valor"] = df["valor"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
```

## 4. Datas em formatos misturados — a armadilha nº 1

O simulado diz que há "datas em formatos distintos" (`2026-08-05`, `25/08/2026` e, nas bases do site, `2026/08/05`). **Os jeitos óbvios erram sem dar erro, e o erro muda com a versão do pandas** (testado com 1.5, 2.2 e 3.0 — veja a sua com `print(pd.__version__)`):

| O que você escreve | O que acontece |
|---|---|
| `pd.to_datetime(s, errors="coerce")` | pandas 2 e 3: adivinha o formato pelo primeiro valor e transforma em `NaT` o que for diferente — perde linhas calado. pandas 1.5: inverte as `dd/mm` com dia ≤ 12 |
| `pd.to_datetime(s, format="mixed", dayfirst=True)` (**Aula 10**) | pandas 2.2: certo. **pandas 3: inverte dia e mês das ISO com dia ≤ 12** (`2026-08-05` vira 8 de maio). pandas 1.5: não existe, zera tudo sem avisar. Na aula não apareceu porque todas as datas tinham dia ≥ 20 |
| `pd.to_datetime(s, format="mixed")` | inverte as `dd/mm` com dia ≤ 12 |
| **ISO separado + método da aula no resto** | certo nas três versões (o `converter_data` trata `2026/08/05` como ISO) |

O `requirements.txt` do curso não fixa versão, então quem instalou agora com `uv pip install` tem pandas 3 — justamente a versão em que o método da aula inverte as datas.

A forma correta é o `converter_data` (no topo deste arquivo):

```python
df["data_publicacao"] = converter_data(df["data_publicacao"])
```

Aceita `2026-08-05`, `2026/08/05`, `2026-08-05 14:30`, `05/08/2026`, `21-08-2026`, `22-Aug-2026`. Data impossível (`2026-08-35`, `31/02/2026`) vira `NaT`.

**Confira sempre:**

```python
print("não convertidas:", df["data_publicacao"].isna().sum())
print(df["data_publicacao"].min(), "->", df["data_publicacao"].max())
```

Se aparecer mês fora do período do enunciado (janeiro numa campanha de agosto), a conversão inverteu dia e mês.

## 5. Inválidos e ausentes

Não existe resposta única (Aula 10): **descartar**, **preencher** ou **manter como ausente e documentar**. O que vale ponto é justificar.

```python
# denominador de taxa: zero, negativo ou ausente -> descarta (NaN > 0 é False, então sai junto)
df = df[df["alcance"] > 0].copy()

# campo essencial ausente -> descarta
df = df.dropna(subset=["id_publicacao"])

# parcela de uma soma -> preencher com a mediana é defensável
df["compartilhamentos"] = df["compartilhamentos"].fillna(df["compartilhamentos"].median())
```

Valor que existe, no tipo certo, mas fora do possível (Aula 10: avaliação vai de 1 a 5 estrelas; veio um 7). Nenhum `isna()` pega isso — só a regra do domínio:

```python
fora = (livros["avaliacao"] < 1) | (livros["avaliacao"] > 5)
print(f"{fora.sum()} avaliações fora de 1-5")
livros.loc[fora, "avaliacao"] = np.nan          # mantém a linha, marca o valor como ausente
```

- Mediana, não média: é menos sensível a extremos e mais fácil de justificar.
- `fillna(0)` em contagem afirma "teve zero" — diferente de "não sabemos". Só use com justificativa (a Aula 10 usa 0 como marcador explícito de "sem avaliação registrada").

## 6. Coluna calculada

```python
df["taxa_utilidade_pct"] = (df["compartilhamentos"] + df["salvamentos"]) / df["alcance"] * 100
```

Monte exatamente a fórmula do enunciado: numerador **entre parênteses**, divide, multiplica por 100 no fim. Se o denominador pudesse ser zero e você não tratou, sai `inf` — que **não** aparece em `isna()`:

```python
print(np.isinf(df["taxa_utilidade_pct"]).sum())
```

## 7. Conferir (10 segundos que salvam a questão)

```python
print(df.shape)
print(sorted(df["tema"].unique()))
print(df.dtypes)
print(df["taxa_utilidade_pct"].describe())
```

Taxa negativa, acima de 100% ou `inf` = algo errado no tratamento.

Validação no estilo da Aula 10 (para se a prova pedir "valide as colunas obrigatórias"):

```python
for coluna in ["id_publicacao", "tema", "alcance", "data_publicacao"]:
    if coluna not in df.columns:
        raise ValueError(f"Coluna obrigatória ausente: {coluna}")
    if df[coluna].isna().all():
        raise ValueError(f"Coluna obrigatória totalmente vazia: {coluna}")
print("Validação de colunas obrigatórias: OK")
```

---

## Resposta escrita (decisões de tratamento)

Uma frase por decisão, sempre com o **porquê**. Os números estão na célula `[NÃO COLE]` da seção 4 do template (`>>> PARA A RESPOSTA`).

> Removi os registros duplicados por `id_publicacao` para não contar a mesma publicação duas vezes. Padronizei `tema` (espaços e caixa) porque a mesma categoria aparecia escrita de formas diferentes, o que dividiria os grupos. Converti as datas tratando separadamente os formatos presentes, para não perder nem inverter registros. Descartei as linhas com `alcance` ausente ou não positivo, já que sem denominador válido a taxa não pode ser calculada, e preenchi ausências de `compartilhamentos` com a mediana, por ser menos sensível a valores extremos que a média.
