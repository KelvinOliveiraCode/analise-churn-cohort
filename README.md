# Analise de Churn e Coorte de Retencao

Analise de churn e coorte de retencao de clientes. Projeto da area Dados/BI.

Gera um dataset sintetico de usuarios e compras, atribui cada usuario a uma
coorte pelo mes de cadastro, calcula a taxa de retencao por periodo e plota a
curva de churn acumulada. O grafico e salvo em PNG; nao e exibido na tela.
Tudo e deterministico: usa semente aleatoria fixa (padrao 42).

Stack: Python, pandas, matplotlib.

## Sobre o projeto

O pacote `analise_churn_cohort` gera dados sinteticos de usuarios e compras,
organiza os usuarios em coortes pelo mes de cadastro e calcula a matriz de
retencao: no periodo 0 (mes de cadastro) a retencao e 1.0; no periodo k, a taxa
e a fracao de usuarios da coorte que fizeram pelo menos uma compra nos k meses
seguintes ao cadastro. A curva de churn mostra a taxa acumulada de churn por
periodo (1 menos a retencao media ponderada pelo tamanho da coorte) e e salva
como `churn_curve.png`.

Principais funcoes da API publica:

- `generate_synthetic_data(n_users, n_purchases, start_date, end_date, seed)`:
  usuarios e compras sinteticos, deterministico por semente.
- `compute_cohort_retention(users, purchases, periods)`: tabela de retencao
  (coorte x periodo), tamanhos de coorte e numero de periodos. Levanta
  `ValueError` se `periods <= 0`; entrada vazia nao quebra o calculo.
- `plot_churn_curve(retention, output_path)`: plota e salva a curva de churn
  em PNG (nao exibe); forca a extensao `.png`.
- `run_pipeline(output_dir, n_users, n_purchases)`: executa o pipeline
  completo e retorna o caminho do PNG gerado.

Valores padrao: 1000 usuarios, 5000 compras, intervalo de 2024-01-01 a
2025-12-31, semente 42, 12 periodos.

## Estrutura do repositorio

| Caminho | Conteudo |
| --- | --- |
| `pyproject.toml` | Declaracao do projeto (hatchling), dependencias pandas>=2.0, matplotlib>=3.7, pytest>=9.1.1, ponto de entrada CLI `analise-churn-cohort` |
| `src/analise_churn_cohort/__init__.py` | API publica: `ChurnCurve`, `CohortRetention`, `Purchase`, `User`, `compute_cohort_retention`, `generate_synthetic_data`, `plot_churn_curve` |
| `src/analise_churn_cohort/cohort.py` | Geracao de dados sinteticos, calculo de retencao por coorte e plotagem da curva de churn |
| `src/analise_churn_cohort/cli.py` | Interface de linha de comando (`--n-users`, `--n-purchases`, `--output-dir`, `--seed`) |
| `src/analise_churn_cohort/__main__.py` | Ponto de entrada `python -m analise_churn_cohort` |
| `tests/test_cohort.py` | 11 testes pytest: contagem e determinismo dos dados, retencao por coorte (periodo 0, intervalo [0,1], formato, ValueError, entrada vazia) e geracao do PNG |
| `churn_curve.png` | Artefato gerado pelo pipeline (curva de churn) |
| `README.md` | Este documento (PT-BR) |
| `README.en.md` | Mesmo documento em ingles |
| `BRIEF.md` | Resumo de entregas e como verificar |

## Requisitos

- Python >= 3.10
- pandas >= 2.0
- matplotlib >= 3.7
- pytest >= 9.1.1 (para os testes)

## Como usar

Crie o ambiente virtual e instale as dependencias:

```
uv sync
```

Rode o pipeline:

```
uv run python -m analise_churn_cohort
```

Saida: `churn_curve.png` no diretorio atual. O console imprime o caminho do
PNG, o numero de coortes e o numero de periodos.

Opcoes da linha de comando:

| Opcao | Padrao | Significado |
| --- | --- | --- |
| `--n-users` | 1000 | Quantidade de usuarios sinteticos |
| `--n-purchases` | 5000 | Quantidade de compras sinteticas |
| `--output-dir` | . | Diretorio de saida do PNG |
| `--seed` | 42 | Semente aleatoria fixa para determinismo |

Exemplo:

```
uv run python -m analise_churn_cohort --n-users 500 --n-purchases 2000 --output-dir .
```

O ponto de entrada instalado tambem esta disponivel como:

```
uv run analise-churn-cohort --n-users 500 --n-purchases 2000
```

## Testes

Rode a suíte pytest:

```
uv run pytest -q
```

Resultado esperado: 11 aprovados.

Os testes cobrem: geracao de dados (contagem exata, determinismo pela semente,
sementes diferentes produzem dados diferentes), calculo de retencao por coorte
(periodo 0 igual a 1.0, todos os valores entre 0 e 1, formato da tabela
coortes x periods + 1, periodo invalido levanta ValueError, entrada vazia nao
quebra o calculo) e plotagem da curva de churn (arquivo PNG nao vazio gerado,
nao exibido na tela, forcao da extensao .png).

## Licenca

MIT

## Autor

Kelvin Oliveira
