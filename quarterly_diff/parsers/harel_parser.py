from .excel_parser import ExcelParser


class Harel(ExcelParser):
    COMPANIES_START_ROW = 13
    COMPANY_NAME_COL = 1
    COMPANIES_ID_COL = 5
    CURRENCY_COL = 7
    STAKE_AT_COMPANY_COL = 8
    STAKE_SHEET_NAME = "מניות"
