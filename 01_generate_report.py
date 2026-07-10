import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

project_folder = Path(__file__).parent
output_file = project_folder / "edi_transaction_report.csv"

rows = []

TOTAL_ROWS = 5000
HISTORY_DAYS = 120

submitters = [
    {
        "submitter_id": "SUB001",
        "submitter_name": "Atlantic Family Care",
        "organization_type": "Physician Group",
        "state": "FL",
        "billing_provider_npi": "1932456789",
        "rendering_provider_npi": "1932456790",
        "tenure_days": 820,
        "base_weight": 1.1
    },
    {
        "submitter_id": "SUB002",
        "submitter_name": "Metro Billing Services",
        "organization_type": "Billing Service",
        "state": "GA",
        "billing_provider_npi": "1845123456",
        "rendering_provider_npi": "1845123457",
        "tenure_days": 540,
        "base_weight": 1.0
    },
    {
        "submitter_id": "SUB003",
        "submitter_name": "Sunrise Regional Hospital",
        "organization_type": "Hospital",
        "state": "TX",
        "billing_provider_npi": "1777987654",
        "rendering_provider_npi": "1777987655",
        "tenure_days": 1100,
        "base_weight": 1.2
    },
    {
        "submitter_id": "SUB004",
        "submitter_name": "Northlake Specialty Clinic",
        "organization_type": "Specialty Clinic",
        "state": "NC",
        "billing_provider_npi": "1666234567",
        "rendering_provider_npi": "1666234568",
        "tenure_days": 310,
        "base_weight": 0.9
    },
    {
        "submitter_id": "SUB005",
        "submitter_name": "Coastal Health Partners",
        "organization_type": "Physician Group",
        "state": "FL",
        "billing_provider_npi": "1555345678",
        "rendering_provider_npi": "1555345679",
        "tenure_days": 690,
        "base_weight": 1.0
    },
    {
        "submitter_id": "SUB006",
        "submitter_name": "ABC Orthopedics",
        "organization_type": "Specialty Clinic",
        "state": "FL",
        "billing_provider_npi": "1444456789",
        "rendering_provider_npi": "1444456790",
        "tenure_days": 14,
        "base_weight": 0.7
    }
]

payers = [
    {
        "trading_partner": "Centene",
        "payer_id": "11315",
        "payer_name": "Centene Health Plan",
        "receiver_id": "CENTENE",
        "base_weight": 1.2
    },
    {
        "trading_partner": "Aetna",
        "payer_id": "60054",
        "payer_name": "Aetna Health",
        "receiver_id": "AETNA",
        "base_weight": 1.0
    },
    {
        "trading_partner": "Florida Blue",
        "payer_id": "00590",
        "payer_name": "Florida Blue",
        "receiver_id": "FLBLUE",
        "base_weight": 1.1
    }
]

accepted_result = {
    "status": "Accepted",
    "acknowledgment_type": "277CA",
    "claim_status_category_code": "A1",
    "claim_status_code": "19",
    "entity_identifier": "",
    "status_message": "Claim accepted for processing",
    "error_category": "Accepted"
}

rejection_options = [
    {
        "status": "Rejected",
        "acknowledgment_type": "277CA",
        "claim_status_category_code": "A3",
        "claim_status_code": "562",
        "entity_identifier": "Billing Provider",
        "status_message": "Invalid billing provider identifier",
        "error_category": "Provider Identifier"
    },
    {
        "status": "Rejected",
        "acknowledgment_type": "277CA",
        "claim_status_category_code": "A3",
        "claim_status_code": "128",
        "entity_identifier": "Subscriber",
        "status_message": "Invalid subscriber identifier",
        "error_category": "Subscriber / Member Data"
    },
    {
        "status": "Rejected",
        "acknowledgment_type": "277CA",
        "claim_status_category_code": "A3",
        "claim_status_code": "21",
        "entity_identifier": "Patient",
        "status_message": "Missing or invalid patient information",
        "error_category": "Patient Demographics"
    },
    {
        "status": "Rejected",
        "acknowledgment_type": "277CA",
        "claim_status_category_code": "A3",
        "claim_status_code": "145",
        "entity_identifier": "Payer",
        "status_message": "Invalid payer identifier",
        "error_category": "Payer Routing"
    },
    {
        "status": "Rejected",
        "acknowledgment_type": "277CA",
        "claim_status_category_code": "A3",
        "claim_status_code": "187",
        "entity_identifier": "Claim",
        "status_message": "Duplicate claim submission",
        "error_category": "Duplicate Claim"
    },
    {
        "status": "Rejected",
        "acknowledgment_type": "277CA",
        "claim_status_category_code": "A3",
        "claim_status_code": "684",
        "entity_identifier": "Claim",
        "status_message": "Rejected due to syntax errors identified in prior acknowledgment",
        "error_category": "Syntax / 999 Related"
    }
]


