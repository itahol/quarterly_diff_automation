import pytest

from _pytest.fixtures import FixtureRequest
from quarterly_diff.parsers import ExcelParser, Menora, Harel, Altshuler, Phoenix

XLSX_TEMPLATE = "{company}_{quarter}_{year}.xlsx"
XLS_TEMPLATE = "{company}_{quarter}_{year}.xls"


@pytest.fixture
def menora_parser() -> Menora:
    return Menora(XLSX_TEMPLATE.format(company="menora", quarter=4, year=22))


@pytest.fixture
def harel_parser() -> Harel:
    return Harel(XLSX_TEMPLATE.format(company="harel", quarter=4, year=22))


@pytest.fixture
def altshuler_parser() -> Altshuler:
    return Altshuler(XLSX_TEMPLATE.format(company="altshuler", quarter=4, year=22))


@pytest.fixture
def phoenix_parser() -> Phoenix:
    return Phoenix(XLS_TEMPLATE.format(company="phoenix", quarter=4, year=22))


@pytest.mark.parametrize(
    ("parser", "investments_amount"),
    [
        ("menora_parser", 145),
        ("harel_parser", 149),
        ("phoenix_parser", 378),
        ("altshuler_parser", 134),
    ]
)
def test_investments_amount(parser: str, investments_amount: int, request: FixtureRequest):
    parser: ExcelParser = request.getfixturevalue(parser)
    assert len(list(parser.investments)) == investments_amount
