from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    PatternFill,
    Side,
)


# =============================================================
# REPORT THEME
# =============================================================

NAVY = "17365D"
BLUE = "2F75B5"
LIGHT_BLUE = "D9EAF7"
LIGHT_GRAY = "F2F2F2"
MEDIUM_GRAY = "D9E1F2"
DARK_GRAY = "595959"
WHITE = "FFFFFF"
BLACK = "000000"
RED = "C00000"
LIGHT_RED = "FCE4D6"
GREEN = "548235"
LIGHT_GREEN = "E2F0D9"


THIN_GRAY_BORDER = Border(
    bottom=Side(
        style="thin",
        color=MEDIUM_GRAY,
    )
)


def apply_title_style(cell):
    cell.font = Font(
        name="Aptos Display",
        size=20,
        bold=True,
        color=NAVY,
    )

    cell.alignment = Alignment(
        horizontal="left",
        vertical="center",
    )


def apply_subtitle_style(cell):
    cell.font = Font(
        name="Aptos",
        size=10,
        italic=True,
        color=DARK_GRAY,
    )

    cell.alignment = Alignment(
        horizontal="left",
        vertical="center",
    )


def apply_section_header_style(cell):
    cell.fill = PatternFill(
        fill_type="solid",
        fgColor=NAVY,
    )

    cell.font = Font(
        name="Aptos",
        size=10,
        bold=True,
        color=WHITE,
    )

    cell.alignment = Alignment(
        horizontal="left",
        vertical="center",
    )


def apply_kpi_label_style(cell):
    cell.font = Font(
        name="Aptos",
        size=9,
        bold=True,
        color=DARK_GRAY,
    )

    cell.alignment = Alignment(
        horizontal="center",
        vertical="center",
    )


def apply_kpi_value_style(cell):
    cell.font = Font(
        name="Aptos",
        size=16,
        bold=True,
        color=NAVY,
    )

    cell.alignment = Alignment(
        horizontal="center",
        vertical="center",
    )


def apply_table_header_style(cell):
    cell.fill = PatternFill(
        fill_type="solid",
        fgColor=NAVY,
    )

    cell.font = Font(
        name="Aptos",
        size=9,
        bold=True,
        color=WHITE,
    )

    cell.alignment = Alignment(
        horizontal="center",
        vertical="center",
        wrap_text=True,
    )


def apply_table_body_style(cell):
    cell.font = Font(
        name="Aptos",
        size=9,
        color=BLACK,
    )

    cell.alignment = Alignment(
        vertical="center",
    )

    cell.border = THIN_GRAY_BORDER


def format_currency_column(
    worksheet,
    column_number,
    start_row=2,
):
    for row in range(
        start_row,
        worksheet.max_row + 1,
    ):
        worksheet.cell(
            row=row,
            column=column_number,
        ).number_format = '$#,##0.00'


def format_percentage_column(
    worksheet,
    column_number,
    start_row=2,
):
    for row in range(
        start_row,
        worksheet.max_row + 1,
    ):
        worksheet.cell(
            row=row,
            column=column_number,
        ).number_format = '0.00"%"'


def format_integer_column(
    worksheet,
    column_number,
    start_row=2,
):
    for row in range(
        start_row,
        worksheet.max_row + 1,
    ):
        worksheet.cell(
            row=row,
            column=column_number,
        ).number_format = '#,##0'


def format_executive_summary(workbook):
    worksheet = workbook["Executive Summary"]

    worksheet.merge_cells("A1:F1")
    apply_title_style(worksheet["A1"])

    worksheet.merge_cells("A2:F2")
    apply_subtitle_style(worksheet["A2"])

    for cell_reference in [
        "A4",
        "C4",
        "E4",
        "A7",
        "C7",
        "E7",
    ]:
        apply_kpi_label_style(
            worksheet[cell_reference]
        )

    for cell_reference in [
        "A5",
        "C5",
        "E5",
        "A8",
        "C8",
        "E8",
    ]:
        apply_kpi_value_style(
            worksheet[cell_reference]
        )

    worksheet["A5"].number_format = '$#,##0.00,,"M"'
    worksheet["C5"].number_format = '$#,##0.00,,"M"'
    worksheet["E5"].number_format = '0.00"%"'

    worksheet["A8"].number_format = '#,##0'
    worksheet["C8"].number_format = '#,##0'
    worksheet["E8"].number_format = '#,##0'

    for cell_reference in [
        "A10",
        "A25",
        "A40",
    ]:
        apply_section_header_style(
            worksheet[cell_reference]
        )

    worksheet.merge_cells("A10:F10")
    worksheet.merge_cells("A25:F25")
    worksheet.merge_cells("A40:F40")

    for row in range(
        41,
        worksheet.max_row + 1,
    ):
        cell = worksheet.cell(
            row=row,
            column=1,
        )

        cell.font = Font(
            name="Aptos",
            size=9,
            color=BLACK,
        )

        cell.alignment = Alignment(
            horizontal="left",
            vertical="center",
            wrap_text=True,
        )

    widths = {
        "A": 18,
        "B": 4,
        "C": 18,
        "D": 4,
        "E": 18,
        "F": 4,
    }

    for column, width in widths.items():
        worksheet.column_dimensions[column].width = width

    worksheet.sheet_view.showGridLines = False

    return worksheet


