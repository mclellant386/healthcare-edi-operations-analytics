import subprocess
from pathlib import Path

project_folder = Path(__file__).parent

scripts = [
    "01_generate_report.py",
    "02_analyze_report.py",
    "03_create_excel_report.py"
]

print("Starting EDI reporting pipeline...")
print("---------------------------------")

for script in scripts:
    print(f"Running {script}...")

    result = subprocess.run(
        ["python3", str(project_folder / script)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"ERROR: {script} failed")
        print(result.stderr)
        break

    print(result.stdout)

print("Pipeline complete.")