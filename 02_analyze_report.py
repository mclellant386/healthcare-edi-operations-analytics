import csv
from pathlib import Path
from datetime import datetime

project_folder = Path(__file__).parent
input_file = project_folder / "edi_transaction_report.csv"

total_claims = 0
accepted_count = 0
rejected_count = 0
total_processing_time = 0

file_status = {}
file_rejection_counts = {}

submitter_summary = {}
payer_summary = {}
error_category_summary = {}
daily_summary = {}
status_code_summary = {}

with open(input_file, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_claims += 1

        status = row["status"]
        file_name = row["file_name"]
        submitter_id = row["submitter_id"]
        submitter_name = row["submitter_name"]
        payer_name = row["payer_name"]
        error_category = row["error_category"]
        processing_time = float(row["processing_time_seconds"])
        received_date = row["received_timestamp"].split(" ")[0]

        total_processing_time += processing_time

        if file_name not in file_status:
            file_status[file_name] = True

        if submitter_id not in submitter_summary:
            submitter_summary[submitter_id] = {
                "submitter_name": submitter_name,
                "total_claims": 0,
                "accepted": 0,
                "rejected": 0,
                "error_categories": {},
                "impacted_files": set()
            }

        if payer_name not in payer_summary:
            payer_summary[payer_name] = {
                "total_claims": 0,
                "accepted": 0,
                "rejected": 0,
                "total_processing_time": 0
            }

        if received_date not in daily_summary:
            daily_summary[received_date] = {
                "total_claims": 0,
                "accepted": 0,
                "rejected": 0,
                "total_processing_time": 0
            }

        submitter_summary[submitter_id]["total_claims"] += 1
        payer_summary[payer_name]["total_claims"] += 1
        daily_summary[received_date]["total_claims"] += 1

        payer_summary[payer_name]["total_processing_time"] += processing_time
        daily_summary[received_date]["total_processing_time"] += processing_time

        if status == "Accepted":
            accepted_count += 1
            submitter_summary[submitter_id]["accepted"] += 1
            payer_summary[payer_name]["accepted"] += 1
            daily_summary[received_date]["accepted"] += 1

        elif status == "Rejected":
            rejected_count += 1
            file_status[file_name] = False

            file_rejection_counts[file_name] = (
                file_rejection_counts.get(file_name, 0) + 1
            )

            submitter_summary[submitter_id]["rejected"] += 1
            submitter_summary[submitter_id]["impacted_files"].add(file_name)

            payer_summary[payer_name]["rejected"] += 1
            daily_summary[received_date]["rejected"] += 1

            error_category_summary[error_category] = (
                error_category_summary.get(error_category, 0) + 1
            )

            submitter_summary[submitter_id]["error_categories"][error_category] = (
                submitter_summary[submitter_id]["error_categories"].get(
                    error_category, 0
                ) + 1
            )

            status_key = (
                row["claim_status_category_code"],
                row["claim_status_code"],
                row["entity_identifier"],
                row["status_message"]
            )

            status_code_summary[status_key] = (
                status_code_summary.get(status_key, 0) + 1
            )

fully_accepted_files = []
files_with_rejections = []

for file_name, is_fully_accepted in file_status.items():
    if is_fully_accepted:
        fully_accepted_files.append(file_name)
    else:
        files_with_rejections.append(file_name)

acceptance_rate = accepted_count / total_claims if total_claims else 0
rejection_rate = rejected_count / total_claims if total_claims else 0
average_processing_time = (
    total_processing_time / total_claims if total_claims else 0
)

print("837 Claim Processing Monitoring Summary")
print("=======================================")
print(f"Total Claims: {total_claims}")
print(f"Accepted: {accepted_count}")
print(f"Rejected: {rejected_count}")
print(f"Acceptance Rate: {acceptance_rate:.1%}")
print(f"Rejection Rate: {rejection_rate:.1%}")
print(f"Average Processing Time: {average_processing_time:.2f} seconds")

print()
print("File-Level Summary")
print("------------------")
print(f"Files Processed: {len(file_status)}")
print(f"Fully Accepted Files: {len(fully_accepted_files)}")
print(f"Files with Rejections: {len(files_with_rejections)}")

print()
print("Submitter Performance")
print("---------------------")

for submitter_id, summary in sorted(
    submitter_summary.items(),
    key=lambda item: item[1]["rejected"],
    reverse=True
):
    rejection_rate = (
        summary["rejected"] / summary["total_claims"]
        if summary["total_claims"]
        else 0
    )

    top_error_category = "None"

    if summary["error_categories"]:
        top_error_category = max(
            summary["error_categories"],
            key=summary["error_categories"].get
        )

    print(
        f"{submitter_id} - {summary['submitter_name']} | "
        f"Claims: {summary['total_claims']} | "
        f"Rejected: {summary['rejected']} | "
        f"Rejection Rate: {rejection_rate:.1%} | "
        f"Top Error Category: {top_error_category} | "
        f"Impacted Files: {len(summary['impacted_files'])}"
    )

print()
print("Payer Performance")
print("-----------------")

for payer_name, summary in sorted(
    payer_summary.items(),
    key=lambda item: item[1]["rejected"],
    reverse=True
):
    payer_rejection_rate = (
        summary["rejected"] / summary["total_claims"]
        if summary["total_claims"]
        else 0
    )

    payer_avg_processing_time = (
        summary["total_processing_time"] / summary["total_claims"]
        if summary["total_claims"]
        else 0
    )

    print(
        f"{payer_name} | "
        f"Claims: {summary['total_claims']} | "
        f"Rejected: {summary['rejected']} | "
        f"Rejection Rate: {payer_rejection_rate:.1%} | "
        f"Avg Processing Time: {payer_avg_processing_time:.2f}s"
    )

print()
print("Error Category Summary")
print("----------------------")

for category, count in sorted(
    error_category_summary.items(),
    key=lambda item: item[1],
    reverse=True
):
    category_rate = count / rejected_count if rejected_count else 0
    print(f"{category}: {count} ({category_rate:.1%} of rejections)")

print()
print("Top 277CA Status Combinations")
print("-----------------------------")

for status_key, count in sorted(
    status_code_summary.items(),
    key=lambda item: item[1],
    reverse=True
):
    category_code, status_code, entity, message = status_key
    print(
        f"{category_code}:{status_code} | {entity} | "
        f"{message}: {count}"
    )

print()
print("Daily Monitoring Summary")
print("------------------------")

for date, summary in sorted(daily_summary.items()):
    daily_rejection_rate = (
        summary["rejected"] / summary["total_claims"]
        if summary["total_claims"]
        else 0
    )

    daily_avg_processing_time = (
        summary["total_processing_time"] / summary["total_claims"]
        if summary["total_claims"]
        else 0
    )

    print(
        f"{date} | "
        f"Claims: {summary['total_claims']} | "
        f"Rejected: {summary['rejected']} | "
        f"Rejection Rate: {daily_rejection_rate:.1%} | "
        f"Avg Processing Time: {daily_avg_processing_time:.2f}s"
    )