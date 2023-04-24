import os
from pathlib import Path

import pytest
from _pytest.fixtures import FixtureRequest

from quarterly_diff.parsers import ExcelParser, Menora, Harel, Altshuler, Phoenix

PORTFOLIOS_PATH = Path(os.path.dirname(os.path.realpath(__file__))) / "example_portfolios"


def _get_portfolio_path(company, quarter, year, extension="xlsx"):
    return str(PORTFOLIOS_PATH / f"{company}_{quarter}_{year}.{extension}")


@pytest.fixture
def menora_parser() -> Menora:
    return Menora(_get_portfolio_path(company="menora", quarter=4, year=22))


@pytest.fixture
def harel_parser() -> Harel:
    return Harel(_get_portfolio_path(company="harel", quarter=4, year=22))


@pytest.fixture
def altshuler_parser() -> Altshuler:
    return Altshuler(_get_portfolio_path(company="altshuler", quarter=4, year=22))


@pytest.fixture
def phoenix_parser() -> Phoenix:
    return Phoenix(_get_portfolio_path(company="phoenix", quarter=4, year=22, extension="xls"))


@pytest.mark.parametrize(
    ("parser", "investments_amount"),
    [
        ("menora_parser", 51),
        ("harel_parser", 41),
        ("phoenix_parser", 38),
        ("altshuler_parser", 84),
    ]
)
def test_investments_amount(parser: str, investments_amount: int, request: FixtureRequest):
    parser: ExcelParser = request.getfixturevalue(parser)
    assert len(list(parser.investments)) == investments_amount
