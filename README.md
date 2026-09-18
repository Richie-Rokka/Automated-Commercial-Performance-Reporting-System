# Automated Commercial Performance Reporting System

**An end-to-end commercial analytics solution for actual sales performance, CRM pipeline visibility, and management decision support.**

Built with Python, SQL Server, Excel, Power BI Desktop, Windows Task Scheduler, and Power Automate Desktop, this project connects data processing and validation with management-ready reporting and a repeatable desktop report-preparation workflow.

[![Python](https://img.shields.io/badge/Python-Data%20Pipeline-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-Data%20Source-CC2927?logo=microsoftsqlserver&logoColor=white)](https://www.microsoft.com/sql-server)
[![Power BI](https://img.shields.io/badge/Power%20BI-Reporting-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Excel](https://img.shields.io/badge/Excel-Reporting-217346?logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/microsoft-365/excel)
[![Power Automate Desktop](https://img.shields.io/badge/Power%20Automate%20Desktop-Workflow-0066FF?logo=powerautomate&logoColor=white)](https://powerautomate.microsoft.com/)
[![pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
![License](https://img.shields.io/badge/License-MIT-green)

[**Power BI report**](reports/Automated_Commercial_Performance_Report.pbix) · [**Executive Excel report**](reports/adventureworks_executive_report.xlsx) 

---

## Project Overview

Commercial teams need a consistent view of historical sales, pipeline activity, and the factors affecting commercial outcomes. This project brings together two distinct data domains:

- **Actual commercial performance:** AdventureWorks sales data.
- **CRM pipeline performance:** Maven CRM opportunities and supporting account, product, and sales-team data.

A Python reporting pipeline extracts and processes the source data, applies validations, creates reporting-ready datasets, and generates observations and management recommendations. Excel and Power BI provide the reporting layer, while Windows Task Scheduler and Power Automate Desktop support repeatable execution and local report preparation.

The project is a portfolio implementation of a practical data-to-decision workflow—not a production-hosted analytics service.

## Business Questions Addressed

| Business area | Reporting focus |
|---|---|
| Executive performance | Revenue, gross profit, margin, and pipeline visibility |
| Commercial trends | Monthly performance and gross-profit movement |
| Product and category | Revenue and profitability patterns |
| Customer and seller | Revenue and gross-profit performance |
| CRM pipeline | Opportunity stages, regions, agents, products, and accounts |
| Management action | Findings and suggested actions related to margin, profitability, pipeline visibility, and prioritization |

## Solution Architecture

The project is organized around a staged data-to-reporting workflow. The 14-stage guide used during development served as a focus and project-control aid; it is not a formal architecture specification.

```text
AdventureWorks actual sales             Maven CRM pipeline
              |                                  |
              v                                  v
       Data access / extraction             Extraction
              |                                  |
              v                                  v
       Transformation / preparation       Standardization
              |                                  |
              v                                  v
            Validation                       Validation
              |                                  |
              +----------------+-----------------+
                               |
                               v
                  Reporting dataset preparation
                               |
                +--------------+----------------+
                |              |                |
                v              v                v
             Excel          Power BI       Observations &
             reports        dashboard      recommendations
                               |
                               v
                    Power Automate Desktop
                    report refresh / save /
                    PDF-export navigation
                               |
                               v
                       Report review
                         and saving
```

The actual execution sequence and transformations are implemented in the Python entry points and source modules.

## Data Sources

### AdventureWorks — actual commercial performance

AdventureWorks is used for historical sales and profitability analysis. The project connects to a locally configured SQL Server database through its AdventureWorks connection module.

### Maven CRM — pipeline performance

The Maven CRM dataset supports prospective pipeline analysis. The project keeps pipeline opportunity data analytically distinct from transaction-level actual sales.

The CRM source includes sales pipeline, accounts, products, sales teams, and a data dictionary.

## Analytics and Reporting Outputs

### AdventureWorks reporting datasets

The `data/reporting/` directory contains outputs for:

- Executive KPIs
- Monthly performance
- Category performance
- Product performance
- Customer performance
- Seller performance
- Key observations
- Management recommendations

### Maven CRM reporting datasets

The `data/reporting/maven_crm/` directory contains outputs for:

- Executive pipeline KPIs
- Stage performance
- Regional performance
- Sales-agent performance
- Product performance
- Account performance

### Excel deliverables

| Deliverable | File |
|---|---|
| Executive report | [`adventureworks_executive_report.xlsx`](reports/adventureworks_executive_report.xlsx) |

The reporting package includes workbook construction, formatting, charts, recommendation content, and export functionality.

## Power BI Dashboard

The Power BI report contains four pages with complementary views of actual commercial performance and CRM pipeline activity.

### 1. Executive Overview

Headline actual-performance and pipeline KPIs, monthly revenue and gross-profit trends, pipeline-stage metrics, and executive commercial observations.

![Executive Overview](docs/screenshots/01_Executive_Overview.png)

### 2. Actual Commercial Performance

Revenue and gross margin by category, top products by revenue, customer revenue versus gross profit, and seller gross-profit performance.

![Actual Commercial Performance](docs/screenshots/02_Actual_Commercial_Performance.png)

### 3. Pipeline Performance

Opportunity volume and closed value by stage, opportunities by region, sales-agent pipeline activity, pipeline value by product, and leading accounts by closed value.

![Pipeline Performance](docs/screenshots/03_Pipeline_Performance.png)

### 4. Management Recommendations

Prioritized findings and suggested actions across gross margin, customer profitability, seller profitability, pipeline visibility, and pipeline prioritization.

![Management Recommendations](docs/screenshots/04_Management_Recommendations.png)

**Power BI file:** [`Automated_Commercial_Performance_Report.pbix`](reports/Automated_Commercial_Performance_Report.pbix)

## Technology Stack

| Technology | Role |
|---|---|
| Python | Pipeline execution, data processing, validation, insights, and report generation |
| pandas | Tabular data preparation and transformation |
| SQL Server | AdventureWorks data source |
| SQLAlchemy / pyodbc | Database connectivity |
| Microsoft Excel | Commercial and executive workbooks |
| Power BI Desktop | Interactive commercial and pipeline reporting |
| Power Automate Desktop | Local desktop report-preparation workflow |
| Windows Task Scheduler | Scheduled execution |
| pytest / unittest | Automated testing |
| Git / GitHub | Version control and portfolio publication |

## Python Pipeline and Execution

Primary entry point:

```text
src/run_commercial_reporting.py
```

The repository also includes dedicated scripts for AdventureWorks reporting and management recommendation generation.

From the project root in Windows PowerShell, activate the project environment and run:

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.run_commercial_reporting
```

Additional entry points:

```powershell
python -m src.generate_adventureworks_report
python -m src.generate_management_recommendations
```

Reproduction requires the appropriate source data, Python dependencies, local database access, and application configuration. Configure the AdventureWorks connection for your own environment rather than copying machine-specific connection settings.

## Validation and Testing

The project includes checks covering database connectivity, dataset definitions, extraction, transformation, validation, Maven CRM processing and export, recommendation logic, and reporting output.

**Latest recorded test result:** 8 tests passed in 15.93 seconds.

The recorded command was:

```powershell
python -m pytest test/ -v
```

The 8-test result specifically covered management-recommendation integration and recommendation logic, output, and export. 

### Recorded data validation

The latest documented pipeline run completed successfully on September 16, 2026, in approximately 4.20 seconds.

AdventureWorks validation recorded:

| Measure | Recorded result |
|---|---:|
| Revenue | ~109,846,381.40 |
| Cost | ~97,288,600.80 |
| Gross profit | ~12,557,780.60 |
| Sales lines | 121,317 |
| Historical-cost fallback rows | 64 |
| Unresolved cost rows | 0 |

Historical cost logic uses inclusive `StartDate` and `EndDate` boundaries.

Maven CRM validation recorded 8,800 opportunities. A total of 1,480 product names were normalized from `GTXPro` to `GTX Pro` before validation; the recorded validations passed.

These are documented project-run results, not a guarantee that a fresh run in another environment will produce identical outputs.

## Power Automate Desktop Workflow

The PAD workflow contains **12 actions** and supports local Power BI report preparation. At a high level, it:

1. Launches Power BI Desktop and opens the PBIX.
2. Waits for the report window.
3. Clicks the configured Refresh control.
4. Waits 30 seconds for refresh processing.
5. Saves the PBIX with `Ctrl+S`.
6. Waits for the save operation.
7. Navigates the PDF-export interface through configured clicks and waits.

The final action is a 10-second wait after the last export-navigation click.

![Power Automate Desktop workflow — screenshot 1](docs/screenshots/PAD1.png)

![Power Automate Desktop workflow — screenshot 2](docs/screenshots/PAD2.png)

### Automation boundary

**The workflow is not fully unattended from end to end.**

- The 30-second refresh delay is fixed; it does not programmatically confirm refresh completion.
- Refresh and export navigation use captured screen coordinates.
- Display scaling, resolution, window position, or Power BI interface changes may require coordinates to be recaptured.
- Report review and saving remain manual.
- Automatic PDF saving, publishing, and distribution are not implemented.
- Automatic correction of data, report logic, or dashboard layout is outside the current scope.

The PAD flow completed a documented fresh-start test, reached the PDF-export stage, and had its PDF page fit adjusted and confirmed. A cyclic-reference issue encountered during development was resolved.

## Repository Structure

```text
Automated Commercial Performance Reporting System/
├── data/
│   ├── raw/
│   └── reporting/
├── docs/
│   ├── adventure_documentation.md
│   ├── automation_runbook.md
│   ├── report_export.md
│   └── screenshots/
├── reports/
│   ├── Automated_Commercial_Performance_Report.pbix
│   ├── adventureworks_commercial_performance_report.xlsx
│   └── adventureworks_executive_report.xlsx
├── src/
│   ├── adventureworks/
│   ├── maven_crm/
│   ├── reporting/
│   ├── generate_adventureworks_report.py
│   ├── generate_management_recommendations.py
│   └── run_commercial_reporting.py
├── test/
├── .gitignore
├── README.md
├── run_commercial_reporting.bat
└── 01_python_environment_check.ipynb
```

## Setup Requirements

To reproduce the workflow, you will need:

- Windows
- Python and a configured project virtual environment
- Required Python packages
- AdventureWorks database access and connection configuration
- Required source datasets
- Microsoft Excel
- Microsoft Power BI Desktop
- Power Automate Desktop, if running the desktop automation

The AdventureWorks connection module uses a locally configured SQL Server connection and Windows authentication. Update local connection settings as appropriate for your environment.

## Documentation

- [AdventureWorks documentation](docs/adventure_documentation.md)
- [Automation runbook](docs/automation_runbook.md)
- [Report export documentation](docs/report_export.md)

## Scope and Limitations

This project demonstrates a local commercial reporting and desktop report-preparation workflow. It does not claim to provide a production-hosted analytics service.

Current boundaries include local database and application dependencies, a fixed refresh wait, coordinate-dependent desktop interactions, and human review and saving. Automatic PDF distribution or publishing and automatic correction of data or report logic are not implemented.

These limitations are stated to distinguish demonstrated capabilities from possible future enhancements.

## Connect

I'm interested in opportunities and conversations around **Business Intelligence, Data Analytics, Commercial Analytics, Revenue Analytics, and Operational Performance**.

**Abodunrin Oketade**

📍 Ontario, Canada
🔗 

<p>
<a href="https://www.linkedin.com/in/abodunrin-oketade">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>

<a href="mailto:aoketade@gmail.com">
<img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white"/>
</a>

<a href="https://github.com/Richie-Rokka">
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github"/>
</a>

</p>

</div>

---

### Turning business data into actionable decisions.
