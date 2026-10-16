"""Suite de testes para o modulo cohort.

Cobre: geracao de dados sinteticos (determinismo e contagem),
calculo de retencao por coorte (periodo 0, intervalo [0,1], formato)
e plotagem da curva de churn (arquivo PNG gerado, sem exibicao).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from analise_churn_cohort.cohort import (
    MESES_COHORTE as EXPECTED_PERIODS,
    RANDOM_STATE,
)
from analise_churn_cohort import (
    compute_cohort_retention,
    generate_synthetic_data,
    plot_churn_curve,
)


@pytest.fixture
def users_purchases():
    """Dataset pequeno e deterministico para os testes de retencao."""
    return generate_synthetic_data(n_users=200, n_purchases=800, seed=RANDOM_STATE)


def test_generate_synthetic_data_returns_expected_counts():
    """A geracao produz exatamente n_users usuarios e n_purchases compras."""
    users, purchases = generate_synthetic_data(n_users=50, n_purchases=200, seed=7)
    assert len(users) == 50
    assert len(purchases) == 200


def test_generate_synthetic_data_is_deterministic():
    """Mesma semente produz datasets iguais (determinismo exigido)."""
    a_users, a_purchases = generate_synthetic_data(n_users=100, n_purchases=400, seed=3)
    b_users, b_purchases = generate_synthetic_data(n_users=100, n_purchases=400, seed=3)
    assert a_users == b_users
    assert a_purchases == b_purchases


def test_generate_synthetic_data_different_seed_differs():
    """Sementes diferentes produziu datasets diferentes (nao e constante)."""
    a_users, _ = generate_synthetic_data(n_users=100, n_purchases=400, seed=1)
    b_users, _ = generate_synthetic_data(n_users=100, n_purchases=400, seed=2)
    assert a_users != b_users


def test_compute_cohort_retention_period_zero_is_one(users_purchases):
    """No periodo 0 (mes de cadastro) a retencao de toda coorte e 1.0."""
    users, purchases = users_purchases
    result = compute_cohort_retention(users, purchases, periods=EXPECTED_PERIODS)
    assert (result.retention[0] == 1.0).all()


def test_compute_cohort_retention_values_in_range(users_purchases):
    """Todas as taxas de retencao estao no intervalo [0, 1]."""
    users, purchases = users_purchases
    result = compute_cohort_retention(users, purchases, periods=EXPECTED_PERIODS)
    values = result.retention.values
    assert (values >= 0).all() and (values <= 1).all()


def test_compute_cohort_retention_shape(users_purchases):
    """A tabela tem uma linha por coorte e (periods + 1) colunas (0..periods)."""
    users, purchases = users_purchases
    result = compute_cohort_retention(users, purchases, periods=EXPECTED_PERIODS)
    assert result.retention.shape[1] == EXPECTED_PERIODS + 1
    assert result.periods == EXPECTED_PERIODS
    assert len(result.cohort_sizes) == len(result.retention)


def test_compute_cohort_retention_periods_must_be_positive(users_purchases):
    """periods <= 0 deve levantar ValueError."""
    users, purchases = users_purchases
    with pytest.raises(ValueError, match="periods"):
        compute_cohort_retention(users, purchases, periods=0)
    with pytest.raises(ValueError, match="periods"):
        compute_cohort_retention(users, purchases, periods=-3)


def test_compute_cohort_retention_empty_input():
    """Lista vazia de usuarios nao quebra o calculo (retencao vazia)."""
    result = compute_cohort_retention([], [], periods=6)
    assert result.retention.empty
    assert result.periods == 6


def test_plot_churn_curve_creates_png(tmp_path: Path, users_purchases):
    """plot_churn_curve gera um arquivo PNG nao vazio (nao exibe a figura)."""
    users, purchases = users_purchases
    result = compute_cohort_retention(users, purchases)
    out = tmp_path / "churn_curve.png"
    path = plot_churn_curve(result, out)
    assert path == out
    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_churn_curve_handles_empty_retention(tmp_path: Path):
    """Retencao vazia ainda assim gera um arquivo PNG de saida."""
    empty = compute_cohort_retention([], [], periods=6)
    out = tmp_path / "churn_curve_empty.png"
    path = plot_churn_curve(empty, out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_churn_curve_forces_png_extension(tmp_path: Path, users_purchases):
    """Sem extensao .png, a saida recebe .png automaticamente."""
    users, purchases = users_purchases
    result = compute_cohort_retention(users, purchases)
    out = tmp_path / "curva"  # sem extensao
    path = plot_churn_curve(result, out)
    assert path.suffix == ".png"
    assert path.exists()
