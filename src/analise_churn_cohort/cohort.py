"""Calculo de coorte de retencao e curva de churn.

Gera um dataset sintetico de usuarios e compras, atribui cada usuario
a uma coorte pelo mes de cadastro, calcula a matriz de retencao por
periodo (mes desde o cadastro) e plota a curva de churn acumulada.
Tudo e deterministico: usa random_state fixo e nao exibe figuras.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RANDOM_STATE: Final[int] = 42
MESES_COHORTE: Final[int] = 12


@dataclass(frozen=True)
class User:
    """Registro de usuario com data de cadastro."""

    user_id: int
    signup_date: pd.Timestamp


@dataclass(frozen=True)
class Purchase:
    """Registro de compra vinculada a um usuario."""

    purchase_id: int
    user_id: int
    purchase_date: pd.Timestamp
    value: float


@dataclass(frozen=True)
class CohortRetention:
    """Resultado do calculo de retencao por coorte.

    Attributes:
        retention: tabela (coorte x periodo) com taxa de retencao em [0, 1].
        cohort_sizes: numero de usuarios por coorte (index = mes de cadastro).
        periods: numero de periodos (meses) avaliados apos o cadastro.
    """

    retention: pd.DataFrame
    cohort_sizes: pd.Series
    periods: int


@dataclass(frozen=True)
class ChurnCurve:
    """Resultado da curva de churn acumulada.

    Attributes:
        churn_rate: taxa de churn acumulada por periodo (index = periodo).
        users_remaining: usuarios ainda ativos por periodo.
    """

    churn_rate: pd.Series
    users_remaining: pd.Series


def generate_synthetic_data(
    n_users: int = 1_000,
    n_purchases: int = 5_000,
    start_date: str = "2024-01-01",
    end_date: str = "2025-12-31",
    seed: int = RANDOM_STATE,
) -> tuple[list[User], list[Purchase]]:
    """Gera dataset sintetico de usuarios e compras.

    Args:
        n_users: quantidade de usuarios a gerar.
        n_purchases: quantidade de compras a gerar.
        start_date: data inicial do intervalo (inclusive).
        end_date: data final do intervalo (inclusive).
        seed: semente aleatoria fixa para determinismo.

    Returns:
        Tupla (usuarios, compras).
    """
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    n_days = len(dates)

    users: list[User] = []
    for user_id in range(1, n_users + 1):
        # Semente derivada por usuario: deterministica e independente.
        user_rng = np.random.default_rng(seed + user_id)
        signup_idx = int(user_rng.integers(0, n_days))
        signup_date = pd.Timestamp(dates[signup_idx])
        users.append(User(user_id=user_id, signup_date=signup_date))

    purchases: list[Purchase] = []
    purchase_rng = np.random.default_rng(seed + 10_000)
    user_indices = purchase_rng.integers(0, n_users, size=n_purchases)
    purchase_dates_idx = purchase_rng.integers(0, n_days, size=n_purchases)
    values = purchase_rng.uniform(10.0, 500.0, size=n_purchases).round(2)

    for purchase_id in range(1, n_purchases + 1):
        user_id = int(user_indices[purchase_id - 1]) + 1
        purchase_date = pd.Timestamp(dates[purchase_dates_idx[purchase_id - 1]])
        value = float(values[purchase_id - 1])
        purchases.append(
            Purchase(
                purchase_id=purchase_id,
                user_id=user_id,
                purchase_date=purchase_date,
                value=value,
            )
        )

    return users, purchases


def _to_dataframes(
    users: list[User], purchases: list[Purchase]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Converte listas de dataclasses em DataFrames do pandas."""
    users_df = pd.DataFrame(
        [{"user_id": u.user_id, "signup_date": u.signup_date} for u in users]
    )
    purchases_df = pd.DataFrame(
        [
            {
                "purchase_id": p.purchase_id,
                "user_id": p.user_id,
                "purchase_date": p.purchase_date,
                "value": p.value,
            }
            for p in purchases
        ]
    )
    return users_df, purchases_df


