from .excel_parser import ExcelParser


class Menora(ExcelParser):
    COMPANIES_START_ROW = 13
    COMPANIES_ID_COL = 5
    CURRENCY_COL = 7
    STAKE_AT_COMPANY_COL = 8
    STAKE_SHEET_NAME = "מניות"
