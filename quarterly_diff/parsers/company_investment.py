from __future__ import annotations


class CompanyInvestment:
    def __init__(self, company_id: str, stake: float, currency: str = "שקל חדש", company_name: str = ""):
        self._company_id = company_id
        self._stake = stake
        self._currency = currency
        self._company_name = company_name

    @property
    def company_id(self) -> str:
        return self._company_id

    @property
    def company_name(self) -> str:
        return self._company_name

    @property
    def stake(self) -> float:
        return self._stake

    @property
    def currency(self) -> str:
        return self._currency

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

    def __eq__(self, other: CompanyInvestment) -> bool:
        return self.company_id == other.company_id and \
               self.currency == other.currency and \
               self.stake == other.stake and \
               self.company_name == other.company_name

    def __repr__(self) -> str:
        return f"<CompanyInvestment: {self._company_id}>" if not self.company_name else \
            f"<CompanyInvestment: {self.company_name} - {self.company_id}>"
