# Automated Commercial Performance Reporting System

**An end-to-end commercial analytics solution for actual sales performance, CRM pipeline visibility, and management decision support.**

Built with Python, SQL Server, Excel, Power BI, and Power Automate Desktop, this project brings commercial data through a repeatable reporting workflow—from extraction and validation to executive reporting and management recommendations.

[**View the Power BI Report**](reports/Automated_Commercial_Performance_Report.pbix) · [**Executive Excel Report**](reports/adventureworks_executive_report.xlsx) · 

---

## Executive Overview

Commercial teams need consistent visibility into historical performance, sales pipeline activity, and the factors affecting commercial outcomes.

This project demonstrates an integrated reporting workflow that combines:

* **Actual commercial performance** using AdventureWorks sales data.
* **CRM pipeline performance** using Maven CRM data.
* **Management observations and recommendations** derived from analytical outputs.
* **Executive reporting** through Excel workbooks and a four-page Power BI report.
* **Repeatable execution** through a Python reporting pipeline and Windows Task Scheduler.
* **Desktop report preparation** through a tested Power Automate Desktop workflow.

The result is a portfolio implementation connecting data processing, commercial analytics, reporting, and operational workflow automation.

## Business Questions Addressed

| Business area         | Reporting focus                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| Executive performance | Revenue, gross profit, margin, and pipeline visibility                                                 |
| Commercial trends     | Monthly performance and gross-profit movement                                                          |
| Product and category  | Revenue and profitability patterns                                                                     |
| Customer and seller   | Revenue and gross-profit performance                                                                   |
| CRM pipeline          | Opportunity stages, regions, agents, products, and accounts                                            |
| Management action     | Observations and recommendations across margin, profitability, pipeline visibility, and prioritization |

---

## Power BI Dashboard

**Four report pages provide complementary views of commercial performance.**

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

---

## Solution Architecture

The project follows a staged data-to-reporting workflow:

```text
AdventureWorks                    Maven CRM
     |                                |
     v                                v
Connection / Extraction          Extraction
     |                                |
     v                                v
Transformation                  Standardization
     |                                |
     v                                v
Validation                      Validation
     |                                |
     +---------------+----------------+
                     |
                     v
          Reporting Dataset Preparation
                     |
          +----------+-----------+
          |          |           |
          v          v           v
       Excel      Power BI    Management
      Reports     Dashboard   Recommendations
                     |
                     v
              PAD Report Preparation
                     |
                     v
             Human PDF Review / Save
```

The Python implementation is organized into dedicated AdventureWorks, Maven CRM, and reporting modules. The exact execution sequence and transformations are implemented in the source code and entry points.

---

## Analytics and Reporting Deliverables

### AdventureWorks — Actual Commercial Performance

Reporting datasets include:

* Executive KPIs
* Monthly performance
* Category performance
* Product performance
* Customer performance
* Seller performance
* Key observations
* Management recommendations

### Maven CRM — Pipeline Performance

Reporting datasets include:

* Executive pipeline KPIs
* Stage performance
* Regional performance
* Sales-agent performance
* Product performance
* Account performance

### Excel reports

| Deliverable                   | File                                                                                                             |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Executive report              | [`adventureworks_executive_report.xlsx`](reports/adventureworks_executive_report.xlsx)                           |
| Commercial performance report | [`adventureworks_commercial_performance_report.xlsx`](reports/adventureworks_commercial_performance_report.xlsx) |

The reporting package includes chart creation, formatting, recommendation content, workbook construction, and export functionality.

---

## Technology Stack

| Technology             | Role                                                                             |
| ---------------------- | -------------------------------------------------------------------------------- |
| Python                 | Pipeline execution, data processing, validation, insights, and report generation |
| pandas                 | Tabular data preparation and transformation                                      |
| SQL Server             | AdventureWorks data source                                                       |
| SQLAlchemy / pyodbc    | Database connectivity                                                            |
| Microsoft Excel        | Commercial and executive workbooks                                               |
| Power BI Desktop       | Interactive commercial performance and pipeline reporting                        |
| Power Automate Desktop | Desktop report preparation workflow                                              |
| pytest / unittest      | Automated testing                                                                |
| Git / GitHub           | Version control and portfolio publication                                        |

---

## Python Pipeline and Execution

The primary reporting entry point is:

```text
src/run_commercial_reporting.py
```

The project also includes dedicated scripts for AdventureWorks reporting and management recommendation generation.

### Run the reporting workflow

