# BRIEF — analise-churn-cohort (area Dados/BI)

## Projeto
Analise de churn e coorte de retencao. MVP: coorte de retencao + curva de
churn. Stack: Python, pandas, matplotlib.

## Diretorio de entregas
C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\analise-churn-cohort\

## Arquivos criados
- pyproject.toml — declaracao do projeto, dependencias (pandas, matplotlib, pytest) e entry point CLI
- src/analise_churn_cohort/__init__.py — API publica do pacote
- src/analise_churn_cohort/cohort.py — geracao de dados sinteticos (random_state fixo), calculo de retencao por coorte, plotagem da curva de churn (PNG, sem exibicao)
- src/analise_churn_cohort/cli.py — interface de linha de comando
- src/analise_churn_cohort/__main__.py — ponto de entrada `python -m analise_churn_cohort`
- tests/test_cohort.py — suíte pytest (11 testes), incluindo calculo de retencao por coorte
- README.md — bilíngue PT-BR + EN (titulo, descricao, como usar, testes, licenca MIT, autor Kelvin Oliveira)
- BRIEF.md — este arquivo
- churn_curve.png — artefato gerado pelo pipeline (curva de churn)

Artefatos de ambiente (nao entregas): .venv/, uv.lock

## Comando de teste
uv run pytest -q

## Resultado dos testes
11 passed (PASS). Gate verify-and-stop satisfeito.

## Como verificar
1. Acesse o diretorio do projeto.
2. Rode: uv run pytest -q  -> deve reportar 11 aprovados.
3. Rode: uv run python -m analise_churn_cohort  -> gera churn_curve.png.
4. Leia: README.md (PT-BR e EN) e BRIEF.md.

## Autor
Kelvin Oliveira

## Licenca
MIT
