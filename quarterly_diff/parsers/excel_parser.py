from abc import ABCMeta, abstractmethod

import xlrd


class CompanyInvestment(object):
    def __init__(self, company_id: str, stake: float):
        self._company_id = company_id
        self._stake = stake

    @property
    def company_id(self):
        return self._company_id

    @property
    def stake(self):
        return self._stake

    def __sub__(self, other) -> CompanyInvestment:
        if other.company_id != self.company_id:
            raise ValueError(f"Different ID's! {self.company_id} != {other.company_id}")
        return CompanyInvestment(company_id=self.company_id, stake=self.stake - other.stake)

    def __add__(self, other) -> CompanyInvestment:
        if other.company_id != self.company_id:
            raise ValueError(f"Different ID's! {self.company_id} != {other.company_id}")
        return CompanyInvestment(company_id=self.company_id, stake=self.stake + other.stake)

    def __repr__(self) -> str:
        return f"<CompanyInvestment: {self._company_id}>"


class ExcelParser(metaclass=ABCMeta):
    @property
    @abstractmethod
    def COMPANIES_START_ROW(self):
        pass

    @property
    @abstractmethod
    def COMPANIES_ID_COL(self):
        pass

    @property
    @abstractmethod
    def STAKE_AT_COMPANY_COL(self):
        pass

    @property
    @abstractmethod
    def STAKE_SHEET_NAME(self):
        pass

    def __init__(self, workbook_path):
        self._workbook = xlrd.open_workbook(workbook_path)
        self._sheet = self._workbook.sheet_by_name(self.STAKE_SHEET_NAME)

    def _get_company_id(self, investment):
        return investment[self.COMPANIES_ID_COL].value

    def _get_stake_at_company(self, investment):
        return investment[self.STAKE_AT_COMPANY_COL].value

    @property
    def _investments_rows(self):
        return (self._sheet.row(index) for index in range(self.COMPANIES_START_ROW, self._sheet.nrows)
                if self._get_company_id(self._sheet.row(index)))

    @property
    def investments(self):
        return (CompanyInvestment(company_id=self._get_company_id(investment),
                                  stake=self._get_stake_at_company(investment)) for investment in
                self._investments_rows)
