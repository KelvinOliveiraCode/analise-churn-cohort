# Analise de Churn e Coorte de Retencao

Projeto da area Dados/BI. Analise de churn e coorte de retencao de clientes.

Gera um dataset sintetico de usuarios e compras, atribui cada usuario a uma
coorte pelo mes de cadastro, calcula a taxa de retencao por periodo e plota a
curva de churn acumulada. O grafico e salvo em PNG; nao e exibido na tela.

Stack: Python, pandas, matplotlib.

## Como usar

Crie o ambiente virtual e instale as dependencias:

uv sync

Rode o pipeline:

uv run python -m analise_churn_cohort

Saida: churn_curve.png no diretorio atual.

Opcoes da linha de comando:

--n-users      quantidade de usuarios (padrao: 1000)
--n-purchases  quantidade de compras (padrao: 5000)
--output-dir   diretorio de saida do PNG (padrao: .)
--seed         semente aleatoria fixa (padrao: 42)

Exemplo:

uv run python -m analise_churn_cohort --n-users 500 --n-purchases 2000 --output-dir .

## Testes

Rode a suíte pytest:

uv run pytest -q

Resultado esperado: 11 aprovados.

Inclui teste de calculo de retencao por coorte: periodo 0 igual a 1.0, todos
os valores entre 0 e 1, formato da tabela (coortes x periods + 1), periodo
invalido levanta ValueError e entrada vazia nao quebra o calculo.

## Licenca

MIT

## Autor

Kelvin Oliveira

---

# Churn and Cohort Retention Analysis

Data/BI project. Churn analysis and customer retention cohorts.

Generates a synthetic dataset of users and purchases, assigns each user to a
cohort by signup month, calculates the retention rate per period, and plots
the cumulative churn curve. The chart is saved as a PNG; it is not displayed
on screen.

Stack: Python, pandas, matplotlib.

## How to use

Create the virtual environment and install the dependencies:

uv sync

Run the pipeline:

uv run python -m analise_churn_cohort

Output: churn_curve.png in the current directory.

Command-line options:

--n-users      number of users (default: 1000)
--n-purchases  number of purchases (default: 5000)
--output-dir   output directory for the PNG (default: .)
--seed         fixed random seed (default: 42)

Example:

uv run python -m analise_churn_cohort --n-users 500 --n-purchases 2000 --output-dir .

## Tests

Run the pytest suite:

uv run pytest -q

Expected result: 11 passed.

Includes a cohort retention calculation test: period 0 equals 1.0, all values
between 0 and 1, table shape (cohorts x periods + 1), invalid period raises
ValueError, and empty input does not break the calculation.

## License

MIT

## Author

Kelvin Oliveira
