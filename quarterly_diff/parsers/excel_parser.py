from __future__ import annotations

import os.path
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Dict, Tuple

import openpyxl
import xlrd

if TYPE_CHECKING:
    from typing import Generator, Callable, Union, Any
    from openpyxl.worksheet.worksheet import Worksheet as XLSXWorksheet
    from openpyxl.worksheet.worksheet import Worksheet as XLSXWorksheet
    from xlrd.sheet import Sheet as XLSWorksheet


class CompanyInvestment(object):
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
        elif other.currency != self.currency:
            raise ValueError(f"Different currencies! {self.currency} != {other.currency}")

        return CompanyInvestment(company_id=self.company_id, stake=self.stake - other.stake, currency=self.currency,
                                 company_name=self.company_name)

    def __add__(self, other: CompanyInvestment) -> CompanyInvestment:
        if other.company_id != self.company_id:
            raise ValueError(f"Different ID's! {self.company_id} != {other.company_id}")
        elif other.currency != self.currency:
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


InvestmentPortfolio = Dict[Tuple[str, str], CompanyInvestment]


def _get_rows_from_xls(
        sheet: XLSWorksheet,
        start_index: int,
        end_index: int,
        condition_func: Callable[[Union[list, tuple]], Any]) -> Generator[list, None, None]:
    return (sheet.row(index) for index in range(start_index, end_index) if condition_func(sheet.row(index)))


def _get_rows_from_xlsx(sheet: XLSXWorksheet,
                        start_index: int,
                        end_index: int,
                        condition_func: Callable[[Union[list, tuple]], Any]) -> Generator[list, None, None]:
    return (row for row in sheet.iter_rows(min_row=start_index, max_row=end_index) if condition_func(row))


class ExcelParser(metaclass=ABCMeta):
    @property
    @abstractmethod
    def COMPANIES_START_ROW(self):
        pass

    @property
    @abstractmethod
    def COMPANY_NAME_COL(self):
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
    def CURRENCY_COL(self):
        pass

    @property
    @abstractmethod
    def STAKE_SHEET_NAME(self):
        pass

    EXT_TO_LIB = {
        ".xlsx": openpyxl,
        ".xls": xlrd,
    }

    def __init__(self, workbook_path):
        self._file_ext = os.path.splitext(workbook_path)[-1]
        if self._file_ext == ".xls":
            self._workbook = xlrd.open_workbook(workbook_path)
            self._sheet = self._workbook.sheet_by_name(self.STAKE_SHEET_NAME)  # type: XLSWorksheet
        elif self._file_ext == ".xlsx":
            self._workbook = openpyxl.load_workbook(workbook_path)
            self._sheet = self._workbook[self.STAKE_SHEET_NAME]  # type: XLSXWorksheet
        else:
            raise ValueError(f"Only .xls and .xlsx files are supported - a {self._file_ext} file was provided")

    def _get_company_id(self, investment: list) -> str:
        return investment[self.COMPANIES_ID_COL].value.strip() if isinstance(investment[self.COMPANIES_ID_COL].value,
                                                                             str) \
            else investment[self.COMPANIES_ID_COL].value

    def _get_stake_at_company(self, investment: list) -> float:
        return investment[self.STAKE_AT_COMPANY_COL].value

    def _get_currency(self, investment: list) -> str:
        return investment[self.CURRENCY_COL].value

    def _get_company_name(self, investment: list) -> str:
        return investment[self.COMPANY_NAME_COL].value

    @property
    def _investments_rows(self) -> Generator[list, None, None]:
        if self._file_ext == ".xls":
            return _get_rows_from_xls(self._sheet, self.COMPANIES_START_ROW, self._sheet.nrows, self._get_company_id)
        elif self._file_ext == ".xlsx":
            return _get_rows_from_xlsx(self._sheet, self.COMPANIES_START_ROW, self._sheet.max_row, self._get_company_id)

    @property
    def investments(self) -> Generator[CompanyInvestment, None, None]:
        return (CompanyInvestment(company_id=self._get_company_id(investment),
                                  stake=self._get_stake_at_company(investment),
                                  currency=self._get_currency(investment),
                                  company_name=self._get_company_name(investment)) for investment in
                self._investments_rows)

    @property
    def summed_investments(self) -> InvestmentPortfolio:
        companies_dict = {}
        for investment in self.investments:
            companies_dict[(investment.company_id, investment.currency)] = companies_dict.get(
                (investment.company_id, investment.currency),
                CompanyInvestment(
                    company_id=investment.company_id,
                    stake=0,
                    currency=investment.currency,
                    company_name=investment.company_name)) + investment
        return companies_dict
