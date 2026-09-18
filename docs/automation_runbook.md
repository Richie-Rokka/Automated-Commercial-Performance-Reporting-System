# Commercial Reporting Automation Runbook

## Purpose

This automation turns the two prepared business sources into the reporting datasets consumed by the Power BI report.

The automated flow is:

AdventureWorks SQL Server
→ extraction
→ commercial calculations
→ risk-based controls
→ AdventureWorks reporting CSVs

Maven CRM CSV files
→ validation
→ transformation
→ Maven reporting CSVs

Both reporting layers
→ deterministic management recommendation engine
→ `management_recommendations.csv`

Power BI
→ refresh
→ four-page management report

## Python entry point

Run from the project root:

```powershell
python -m src.run_commercial_reporting
```

Or use the Windows launcher:

```text
run_commercial_reporting.bat
```

## Outputs

AdventureWorks:

- `data/reporting/executive_kpis.csv`
- `data/reporting/monthly_performance.csv`
- `data/reporting/category_performance.csv`
- `data/reporting/product_performance.csv`
- `data/reporting/customer_performance.csv`
- `data/reporting/seller_performance.csv`

Maven CRM:

- `data/reporting/executive_pipeline_kpis.csv`
- `data/reporting/stage_performance.csv`
- `data/reporting/regional_performance.csv`
- `data/reporting/sales_agent_performance.csv`
- `data/reporting/product_performance.csv`
- `data/reporting/account_performance.csv`

Management recommendations:

- `data/reporting/management_recommendations.csv`

Execution log:

- `logs/commercial_reporting.log`

## Failure behavior

The pipeline is fail-fast.

A failed source extraction, failed critical control, failed financial reconciliation, invalid recommendation output, or export error stops the run with a non-zero exit code.

This prevents the scheduler from treating an incomplete report as a successful run.

## Controls

AdventureWorks controls include:

- source population is non-empty;
- reporting population matches extracted sales population;
- sales-line identifier is present;
- sales-line identifier is unique;
- revenue is populated;
- revenue is not negative;
- gross profit reconciles to revenue minus cost;
- unresolved reporting costs are zero.

Maven CRM uses the established Maven validation framework before transformation.

Recommendation output controls include:

- exactly five recommendations;
- IDs 1–5;
- all required columns present;
- no null output fields.

## Scheduling

For a local Windows implementation, use Windows Task Scheduler to launch:

```text
run_commercial_reporting.bat
```

Recommended sequence:

1. Confirm SQL Server Express is running.
2. Confirm the Maven source files are present.
3. Run the batch file.
4. Review the exit code/log.
5. Refresh the Power BI semantic model.

## Power BI production automation

The Python process updates the reporting files. Power BI Desktop does not need to be used as the scheduling engine.

For a cloud-delivered automated report, publish the PBIX to Power BI Service and configure scheduled semantic-model refresh. Because the project uses an on-premises SQL Server source, an on-premises data gateway is required for that source. Microsoft documents scheduled refresh and gateway configuration for on-premises sources.

If the Power BI model also reads local CSV files, configure those file sources through the supported gateway/data-source configuration or move the reporting outputs to an appropriate cloud-accessible location.

## Important architecture decision

Python owns:

- extraction;
- transformation;
- validation;
- reporting datasets;
- management recommendation generation.

Power BI owns:

- visualization;
- filtering;
- presentation.

Power BI should not reproduce the Python recommendation logic in DAX.
