from __future__ import annotations
from dataclasses import dataclass, field
from functools import cached_property


@dataclass(eq=True)
class CompanyInvestment:
    name: str = field(compare=False)
    category: str = field(compare=False)
    share_value: float = field(default=0.0, compare=False)  # ערך של יחידה
    securities_id: str = ""
    issuer_id: str = ""
    currency: str = "שקל חדש"
    nominal_value: float = 0.0  # מספר יחידות

    def __post_init__(self):
        self.share_value = round(self.share_value, 2)
        self.nominal_value = round(self.nominal_value, 2)

    def __sub__(self, other: CompanyInvestment) -> CompanyInvestment:
        if other.issuer_id != self.issuer_id:
            raise ValueError(f"Different ID's! {self.issuer_id} != {other.issuer_id}")
        if other.securities_id != self.securities_id:
            raise ValueError(f"Different securities ID's! {self.securities_id} != {other.securities_id}")
        if other.currency != self.currency:
            raise ValueError(f"Different currencies! {self.currency} != {other.currency}")

        return CompanyInvestment(issuer_id=self.issuer_id, nominal_value=self.nominal_value - other.nominal_value,
                                 currency=self.currency, name=self.name, category=self.category,
                                 share_value=self.share_value, securities_id=self.securities_id)

    def __add__(self, other: CompanyInvestment) -> CompanyInvestment:
        if other.issuer_id != self.issuer_id:
            raise ValueError(f"Different ID's! {self.issuer_id} != {other.issuer_id}")
        if other.securities_id != self.securities_id:
            raise ValueError(f"Different securities ID's! {self.securities_id} != {other.securities_id}")
        if other.currency != self.currency:
            raise ValueError(f"Different currencies! {self.currency} != {other.currency}")
        if other.share_value != self.share_value:
            raise ValueError(f"Different share values! {self.share_value} != {other.share_value}")

        return CompanyInvestment(issuer_id=self.issuer_id, nominal_value=self.nominal_value + other.nominal_value,
                                 currency=self.currency, name=self.name, category=self.category,
                                 share_value=self.share_value, securities_id=self.securities_id)

    def __repr__(self) -> str:
        return f"<CompanyInvestment: {self.issuer_id}>" if not self.name else \
            f"<CompanyInvestment: {self.name} - {self.issuer_id}>"

    @cached_property
    def calculated_fair_value(self):
        return self.share_value * self.nominal_value / 100
