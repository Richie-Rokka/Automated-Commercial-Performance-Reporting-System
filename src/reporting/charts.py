from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.text import RichText
from openpyxl.drawing.text import Paragraph
from openpyxl.drawing.text import ParagraphProperties
from openpyxl.drawing.text import CharacterProperties


# =============================================================
# CHART TEXT FORMATTING
# =============================================================


def _set_axis_font(axis, size=800):
    """
    Set the font size for chart axis labels.

    Excel/OpenXML stores font size in 1/100 of a point.

    Examples:
        800  = 8 pt
        900  = 9 pt
        1000 = 10 pt
    """

    axis.txPr = RichText(
        p=[
            Paragraph(
                pPr=ParagraphProperties(
                    defRPr=CharacterProperties(
                        sz=size
                    )
                )
            )
        ]
    )


def _set_data_label_font(labels, size=800):
    """
    Set the font size for chart data labels.

    Default:
        8 pt
    """

    labels.txPr = RichText(
        p=[
            Paragraph(
                pPr=ParagraphProperties(
                    defRPr=CharacterProperties(
                        sz=size
                    )
                )
            )
        ]
    )


# =============================================================
# EXECUTIVE SUMMARY
# =============================================================


def add_revenue_trend_chart(workbook):
    """
    Add the monthly revenue trend chart to the Executive Summary.

    Data source:
        Monthly Performance worksheet.

    Responsibility:
        Presentation only.
    """

    executive_sheet = workbook["Executive Summary"]
    monthly_sheet = workbook["Monthly Performance"]

    chart = LineChart()

    chart.title = "Monthly Revenue Trend"

    revenue_data = Reference(
        monthly_sheet,
        min_col=2,
        min_row=1,
        max_row=monthly_sheet.max_row,
    )

    categories = Reference(
        monthly_sheet,
        min_col=1,
        min_row=2,
        max_row=monthly_sheet.max_row,
    )

    chart.add_data(
        revenue_data,
        titles_from_data=True,
    )

    chart.set_categories(categories)

    chart.height = 7.5
    chart.width = 15

    chart.style = 13

    chart.legend = None

    chart.y_axis.title = "Revenue"
    chart.y_axis.numFmt = '$#,##0.0,,"M"'
    chart.y_axis.majorGridlines = None

    chart.x_axis.title = "Month"

    _set_axis_font(chart.x_axis, 800)
    _set_axis_font(chart.y_axis, 800)

    executive_sheet.add_chart(
        chart,
        "A11",
    )

    return chart


def add_commercial_performance_chart(workbook):
    """
    Add Revenue, Gross Profit and Gross Margin
    to the Executive Summary.
    """

    executive_sheet = workbook["Executive Summary"]
    monthly_sheet = workbook["Monthly Performance"]

    categories = Reference(
        monthly_sheet,
        min_col=1,
        min_row=2,
        max_row=monthly_sheet.max_row,
    )

    primary_chart = BarChart()

    primary_chart.type = "col"
    primary_chart.title = "Commercial Performance"

    revenue_data = Reference(
        monthly_sheet,
        min_col=2,
        min_row=1,
        max_row=monthly_sheet.max_row,
    )

    gross_profit_data = Reference(
        monthly_sheet,
        min_col=4,
        min_row=1,
        max_row=monthly_sheet.max_row,
    )

    primary_chart.add_data(
        revenue_data,
        titles_from_data=True,
    )

    primary_chart.add_data(
        gross_profit_data,
        titles_from_data=True,
    )

    primary_chart.set_categories(categories)

    primary_chart.height = 8
    primary_chart.width = 15

    primary_chart.style = 10

    primary_chart.y_axis.title = "Revenue / Gross Profit"
    primary_chart.y_axis.numFmt = '$#,##0.0,,"M"'
    primary_chart.y_axis.majorGridlines = None

    primary_chart.x_axis.title = "Month"

    margin_chart = LineChart()

    margin_data = Reference(
        monthly_sheet,
        min_col=7,
        min_row=1,
        max_row=monthly_sheet.max_row,
    )

    margin_chart.add_data(
        margin_data,
        titles_from_data=True,
    )

    margin_chart.set_categories(categories)

    margin_chart.y_axis.axId = 200
    margin_chart.y_axis.title = "Gross Margin %"
    margin_chart.y_axis.crosses = "max"
    margin_chart.y_axis.numFmt = '0.0"%"'
    margin_chart.y_axis.majorGridlines = None

    primary_chart += margin_chart

    primary_chart.legend.position = "b"

    _set_axis_font(
        primary_chart.x_axis,
        800,
    )

    _set_axis_font(
        primary_chart.y_axis,
        800,
    )

    executive_sheet.add_chart(
        primary_chart,
        "A26",
    )

    return primary_chart


