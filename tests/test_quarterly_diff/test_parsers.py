import os
from pathlib import Path

import pytest
from _pytest.fixtures import FixtureRequest

from quarterly_diff.parsers import ExcelParser

PORTFOLIOS_PATH = Path(os.path.dirname(os.path.realpath(__file__))) / "example_portfolios"


def _get_portfolio_path(company, quarter, year, extension="xlsx"):
    return str(PORTFOLIOS_PATH / f"{company}_{quarter}_{year}.{extension}")


@pytest.fixture
def menora_parser() -> ExcelParser:
    return ExcelParser(_get_portfolio_path(company="menora", quarter=4, year=22))


@pytest.fixture
def harel_parser() -> ExcelParser:
    return ExcelParser(_get_portfolio_path(company="harel", quarter=4, year=22))


@pytest.fixture
def altshuler_parser() -> ExcelParser:
    return ExcelParser(_get_portfolio_path(company="altshuler", quarter=4, year=22))


@pytest.fixture
def phoenix_parser() -> ExcelParser:
    return ExcelParser(_get_portfolio_path(company="phoenix", quarter=4, year=22, extension="xls"))


@pytest.fixture
def clal_gemel_parser() -> ExcelParser:
    return ExcelParser(_get_portfolio_path(company="clal_gemel", quarter=4, year=22))


@pytest.fixture
def clal_pension_parser() -> ExcelParser:
    return ExcelParser(_get_portfolio_path(company="clal_pension", quarter=4, year=22))

@pytest.fixture
def meitav_parser() -> ExcelParser:
    return ExcelParser(_get_portfolio_path(company="meitav", quarter=4, year=22))


@pytest.mark.parametrize(
    ("parser", "investments_amount"),
    [
        ("menora_parser", 51),
        ("harel_parser", 41),
        ("phoenix_parser", 38),
        ("altshuler_parser", 84),
        ("clal_gemel_parser", 42),
        ("clal_pension_parser", 47),
        ("meitav_parser", 5),
    ]
)
def test_investments_amount(parser: str, investments_amount: int, request: FixtureRequest):
    parser: ExcelParser = request.getfixturevalue(parser)
    assert len(list(parser.investments)) == investments_amount
