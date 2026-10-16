"""Analise de churn e coorte de retencao.

Exporta a API publica do pacote: geracao de dados sinteticos,
calculo de retencao por coorte e plotagem da curva de churn.
"""

from .cohort import (
    ChurnCurve,
    CohortRetention,
    Purchase,
    User,
    compute_cohort_retention,
    generate_synthetic_data,
    plot_churn_curve,
)

__all__ = [
    "ChurnCurve",
    "CohortRetention",
    "Purchase",
    "User",
    "compute_cohort_retention",
    "generate_synthetic_data",
    "plot_churn_curve",
]
