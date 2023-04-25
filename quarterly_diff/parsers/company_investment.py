from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(eq=True)
class CompanyInvestment:
    company_name: str = field(compare=False)
    company_id: str = ""
    currency: str = "שקל חדש"
    stake: float = 0.0

    def __sub__(self, other: CompanyInvestment) -> CompanyInvestment:
        if other.company_id != self.company_id:
            raise ValueError(f"Different ID's! {self.company_id} != {other.company_id}")
        if other.currency != self.currency:
            raise ValueError(f"Different currencies! {self.currency} != {other.currency}")

        return CompanyInvestment(company_id=self.company_id, stake=self.stake - other.stake, currency=self.currency,
                                 company_name=self.company_name)

    def __add__(self, other: CompanyInvestment) -> CompanyInvestment:
        if other.company_id != self.company_id:
            raise ValueError(f"Different ID's! {self.company_id} != {other.company_id}")
        if other.currency != self.currency:
            raise ValueError(f"Different currencies! {self.currency} != {other.currency}")

        return CompanyInvestment(company_id=self.company_id, stake=self.stake + other.stake, currency=self.currency,
                                 company_name=self.company_name)

    def __repr__(self) -> str:
        return f"<CompanyInvestment: {self.company_id}>" if not self.company_name else \
            f"<CompanyInvestment: {self.company_name} - {self.company_id}>"