def format_category_performance(workbook):
    worksheet = workbook["Category Performance"]

    worksheet.merge_cells("A1:I1")
    apply_title_style(worksheet["A1"])

    worksheet.merge_cells("A2:I2")
    apply_subtitle_style(worksheet["A2"])

    worksheet.merge_cells("A4:I4")
    apply_section_header_style(worksheet["A4"])

    for column_number in range(1, 10):
        apply_table_header_style(
            worksheet.cell(
                row=5,
                column=column_number,
            )
        )

    for row in worksheet.iter_rows(
        min_row=6,
        max_row=worksheet.max_row,
        min_col=1,
        max_col=9,
    ):
        for cell in row:
            apply_table_body_style(cell)

    for column_number in [2, 3, 4]:
        format_currency_column(
            worksheet,
            column_number,
            start_row=6,
        )

    for column_number in [5, 6, 7]:
        format_integer_column(
            worksheet,
            column_number,
            start_row=6,
        )

    for column_number in [8, 9]:
        format_percentage_column(
            worksheet,
            column_number,
            start_row=6,
        )

    widths = {
        "A": 20,
        "B": 16,
        "C": 16,
        "D": 16,
        "E": 12,
        "F": 12,
        "G": 12,
        "H": 16,
        "I": 16,
    }

    for column, width in widths.items():
        worksheet.column_dimensions[column].width = width

    worksheet.sheet_view.showGridLines = False

    return worksheet


def format_product_performance(workbook):
    """
    Format the Product Performance management page.
    """

    worksheet = workbook["Product Performance"]

    # ---------------------------------------------------------
    # Page title
    # ---------------------------------------------------------

    worksheet.merge_cells("A1:H1")

    apply_title_style(
        worksheet["A1"]
    )

    # ---------------------------------------------------------
    # Subtitle
    # ---------------------------------------------------------

    worksheet.merge_cells("A2:H2")

    apply_subtitle_style(
        worksheet["A2"]
    )

    # ---------------------------------------------------------
    # Section 1
    # ---------------------------------------------------------

    worksheet.merge_cells("A4:H4")

    apply_section_header_style(
        worksheet["A4"]
    )

    for column_number in range(1, 9):
        apply_table_header_style(
            worksheet.cell(
                row=5,
                column=column_number,
            )
        )

    top_product_end_row = 5 + 15

    for row in worksheet.iter_rows(
        min_row=6,
        max_row=top_product_end_row,
        min_col=1,
        max_col=8,
    ):
        for cell in row:
            apply_table_body_style(cell)

    # ---------------------------------------------------------
    # Top-product number formats
    #
    # A = ProductID
    # E = Revenue
    # F = GrossProfit
    # G = Units
    # H = GrossMarginPct
    # ---------------------------------------------------------

    format_integer_column(
        worksheet,
        column_number=1,
        start_row=6,
    )

    format_currency_column(
        worksheet,
        column_number=5,
        start_row=6,
    )

    format_currency_column(
        worksheet,
        column_number=6,
        start_row=6,
    )

    format_integer_column(
        worksheet,
        column_number=7,
        start_row=6,
    )

    format_percentage_column(
        worksheet,
        column_number=8,
        start_row=6,
    )

    # ---------------------------------------------------------
    # Section 2
    # ---------------------------------------------------------

    risk_start_row = 23
    risk_header_row = 24
    risk_data_start_row = 25

    worksheet.merge_cells(
        start_row=risk_start_row,
        start_column=1,
        end_row=risk_start_row,
        end_column=8,
    )

    apply_section_header_style(
        worksheet.cell(
            row=risk_start_row,
            column=1,
        )
    )

    for column_number in range(1, 9):
        apply_table_header_style(
            worksheet.cell(
                row=risk_header_row,
                column=column_number,
            )
        )

    # The margin-risk dataset contains at most 10 rows.
    risk_end_row = min(
        worksheet.max_row,
        risk_data_start_row + 10 - 1,
    )

    for row in worksheet.iter_rows(
        min_row=risk_data_start_row,
        max_row=risk_end_row,
        min_col=1,
        max_col=8,
    ):
        for cell in row:
            apply_table_body_style(cell)

    format_integer_column(
        worksheet,
        column_number=1,
        start_row=risk_data_start_row,
    )

    format_currency_column(
        worksheet,
        column_number=5,
        start_row=risk_data_start_row,
    )

    format_currency_column(
        worksheet,
        column_number=6,
        start_row=risk_data_start_row,
    )

    format_integer_column(
        worksheet,
        column_number=7,
        start_row=risk_data_start_row,
    )

    format_percentage_column(
        worksheet,
        column_number=8,
        start_row=risk_data_start_row,
    )

    # ---------------------------------------------------------
    # Highlight negative/low margins
    # ---------------------------------------------------------

    for row in range(
        risk_data_start_row,
        risk_end_row + 1,
    ):
        margin_cell = worksheet.cell(
            row=row,
            column=8,
        )

        if (
            isinstance(
                margin_cell.value,
                (int, float),
            )
            and margin_cell.value < 0
        ):
            margin_cell.font = Font(
                name="Aptos",
                size=9,
                bold=True,
                color=RED,
            )

            margin_cell.fill = PatternFill(
                fill_type="solid",
                fgColor=LIGHT_RED,
            )

    # ---------------------------------------------------------
    # Column widths
    # ---------------------------------------------------------

    widths = {
        "A": 12,
        "B": 34,
        "C": 18,
        "D": 24,
        "E": 17,
        "F": 17,
        "G": 12,
        "H": 17,
    }

    for column, width in widths.items():
        worksheet.column_dimensions[column].width = width

    worksheet.freeze_panes = "A6"
    worksheet.sheet_view.showGridLines = False

    return worksheet


