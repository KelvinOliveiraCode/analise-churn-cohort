"""Interface de linha de comando do analise-churn-cohort."""

from __future__ import annotations

import argparse
from pathlib import Path

from .cohort import RANDOM_STATE, compute_cohort_retention, generate_synthetic_data, plot_churn_curve


def build_parser() -> argparse.ArgumentParser:
    """Constrói o parser de argumentos da CLI."""
    parser = argparse.ArgumentParser(
        prog="analise-churn-cohort",
        description="Gera dados sinteticos, calcula retencao por coorte e plota a curva de churn.",
    )
    parser.add_argument(
        "--n-users",
        type=int,
        default=1_000,
        help="Quantidade de usuarios sinteticos (padrao: 1000).",
    )
    parser.add_argument(
        "--n-purchases",
        type=int,
        default=5_000,
        help="Quantidade de compras sinteticas (padrao: 5000).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Diretorio de saida do PNG (padrao: diretorio atual).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=RANDOM_STATE,
        help="Semente aleatoria fixa para determinismo (padrao: 42).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada da CLI. Retorna 0 em sucesso."""
    args = build_parser().parse_args(argv)

    users, purchases = generate_synthetic_data(
        n_users=args.n_users,
        n_purchases=args.n_purchases,
        seed=args.seed,
    )
    retention = compute_cohort_retention(users, purchases)
    png_path = plot_churn_curve(retention, args.output_dir / "churn_curve.png")
    print(f"Curva de churn salva em: {png_path}")
    print(f"Coortes: {len(retention.cohort_sizes)} | Periodos: {retention.periods}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