From the project root in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.run_commercial_reporting
```

Additional entry points:

```powershell
python -m src.generate_adventureworks_report
python -m src.generate_management_recommendations
```

The project uses a local AdventureWorks SQL Server connection. To reproduce the workflow, configure the required database, source data, Python environment, and application dependencies for your own machine.

---

## Validation and Testing

### Python tests

The test suite includes checks covering:

* Database connection
* Dataset definitions
* Extraction
* Transformation
* Validation
* Maven CRM datasets, processing, and export
* Recommendation logic
* Reporting export and workbook generation
* Management-recommendation integration

**Latest recorded test result:** 8 tests passed in 15.93 seconds.

The recorded run used:

```powershell
python -m pytest test/ -v
```

The 8 passing tests were for management-recommendation integration and recommendation logic/output/export. This result should not be interpreted as evidence that every module in the repository is covered by those 8 tests.

### Power BI and PAD validation

The PAD workflow completed a fresh-start end-to-end test. The report refresh action was confirmed, the flow reached the PDF export stage, and PDF page fit was adjusted and confirmed.

The cyclic-reference issue encountered during development has been resolved.

---

## Desktop Reporting Automation

The Power Automate Desktop flow contains **12 actions** and prepares the Power BI report for PDF review.

Current workflow:

1. Launch Power BI Desktop and open the PBIX.
2. Wait for the report window.
3. Click the configured Refresh control.
4. Wait 30 seconds for refresh processing.
5. Save the PBIX using `Ctrl+S`.
6. Wait for the save operation.
7. Navigate through the PDF export interface using configured screen-coordinate clicks and waits.

The final action is a 10-second wait after the last export-navigation click.

### Automation boundary

**The workflow is not fully unattended from end to end.**

* The 30-second refresh delay is fixed; it does not guarantee that every refresh has completed.
* Refresh and export navigation use captured screen coordinates.
* Display scaling, resolution, window position, or Power BI interface changes may require coordinates to be recaptured.
* The flow does not independently verify the correctness of every business metric or source record.
* PDF review and saving remain manual.
* Automatic PDF saving, publishing, and distribution are not implemented.
* Automatic correction of data, report logic, or dashboard layout is outside the current scope.

### PAD screenshots

![Power Automate Desktop workflow — screenshot 1](docs/screenshots/PAD1.png)

![Power Automate Desktop workflow — screenshot 2](docs/screenshots/PAD2.png)

---

## Repository Structure

```text
Automated Commercial Performance Reporting System/
├── data/
│   ├── raw/
│   └── reporting/
├── docs/
│   ├── adventure_documentation.md
│   ├── automation_runbook.md
│   ├── generate_adventureworks_copy.py
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

---

## Setup Requirements

To reproduce the workflow, you will need:

* Windows
* Python and a configured project virtual environment
* Required Python packages
* AdventureWorks database access and connection configuration
* Required source datasets
* Microsoft Excel
* Microsoft Power BI Desktop
* Power Automate Desktop, if running the desktop automation

The AdventureWorks connection module currently uses a local SQL Server instance and Windows authentication. Update local connection settings as appropriate for your environment.

---

## Documentation

* [AdventureWorks documentation](docs/adventure_documentation.md)
* [Automation runbook](docs/automation_runbook.md)
* [Report export documentation](docs/report_export.md)

---

## Project Scope and Limitations

This project demonstrates a commercial reporting and desktop report-preparation workflow. It does not claim to provide a production-hosted analytics service.

Current boundaries include:

* Local database and application dependencies.
* A fixed PAD refresh wait rather than programmatic refresh-completion detection.
* Coordinate-dependent desktop interactions.
* Manual PDF review and saving.
* No automatic PDF distribution or publishing.
* No automatic correction of data or report logic.

These boundaries are documented so that the demonstrated capabilities remain distinct from potential future enhancements.

---

## Project Deliverables at a Glance

* Python extraction, transformation, and validation modules for AdventureWorks and Maven CRM.
* Reporting-ready datasets for actual commercial performance and CRM pipeline analytics.
* Excel commercial and executive reports.
* Four-page Power BI commercial performance report.
* Management observations and recommendations.
* Scheduled Python pipeline execution.
* Tested PAD workflow for report refresh and PDF-export preparation.
* Documentation, screenshots, and automated tests.

---

**Author:** Abodunrin Oketade
**GitHub:** [Richie-Rokka](https://github.com/Richie-Rokka)