def choose_weighted_item(items):
    return random.choices(
        items,
        weights=[item["base_weight"] for item in items],
        k=1
    )[0]


def get_rejection_by_category(category):
    matching_options = [
        option for option in rejection_options
        if option["error_category"] == category
    ]

    return random.choice(matching_options)


def get_general_rejection():
    return random.choice(rejection_options)


def get_recommended_action(error_category):
    recommendations = {
        "Accepted": "No action required",
        "Provider Identifier": "Validate billing/rendering provider NPI and provider enrollment configuration",
        "Subscriber / Member Data": "Review subscriber identifiers and member demographic data submitted by the client",
        "Patient Demographics": "Review patient demographic mapping and required claim data elements",
        "Payer Routing": "Validate payer ID, receiver ID, and trading partner routing configuration",
        "Duplicate Claim": "Review submitter retry logic and duplicate claim submission behavior",
        "Syntax / 999 Related": "Review 999 acknowledgment details and X12 syntax or implementation guide validation errors"
    }

    return recommendations.get(error_category, "Review rejected claim details")


def get_operational_risk(status_result, processing_time, rejection_probability):
    if status_result["status"] == "Rejected" and rejection_probability >= 0.25:
        return "High"

    if processing_time > 45:
        return "High"

    if status_result["status"] == "Rejected" or processing_time > 30:
        return "Medium"

    return "Low"


start_date = datetime.now() - timedelta(days=HISTORY_DAYS - 1)

transaction_number = 1

