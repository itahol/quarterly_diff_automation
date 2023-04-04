from typing import Tuple

from .parsers import Phoenix, InvestmentPortfolio


def compare_portfolios(prev_quarter_path: str, quarter_path: str) -> Tuple[
        InvestmentPortfolio, InvestmentPortfolio, InvestmentPortfolio]:
    prev_quarter = Phoenix(prev_quarter_path)  # TODO use matching parsers
    quarter = Phoenix(quarter_path)

    new_investments = {}  # type: InvestmentPortfolio
    updated_investments = {}  # type: InvestmentPortfolio
    deprecated_investments = prev_quarter.summed_investments.copy()  # type: InvestmentPortfolio
    for key, investment in quarter.summed_investments.items():
        if key not in prev_quarter.summed_investments:
            new_investments[key] = investment
        elif investment != prev_quarter.summed_investments[key]:
            updated_investments[key] = investment - prev_quarter.summed_investments[key]
        deprecated_investments.pop(key, None)
    return new_investments, updated_investments, deprecated_investments