# =============================================================
# CATEGORY PERFORMANCE
# =============================================================


def add_category_revenue_chart(workbook):
    """
    Add Revenue by Category.
    """

    worksheet = workbook["Category Performance"]

    chart = BarChart()

    revenue_data = Reference(
        worksheet,
        min_col=2,
        min_row=5,
        max_row=9,
    )

    categories = Reference(
        worksheet,
        min_col=1,
        min_row=6,
        max_row=9,
    )

    chart.add_data(
        revenue_data,
        titles_from_data=True,
        from_rows=False,
    )

    chart.set_categories(categories)

    chart.type = "col"
    chart.title = "Revenue by Category"

    chart.height = 7.5
    chart.width = 12

    chart.style = 10

    chart.legend = None

    chart.y_axis.title = "Revenue"
    chart.y_axis.numFmt = '$#,##0.0,,"M"'
    chart.y_axis.majorGridlines = None

    chart.x_axis.title = None
    chart.x_axis.tickLblPos = "none"

    labels = DataLabelList()

    labels.showCatName = True
    labels.showVal = False
    labels.showSerName = False
    labels.showLegendKey = False
    labels.dLblPos = "outEnd"

    _set_data_label_font(labels, 800)

    chart.dLbls = labels

    worksheet.add_chart(
        chart,
        "A12",
    )

    return chart


def add_category_margin_chart(workbook):
    """
    Add Gross Margin by Category.
    """

    worksheet = workbook["Category Performance"]

    chart = BarChart()

    margin_data = Reference(
        worksheet,
        min_col=8,
        min_row=5,
        max_row=9,
    )

    categories = Reference(
        worksheet,
        min_col=1,
        min_row=6,
        max_row=9,
    )

    chart.add_data(
        margin_data,
        titles_from_data=True,
        from_rows=False,
    )

    chart.set_categories(categories)

    chart.type = "col"
    chart.title = "Gross Margin by Category"

    chart.height = 7.5
    chart.width = 12

    chart.style = 10

    chart.legend = None

    chart.y_axis.title = "Gross Margin %"
    chart.y_axis.numFmt = '0.0"%"'
    chart.y_axis.majorGridlines = None

    chart.x_axis.title = None
    chart.x_axis.tickLblPos = "none"

    labels = DataLabelList()

    labels.showCatName = True
    labels.showVal = True
    labels.showSerName = False
    labels.showLegendKey = False
    labels.dLblPos = "outEnd"
    labels.numFmt = '0.0"%"'

    _set_data_label_font(labels, 800)

    chart.dLbls = labels

    worksheet.add_chart(
        chart,
        "G12",
    )

    return chart


# =============================================================
# PRODUCT PERFORMANCE
# =============================================================


def _configure_product_bar_chart(
    chart,
    title,
    value_axis_title,
    value_number_format,
):
    """
    Configure a horizontal Product Performance chart.

    Product IDs are used as category labels.

    The horizontal orientation is intentional:
        - Product IDs are easier to read vertically.
        - Long product names are removed from the chart.
        - Numerical values can sit outside the bars.
    """

    chart.type = "bar"

    chart.title = title

    chart.height = 8.5
    chart.width = 14

    chart.style = 10

    chart.legend = None

    # ---------------------------------------------------------
    # Value axis
    # ---------------------------------------------------------

    chart.x_axis.title = value_axis_title

    chart.x_axis.numFmt = value_number_format

    chart.x_axis.majorGridlines = None

    # ---------------------------------------------------------
    # Product ID axis
    # ---------------------------------------------------------

    chart.y_axis.title = "Product ID"

    chart.y_axis.tickLblPos = "nextTo"

    # Reverse the order so the first table row appears
    # at the top of the chart.
    chart.y_axis.scaling.orientation = "maxMin"

    # Smaller Product ID labels.
    _set_axis_font(
        chart.y_axis,
        800,
    )

    _set_axis_font(
        chart.x_axis,
        800,
    )


