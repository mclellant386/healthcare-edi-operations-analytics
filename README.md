# Healthcare EDI Operations Report Automation & Tableau Dashboard

An end-to-end healthcare EDI operations analytics project that uses Python to generate synthetic transaction data, analyze operational performance, create Excel reports, and visualize key performance indicators in an interactive Tableau dashboard.

The project simulates the type of transaction monitoring, issue investigation, SLA analysis, and operational reporting performed by healthcare EDI operations and technical analyst teams.

## Dashboard Preview

[EDI Operations Performance Dashboard](images/EDI Ops Dashboard.png)

### View the Interactive Dashboard

[View the Interactive Tableau Dashboard](https://public.tableau.com/views/EDIOperationsPerformanceDashboard/EDIOperationsPerformanceDashboard?:language=en-US&:sid=&:redirect=auth&publish=yes&showOnboarding=true&:display_count=n&:origin=viz_share_link)

## Project Overview

Healthcare EDI operations teams monitor large volumes of electronic transactions and investigate issues that can affect successful processing.

This project creates a synthetic healthcare claims dataset containing operational scenarios such as transaction rejections, payer routing issues, submitter data errors, processing latency, and SLA breaches.

A Python-based reporting pipeline processes the data and produces analytical outputs that are visualized in Tableau.

### Workflow

Synthetic EDI Transaction Data
→ Python Data Generation
→ Operational Analysis
→ Excel Reporting
→ Automated Pipeline Execution
→ Interactive Tableau Dashboard

## Key Features

- Generates synthetic healthcare EDI transaction data for operational analysis.
- Simulates claim acceptance, rejection, acknowledgment, and processing scenarios.
- Categorizes transaction errors including provider identifier, subscriber/member data, patient demographics, payer routing, duplicate claims, and syntax/999-related errors.
- Tracks payer and submitter-level transaction patterns.
- Calculates operational KPIs including:
  - Claims processed
  - Acceptance rate
  - SLA compliance
  - SLA breaches
  - Average processing time
- Simulates operational scenarios such as payer routing outages, submitter configuration issues, processing latency, and transaction validation spikes.
- Generates CSV and formatted Excel reporting outputs.
- Automates the reporting workflow through a Python pipeline.
- Provides an interactive Tableau dashboard for operational monitoring and root-cause investigation.

## Tableau Dashboard

The Tableau dashboard provides an operational view of healthcare EDI transaction performance.

Dashboard visualizations include:

- Claims Processed
- Acceptance Rate
- SLA Compliance
- SLA Breaches
- Rejected Claims by Month
- Top Error Categories
- Errors by Submitter
- Payer Routing Errors by Payer
- Average Processing Time Trend
- 20-Second SLA Threshold

Interactive dashboard actions allow users to select error categories and payer routing issues to filter supporting KPIs and visualizations for further investigation.

## Project Structure

```text
Project_02_Healthcare_EDI_Report_Automation/
│
├── 01_generate_report.py
├── 02_analyze_report.py
├── 03_create_excel_report.py
├── 04_run_pipeline.py
├── EDI Operations Performance Dashboard.twb
├── README.md
└── .gitignore