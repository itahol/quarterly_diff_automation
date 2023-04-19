from .excel_parser import ExcelParser


class Altshuler(ExcelParser):
    COMPANIES_START_ROW = 12
    COMPANY_NAME_COL = 1
    COMPANIES_ID_COL = 4
    CURRENCY_COL = 6
    STAKE_AT_COMPANY_COL = 7
    STAKE_SHEET_NAME = "לא סחיר - מניות"
