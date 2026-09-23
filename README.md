# Guia de Consulta — Extração e Análise de Dados

Material de consulta para a A1 de E&AD (Prof. Matheus Pestana, FGV 2026.2) — prova prática, **conteúdo até a Aula 13** (a Aula 14, de API e persistência, não cai).
Organizado por **técnica**, não por questão: serve mesmo que a prova mude o tema, os nomes das colunas ou a ordem das perguntas.

Baseado no simulado "Festival ViraBairro" e no código das aulas do [repositório da matéria](https://github.com/mateuspestana/extracao_analise_2026). Todo o código foi executado e testado com pandas 1.5, 2.2 e 3.0.

---

## Para a prova (deixe aberto)

1. **`prova-template.ipynb`** — comece por aqui. Uma seção por tipo de questão. Células **`# [COLE]`** são código de prova: copie a célula inteira e troque o que tem `# <-- troque` — ela produz só o que o enunciado pede. Células **`# [NÃO COLE]`** são conferência para você (imprimem `>>> PARA A RESPOSTA` com os números para o texto). Nenhuma célula precisa ser copiada pela metade. Roda inteiro de cara com uma base de exemplo; na prova, troque `PASTA` na seção 1.
   [Abrir no Colab](https://colab.research.google.com/github/BeAmara1/prova-pestana/blob/main/prova-template.ipynb)
2. **`00-fluxograma.md`** — quando não souber por onde começar: qual seção do template, qual modelo, em que ordem limpar, qual gráfico.
3. **`10-frases-prontas.md`** — para escrever as respostas sem travar.
4. **`12-erros-por-questao.md`** — antes de fechar cada questão, a lista do que costuma custar ponto.
5. **`11-erros-comuns.md`** — quando der erro (ou quando o resultado parecer estranho sem dar erro).

## No site da prova ([mateuspestana.github.io/prova](https://mateuspestana.github.io/prova/))

O site roda Python no navegador (Pyodide 0.28, pandas 2.3). O template foi testado lá dentro, com o mesmo código que o site usa para executar as células e as bases reais da pasta `dados/` do site: as 8 questões do simulado rodam, com tabelas e gráficos aparecendo.

1. **Na 1ª célula de código** (a de imports do professor), cole embaixo a célula de Setup (seção 1) e a das funções de limpeza (seção 4). Troque `PASTA = "dados"`. Execute uma vez.
2. **Cada questão tem uma célula só.** Cole nela, uma embaixo da outra, as células `[COLE]` que a questão pede.
3. O site só mostra sozinho o valor da **última** linha da célula; por isso toda tabela do template já está em `print(...)`. Gráficos aparecem todos.
4. **Não funciona no site:** `display()` (use `print`), `requests`, Playwright e BeautifulSoup (o site não carrega `bs4`, e a prova proíbe instalar biblioteca e fazer coleta).
5. **Limpeza:** as bases do site têm acento misturado (`saude`/`Saúde`), sinônimos (`app`/`Aplicativo`), número com vírgula ou `R$` (`"347,9"`, `"R$ 724,84"`) e data `2026/02/06`. Use `padronizar`, `para_numero` e `converter_data` (seção 4); o `to_numeric` sozinho apaga os números com vírgula sem avisar. Depois do `padronizar`, confira o `print` das categorias e mapeie os sinônimos que sobrarem.

## Roteiro de 30 segundos (toda questão)

1. **Que arquivo?** `*_brutas.csv` → precisa limpar. `*_analise.csv` → usar direto, em variável nova.
2. **Que tipo de tarefa?** Ache a seção na tabela abaixo (ou siga o `00-fluxograma.md`).
3. **Copie as células `[COLE]` da seção**, inteiras, e troque o que está marcado com `# <-- troque`.
4. **Rode e confira o resultado** — não confie só porque não deu erro.
5. **Escreva a resposta** com os números da célula `[NÃO COLE]` da seção e uma frase do `10-frases-prontas.md`.

---

## Índice: "o enunciado pede isso" → "vá para"

| O enunciado pede... | Template | Explicação |
|---|---|---|
| head, shape, ausências, tipos, valores únicos, "conhecer a base" | seção 3 | `01-diagnostico.md` |
| tirar duplicata, padronizar texto, converter data/número, tratar ausente/inválido | seção 4 | `02-limpeza.md` |
| criar uma taxa com fórmula; features a partir de legenda/hashtags/data | seção 5 | `02-limpeza.md`, `06-regressao.md` |
| tabela por grupo, contagem + média/mediana, cruzar duas categorias, hashtags | seção 6 | `03-agrupar-e-tabelas.md` |
| gráfico de barras / linha / dispersão / horizontal, título, eixos, fonte | seção 7 | `04-graficos.md` |
| "por dia", recorte por hora/formato, top 5 | seção 8 | `05-datas-e-recortes.md` |
| **prever um número** (taxa esperada) — MAE, R², modelo bobo | seção 9 | `06-regressao.md` |
| **prever uma categoria** (merece/não merece) — precisão, recall, F1, matriz, cortes, importâncias | seção 10 | `07-classificacao.md` |
| **agrupar sem rótulo** — KMeans, escolher k, perfis | seção 11 | `08-clusterizacao.md` |
| extrair de HTML (BeautifulSoup, requests) | seção 12 | `09-scraping-e-apis.md` |
| a **resposta escrita** (causalidade, limitação, interpretação) | blocos "Para a resposta" | `10-frases-prontas.md` |
| não sei qual técnica / qual modelo / qual gráfico | — | `00-fluxograma.md` |
| só quero o snippet, rápido | — | `00-COLA-RAPIDA.md` |

**Dica de velocidade:** no GitHub, `t` busca arquivo e `Ctrl+F` busca dentro dele. Os títulos usam as palavras do enunciado ("mediana por tema", "matriz de confusão", "vazamento") de propósito.

---

## Checklist — as 10 coisas que mais custam nota

1. **Recarregue o CSV** quando o enunciado disser "em uma nova variável" ou "use somente o arquivo X".
2. **Gráfico sem título, sem nome de eixo ou sem a fonte dentro da figura** é ponto perdido. Se o enunciado escreve "Fonte: ...", isso tem que aparecer no gráfico.
3. **Mediana ≠ média**, e **taxa de utilidade ≠ taxa de engajamento**. Leia a palavra no enunciado.
4. **Nunca afirme causalidade.** "Associado a", "tende a", "nesta base". Nunca "causa", "prova que", "garante".
5. **Vazamento de dados:** para prever algo *antes* da publicação, nada de `alcance`, interações, curtidas, compartilhamentos, salvamentos, nem a coluna que gerou o rótulo. R² ou F1 perto de 1 de primeira = vazamento quase certo.
6. **`random_state=42`** em tudo que sorteia (split, árvore, floresta, KMeans).
7. **`stratify=y`** no split de classificação; **padronize** (`StandardScaler`) antes da regressão logística e do KMeans.
8. **Categoria vira número** com `pd.get_dummies(..., drop_first=True, dtype=int)` antes de qualquer modelo.
9. **Confira datas, números e categorias depois de limpar.** Datas: o jeito da Aula 10 (`format="mixed", dayfirst=True`) inverte dia e mês das datas que começam pelo ano no pandas 3. Números: `to_numeric` apaga `"347,9"`. Categorias: `strip().lower()` não junta `saude` com `Saúde`. As funções da seção 4 resolvem as três; veja `02-limpeza.md`.
10. **Respeite o limite de frases.** Uma frase por item pedido (indicação, explicação, limitação).

---

## Estrutura

```
.
├── README.md
├── prova-template.ipynb               ← o notebook para a prova
├── solucao-simulado-virabairro.ipynb  ← o simulado inteiro resolvido
├── 00-fluxograma.md                   ← decisão rápida: seção, modelo, limpeza, gráfico
├── 00-COLA-RAPIDA.md                  ← os snippets mais usados, numa página
├── 01-diagnostico.md
├── 02-limpeza.md
├── 03-agrupar-e-tabelas.md
├── 04-graficos.md
├── 05-datas-e-recortes.md
├── 06-regressao.md
├── 07-classificacao.md
├── 08-clusterizacao.md
├── 09-scraping-e-apis.md
├── 10-frases-prontas.md
├── 11-erros-comuns.md
├── 12-erros-por-questao.md
└── 99-testar-a-cola.py                ← confere se o template roda na versão de hoje
```

## Conferir antes da prova

Roda o template inteiro e confere os resultados (não só se deu erro):

```bash
python 99-testar-a-cola.py
```

No Colab:

```python
!git clone https://github.com/BeAmara1/prova-pestana.git
%cd prova-pestana
!python 99-testar-a-cola.py
```