for i in range(TOTAL_ROWS):
    submitter = choose_weighted_item(submitters)
    payer = choose_weighted_item(payers)

    day_offset = random.randint(0, HISTORY_DAYS - 1)
    current_date = start_date + timedelta(days=day_offset)
    weekday = current_date.weekday()

    # Monday volume pattern: Mondays are more likely to appear in generated data.
    if random.random() < 0.18:
        while current_date.weekday() != 0:
            current_date += timedelta(days=1)
            if (current_date - start_date).days >= HISTORY_DAYS:
                current_date = start_date + timedelta(days=day_offset)
                break

    received_time = current_date + timedelta(
        hours=random.randint(7, 20),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    day_offset = (received_time.date() - start_date.date()).days
    weekday = received_time.weekday()

    claims_in_file = random.randint(15, 80)

    if weekday == 0:
        claims_in_file = random.randint(55, 130)

    file_size_kb = round(claims_in_file * random.uniform(2.0, 4.5), 2)

    batch_number = (i // 50) + 1
    batch_id = f"BATCH{batch_number:04}"

    file_name = (
        f"837_{payer['receiver_id']}_"
        f"{submitter['submitter_id']}_{batch_id}.edi"
    )

    rejection_probability = 0.055
    forced_error_category = None

    queue_time = random.uniform(1.0, 6.0)
    validation_time = random.uniform(2.0, 8.0)
    routing_time = random.uniform(1.0, 5.0)

    operational_event = "Normal Processing"
    payer_incident_flag = False
    configuration_change_flag = False
    onboarding_issue_flag = False
    high_volume_day_flag = False
    deployment_issue_flag = False

    # Event 1: Monday volume spike.
    if weekday == 0:
        high_volume_day_flag = True
        queue_time += random.uniform(8.0, 18.0)
        rejection_probability += 0.025
        operational_event = "Monday Volume Spike"

    # Event 2: New submitter onboarding issue for ABC Orthopedics.
    # Final 20 days simulate early production period.
    if submitter["submitter_id"] == "SUB006" and day_offset >= 100:
        onboarding_issue_flag = True
        rejection_probability = 0.32

        forced_error_category = random.choices(
            ["Provider Identifier", "Syntax / 999 Related"],
            weights=[75, 25],
            k=1
        )[0]

        validation_time += random.uniform(6.0, 14.0)
        operational_event = "New Submitter Onboarding Issue"

    # Event 3: Centene two-day payer routing outage.
    if payer["receiver_id"] == "CENTENE" and 78 <= day_offset <= 79:
        payer_incident_flag = True
        rejection_probability = 0.42
        forced_error_category = "Payer Routing"
        routing_time += random.uniform(20.0, 40.0)
        operational_event = "Centene Routing Outage"

    # Event 4: Translator deployment created temporary syntax / 999 errors.
    if 50 <= day_offset <= 52:
        deployment_issue_flag = True
        rejection_probability += 0.10

        if random.random() < 0.65:
            forced_error_category = "Syntax / 999 Related"

        validation_time += random.uniform(8.0, 20.0)
        operational_event = "Translator Deployment Validation Spike"

    # Event 5: Aetna latency trend in final 50 days.
    if payer["receiver_id"] == "AETNA" and day_offset >= 70:
        days_into_latency_trend = day_offset - 70
        queue_time += days_into_latency_trend * 0.28

        if operational_event == "Normal Processing":
            operational_event = "Aetna Processing Latency Trend"

    # Event 6: SUB002 member data configuration issue.
    if submitter["submitter_id"] == "SUB002" and 95 <= day_offset <= 104:
        configuration_change_flag = True
        rejection_probability = 0.24
        forced_error_category = "Subscriber / Member Data"
        operational_event = "Submitter Member Data Configuration Issue"

    # Event 7: Existing submitter provider identifier deterioration.
    if submitter["submitter_id"] == "SUB004" and day_offset >= 60:
        days_into_deterioration = day_offset - 60
        rejection_probability += days_into_deterioration * 0.003

        if random.random() < 0.75:
            forced_error_category = "Provider Identifier"

        if operational_event == "Normal Processing":
            operational_event = "Provider Identifier Deterioration"

    if random.random() < rejection_probability:
        if forced_error_category:
            status_result = get_rejection_by_category(forced_error_category)
        else:
            status_result = get_general_rejection()
    else:
        status_result = accepted_result

    processing_time = round(
        queue_time + validation_time + routing_time,
        2
    )

    processed_time = received_time + timedelta(seconds=processing_time)
    sla_breached = processing_time > 30

    recommended_action = get_recommended_action(
        status_result["error_category"]
    )

    operational_risk = get_operational_risk(
        status_result,
        processing_time,
        rejection_probability
    )

    row = {
        "received_timestamp": received_time.strftime("%Y-%m-%d %H:%M:%S"),
        "processed_timestamp": processed_time.strftime("%Y-%m-%d %H:%M:%S"),
        "claim_id": f"CLM{transaction_number:08}",
        "transaction_id": f"TXN{transaction_number:08}",
        "batch_id": batch_id,
        "file_name": file_name,

        "submitter_id": submitter["submitter_id"],
        "submitter_name": submitter["submitter_name"],
        "organization_type": submitter["organization_type"],
        "state": submitter["state"],
        "submitter_tenure_days": submitter["tenure_days"],

        "billing_provider_npi": submitter["billing_provider_npi"],
        "rendering_provider_npi": submitter["rendering_provider_npi"],

        "trading_partner": payer["trading_partner"],
        "payer_id": payer["payer_id"],
        "payer_name": payer["payer_name"],
        "receiver_id": payer["receiver_id"],

        "transaction_type": "837",
        "mode": "batch",

        "status": status_result["status"],
        "acknowledgment_type": status_result["acknowledgment_type"],
        "claim_status_category_code": status_result["claim_status_category_code"],
        "claim_status_code": status_result["claim_status_code"],
        "entity_identifier": status_result["entity_identifier"],
        "status_message": status_result["status_message"],
        "error_category": status_result["error_category"],

        "claim_count": 1,
        "claims_in_file": claims_in_file,
        "file_size_kb": file_size_kb,
        "submission_hour": received_time.hour,

        "processing_queue_seconds": round(queue_time, 2),
        "validation_time_seconds": round(validation_time, 2),
        "routing_time_seconds": round(routing_time, 2),
        "processing_time_seconds": processing_time,
        "sla_breached": sla_breached,

        "operational_event": operational_event,
        "operational_risk": operational_risk,
        "recommended_action": recommended_action,

        "payer_incident_flag": payer_incident_flag,
        "configuration_change_flag": configuration_change_flag,
        "onboarding_issue_flag": onboarding_issue_flag,
        "high_volume_day_flag": high_volume_day_flag,
        "deployment_issue_flag": deployment_issue_flag
    }

    rows.append(row)
    transaction_number += 1

rows.sort(key=lambda row: row["received_timestamp"])

with open(output_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Report generated: {output_file}")
print(f"Rows generated: {len(rows)}")
print(f"History generated: {HISTORY_DAYS} days")
print("Operational scenarios included:")
print("- Monday volume spike")
print("- New submitter onboarding issue")
print("- Centene routing outage")
print("- Translator deployment validation spike")
print("- Aetna processing latency trend")
print("- Submitter member data configuration issue")
print("- Provider identifier deterioration")