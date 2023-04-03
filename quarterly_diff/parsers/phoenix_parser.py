from .excel_parser import ExcelParser


class Phoenix(ExcelParser):
    COMPANIES_START_ROW = 13
    COMPANIES_ID_COL = 5
    STAKE_AT_COMPANY_COL = 8
    STAKE_SHEET_NAME = "מניות"