def format_data_sheet(
    worksheet,
    currency_columns=None,
    percentage_columns=None,
    integer_columns=None,
):
    currency_columns = currency_columns or []
    percentage_columns = percentage_columns or []
    integer_columns = integer_columns or []

    for cell in worksheet[1]:
        apply_table_header_style(cell)

    for row in worksheet.iter_rows(
        min_row=2,
        max_row=worksheet.max_row,
    ):
        for cell in row:
            apply_table_body_style(cell)

    for column_number in currency_columns:
        format_currency_column(
            worksheet,
            column_number,
        )

    for column_number in percentage_columns:
        format_percentage_column(
            worksheet,
            column_number,
        )

    for column_number in integer_columns:
        format_integer_column(
            worksheet,
            column_number,
        )

    worksheet.freeze_panes = "A2"
    worksheet.sheet_view.showGridLines = False

    return worksheet


def apply_negative_margin_formatting(
    worksheet,
    margin_column_number,
    start_row=2,
):
    """
    Highlight negative gross-margin values.
    """

    for row in range(
        start_row,
        worksheet.max_row + 1,
    ):
        cell = worksheet.cell(
            row=row,
            column=margin_column_number,
        )

        if (
            isinstance(
                cell.value,
                (int, float),
            )
            and cell.value < 0
        ):
            cell.font = Font(
                name="Aptos",
                size=9,
                bold=True,
                color=RED,
            )

            cell.fill = PatternFill(
                fill_type="solid",
                fgColor=LIGHT_RED,
            )


def format_report_workbook(workbook):
    """
    Apply all report formatting currently implemented.
    """

    format_executive_summary(
        workbook
    )

    monthly = workbook["Monthly Performance"]

    format_data_sheet(
        monthly,
        currency_columns=[
            2,
            3,
            4,
        ],
        percentage_columns=[
            7,
            8,
            9,
        ],
        integer_columns=[
            5,
            6,
        ],
    )

    apply_negative_margin_formatting(
        monthly,
        margin_column_number=7,
    )

    format_category_performance(
        workbook
    )

    apply_negative_margin_formatting(
        workbook["Category Performance"],
        margin_column_number=8,
        start_row=6,
    )

    format_product_performance(
        workbook
    )

    customer = workbook["Customer Performance"]

    format_data_sheet(
        customer,
        currency_columns=[
            4,
            5,
            6,
        ],
        percentage_columns=[
            10,
        ],
        integer_columns=[
            1,
            7,
            8,
            9,
        ],
    )

    apply_negative_margin_formatting(
        customer,
        margin_column_number=10,
    )

    seller = workbook["Seller Performance"]

    format_data_sheet(
        seller,
        currency_columns=[
            3,
            4,
            5,
        ],
        percentage_columns=[
            9,
        ],
        integer_columns=[
            1,
            6,
            7,
            8,
        ],
    )

    apply_negative_margin_formatting(
        seller,
        margin_column_number=9,
    )

    return workbook