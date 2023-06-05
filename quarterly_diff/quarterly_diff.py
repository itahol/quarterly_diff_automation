from typing import Tuple

from .parsers import ExcelParser, InvestmentPortfolio


def compare_portfolios(prev_quarter_path: str, quarter_path: str) -> Tuple[
        InvestmentPortfolio, InvestmentPortfolio, InvestmentPortfolio]:
    prev_quarter = ExcelParser(prev_quarter_path)  # TODO use matching parsers
    quarter = ExcelParser(quarter_path)

    new_investments = {}  # type: InvestmentPortfolio
    updated_investments = {}  # type: InvestmentPortfolio
    deprecated_investments = prev_quarter.summed_investments.copy()  # type: InvestmentPortfolio

    for key, investment in quarter.summed_investments.items():
        if key not in prev_quarter.summed_investments:  # New investment
            new_investments[key] = investment
        elif investment.nominal_value != prev_quarter.summed_investments[key].nominal_value:
            # Updated investment - nominal value changed
            updated_investments[key] = investment - prev_quarter.summed_investments[key]
        deprecated_investments.pop(key, None)
    return new_investments, updated_investments, deprecated_investments
