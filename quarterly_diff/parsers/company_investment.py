from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(eq=True)
class CompanyInvestment:
    name: str = field(compare=False)
    category: str = field(compare=False)
    issuer_id: str = ""
    currency: str = "שקל חדש"
    stake: float = 0.0

    def __sub__(self, other: CompanyInvestment) -> CompanyInvestment:
        if other.issuer_id != self.issuer_id:
            raise ValueError(f"Different ID's! {self.issuer_id} != {other.issuer_id}")
        if other.currency != self.currency:
            raise ValueError(f"Different currencies! {self.currency} != {other.currency}")

        return CompanyInvestment(issuer_id=self.issuer_id, stake=self.stake - other.stake, currency=self.currency,
                                 name=self.name, category=self.category)

    def __add__(self, other: CompanyInvestment) -> CompanyInvestment:
        if other.issuer_id != self.issuer_id:
            raise ValueError(f"Different ID's! {self.issuer_id} != {other.issuer_id}")
        if other.currency != self.currency:
            raise ValueError(f"Different currencies! {self.currency} != {other.currency}")

        return CompanyInvestment(issuer_id=self.issuer_id, stake=self.stake + other.stake, currency=self.currency,
                                 name=self.name, category=self.category)

    def __repr__(self) -> str:
        return f"<CompanyInvestment: {self.issuer_id}>" if not self.name else \
            f"<CompanyInvestment: {self.name} - {self.issuer_id}>"