def compute_cohort_retention(
    users: list[User], purchases: list[Purchase], periods: int = MESES_COHORTE
) -> CohortRetention:
    """Calcula a matriz de retencao por coorte de cadastro.

    Cada usuario entra na coorte do mes de seu cadastro. O periodo 0 e o
    mes de cadastro propriamente dito (taxa 1.0). No periodo k, a taxa e a
    fracao de usuarios da coorte que fizeram pelo menos uma compra nos k
    meses seguintes ao cadastro.

    Args:
        users: lista de usuarios cadastrados.
        purchases: lista de compras realizadas.
        periods: quantidade de periodos (meses) apos o cadastro a avaliar.

    Returns:
        CohortRetention com a tabela de retencao, tamanhos de coorte e
        numero de periodos.
    """
    if periods <= 0:
        raise ValueError("periods deve ser maior que zero")

    users_df, purchases_df = _to_dataframes(users, purchases)

    if users_df.empty:
        empty = pd.DataFrame(dtype="float64")
        return CohortRetention(
            retention=empty,
            cohort_sizes=pd.Series(dtype="int64"),
            periods=periods,
        )

    users_df = users_df.copy()
    users_df["cohort_month"] = users_df["signup_date"].dt.to_period("M")

    first_purchase = (
        purchases_df.groupby("user_id")["purchase_date"].min().reset_index()
    )
    users_df = users_df.merge(first_purchase, on="user_id", how="left")
    users_df["first_purchase_month"] = users_df["purchase_date"].dt.to_period("M")

    purchases_df = purchases_df.merge(
        users_df[["user_id", "cohort_month"]], on="user_id", how="inner"
    )
    purchases_df["purchase_month"] = purchases_df["purchase_date"].dt.to_period("M")

    cohort_sizes = users_df.groupby("cohort_month")["user_id"].nunique()

    retention_rows: dict[pd.Period, dict[int, float]] = {}
    for cohort, group in users_df.groupby("cohort_month"):
        size = int(group["user_id"].nunique())
        if size == 0:
            continue
        row: dict[int, float] = {0: 1.0}
        cohort_user_ids = set(group["user_id"])
        cohort_purchases = purchases_df[
            purchases_df["user_id"].isin(cohort_user_ids)
        ]
        for period in range(1, periods + 1):
            limite = cohort + period
            ativos = cohort_purchases[
                cohort_purchases["purchase_month"] <= limite
            ]["user_id"].nunique()
            row[period] = ativos / size
        retention_rows[cohort] = row

    retention = pd.DataFrame.from_dict(retention_rows, orient="index")
    retention = retention.reindex(columns=range(periods + 1), fill_value=0.0)
    retention.index.name = "cohort_month"
    retention.columns.name = "period"

    return CohortRetention(
        retention=retention,
        cohort_sizes=cohort_sizes,
        periods=periods,
    )


def plot_churn_curve(
    retention: CohortRetention, output_path: str | Path = "churn_curve.png"
) -> Path:
    """Plota a curva de churn acumulada e salva em PNG (nao exibe).

    A curva mostra a taxa de churn acumulada por periodo, ou seja, a
    fracao de usuarios de cada coorte que pararam de comprar ate aquele
    periodo (1 - retencao media ponderada pelo tamanho da coorte).

    Args:
        retention: resultado do calculo de retencao por coorte.
        output_path: caminho do arquivo PNG de saida.

    Returns:
        Caminho do arquivo PNG gerado.
    """
    output = Path(output_path)
    if output.suffix.lower() != ".png":
        output = output.with_suffix(".png")

    if retention.retention.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, "Sem dados de retencao", ha="center", va="center")
        ax.set_axis_off()
        fig.savefig(output, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return output

    weighted = (
        retention.retention.mul(retention.cohort_sizes, axis=0)
        .sum()
        / retention.cohort_sizes.sum()
    )
    churn_rate = 1.0 - weighted

    fig, ax = plt.subplots(figsize=(8, 5))
    periods = list(range(retention.periods + 1))
    ax.plot(periods, churn_rate.reindex(periods, fill_value=0.0), marker="o")
    ax.set_xlabel("Periodo (meses apos cadastro)")
    ax.set_ylabel("Churn acumulado")
    ax.set_title("Curva de Churn por Coorte de Cadastro")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1)
    ax.set_xticks(periods)

    fig.tight_layout()
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output


def run_pipeline(
    output_dir: str | Path = ".",
    n_users: int = 1_000,
    n_purchases: int = 5_000,
) -> dict[str, Path]:
    """Executa o pipeline completo: dados, retencao e curva de churn.

    Args:
        output_dir: diretorio de saida para o PNG.
        n_users: quantidade de usuarios sinteticos.
        n_purchases: quantidade de compras sinteticas.

    Returns:
        Dicionario com caminhos dos artefatos gerados.
    """
    users, purchases = generate_synthetic_data(
        n_users=n_users, n_purchases=n_purchases
    )
    retention = compute_cohort_retention(users, purchases)
    png_path = plot_churn_curve(retention, Path(output_dir) / "churn_curve.png")
    return {"churn_curve_png": png_path}
