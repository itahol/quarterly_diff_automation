from __future__ import annotations

import os.path
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Dict, Tuple

import openpyxl
import xlrd

from quarterly_diff.parsers.company_investment import CompanyInvestment

if TYPE_CHECKING:
    from typing import Generator, Callable, Union, Any
    from openpyxl.worksheet.worksheet import Worksheet as XLSXWorksheet
    from openpyxl.worksheet.worksheet import Worksheet as XLSXWorksheet
    from xlrd.sheet import Sheet as XLSWorksheet

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
    def COMPANIES_START_ROW(self):  # pylint: disable=C0103
        pass

    @property
    @abstractmethod
    def COMPANY_NAME_COL(self):  # pylint: disable=C0103
        pass

    @property
    @abstractmethod
    def COMPANIES_ID_COL(self):  # pylint: disable=C0103
        pass

    @property
    @abstractmethod
    def STAKE_AT_COMPANY_COL(self):  # pylint: disable=C0103
        pass

    @property
    @abstractmethod
    def CURRENCY_COL(self):  # pylint: disable=C0103
        pass

    @property
    @abstractmethod
    def STAKE_SHEET_NAME(self):  # pylint: disable=C0103
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
        if self._file_ext == ".xlsx":
            return _get_rows_from_xlsx(self._sheet, self.COMPANIES_START_ROW, self._sheet.max_row, self._get_company_id)
        raise ValueError(f"No defined way to extract rows from {self._file_ext} file")

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