def _add_product_value_labels(
    chart,
    number_format,
):
    """
    Display only the numerical value at the end of each bar.

    Product ID is already displayed on the category axis.
    ProductName is intentionally excluded.
    """

    labels = DataLabelList()

    labels.showVal = True

    labels.showCatName = False
    labels.showSerName = False
    labels.showLegendKey = False

    labels.dLblPos = "outEnd"

    labels.numFmt = number_format

    # Small, unobtrusive numerical labels.
    _set_data_label_font(
        labels,
        800,
    )

    chart.dLbls = labels

    return chart


def add_top_products_revenue_chart(workbook):
    """
    Add Top 10 Products by Revenue.

    Chart identity:
        Product ID

    Chart measure:
        Revenue

    Full ProductName remains available in the table.
    """

    worksheet = workbook["Product Performance"]

    chart = BarChart()

    # ---------------------------------------------------------
    # Revenue
    #
    # Row 5 = table header
    # Rows 6–15 = top 10 products
    # ---------------------------------------------------------

    revenue_data = Reference(
        worksheet,
        min_col=5,
        min_row=5,
        max_row=15,
    )

    # ---------------------------------------------------------
    # Product ID
    #
    # ProductID is column A.
    # ---------------------------------------------------------

    product_ids = Reference(
        worksheet,
        min_col=1,
        min_row=6,
        max_row=15,
    )

    chart.add_data(
        revenue_data,
        titles_from_data=True,
        from_rows=False,
    )

    chart.set_categories(
        product_ids
    )

    _configure_product_bar_chart(
        chart,
        title="Top 10 Products by Revenue",
        value_axis_title="Revenue",
        value_number_format='$#,##0.0,,"M"',
    )

    _add_product_value_labels(
        chart,
        '$0.0,,"M"',
    )

    worksheet.add_chart(
        chart,
        "J4",
    )

    return chart


def add_product_margin_risk_chart(workbook):
    """
    Add the lowest-margin products from the top-50
    revenue population.

    Chart identity:
        Product ID

    Chart measure:
        Gross Margin %

    Product names remain in the table.
    """

    worksheet = workbook["Product Performance"]

    chart = BarChart()

    # ---------------------------------------------------------
    # Gross Margin
    #
    # Row 24 = table header
    # Rows 25–34 = 10 lowest-margin products
    # ---------------------------------------------------------

    margin_data = Reference(
        worksheet,
        min_col=8,
        min_row=24,
        max_row=34,
    )

    # ---------------------------------------------------------
    # Product ID
    #
    # ProductID is column A.
    # ---------------------------------------------------------

    product_ids = Reference(
        worksheet,
        min_col=1,
        min_row=25,
        max_row=34,
    )

    chart.add_data(
        margin_data,
        titles_from_data=True,
        from_rows=False,
    )

    chart.set_categories(
        product_ids
    )

    _configure_product_bar_chart(
        chart,
        title="Lowest-Margin Products",
        value_axis_title="Gross Margin %",
        value_number_format='0.0"%"',
    )

    _add_product_value_labels(
        chart,
        '0.0"%"',
    )

    worksheet.add_chart(
        chart,
        "J21",
    )

    return chart


# =============================================================
# CHART GROUPS
# =============================================================


def add_executive_charts(workbook):
    """
    Add all Executive Summary charts.
    """

    add_revenue_trend_chart(workbook)

    add_commercial_performance_chart(workbook)

    return workbook


def add_category_charts(workbook):
    """
    Add all Category Performance charts.
    """

    add_category_revenue_chart(workbook)

    add_category_margin_chart(workbook)

    return workbook


def add_product_charts(workbook):
    """
    Add all Product Performance charts.
    """

    add_top_products_revenue_chart(workbook)

    add_product_margin_risk_chart(workbook)

    return workbook


def add_reporting_charts(workbook):
    """
    Add charts for all report pages currently implemented.
    """

    add_executive_charts(workbook)

    add_category_charts(workbook)

    add_product_charts(workbook)

    return workbook