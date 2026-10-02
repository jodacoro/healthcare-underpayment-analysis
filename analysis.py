"""Reproducible synthetic portfolio example; Python standard library only."""
from pathlib import Path
import csv
import random
import sqlite3

BASE = Path(__file__).resolve().parent

def write_csv(path, columns, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)

def main():
    data = BASE / "data"
    output = BASE / "output"
    data.mkdir(exist_ok=True)
    output.mkdir(exist_ok=True)
    rng = random.Random(42)
    rows = []
    for i in range(2000):
        payer = rng.choice(["Payer A", "Payer B", "Payer C", "Payer D"])
        expected = round(rng.uniform(100, 2500), 2)
        ratio = rng.choices([1.0, 0.85, 0.65, 1.05], weights=[60, 25, 10, 5])[0]
        paid = round(expected * ratio, 2)
        code = rng.choice(["SIM_CONTRACT", "SIM_CODING", "SIM_DOCUMENTATION"]) if paid < expected else "NONE"
        rows.append((f"CLM-{i+1:05d}", payer, expected, paid, code))
    write_csv(data / "claims.csv", ["claim_id", "payer", "expected", "paid", "denial_code"], rows)
    with sqlite3.connect(output / "claims.db") as connection:
        connection.execute("DROP TABLE IF EXISTS claims")
        connection.execute("CREATE TABLE claims (claim_id TEXT PRIMARY KEY, payer TEXT, expected REAL, paid REAL, denial_code TEXT)")
        connection.executemany("INSERT INTO claims VALUES (?, ?, ?, ?, ?)", rows)
        statements = [q.strip() for q in (BASE / "queries.sql").read_text().split(";") if q.strip()]
        results = []
        for statement, name in zip(statements, ["payer_summary", "denial_summary", "review_queue"]):
            cursor = connection.execute(statement)
            records = cursor.fetchall()
            write_csv(output / f"{name}.csv", [c[0] for c in cursor.description], records)
            results.append(records)
        payers, denials, queue = results
        gap = sum(row[4] for row in payers)
        report = f"# Synthetic claims analysis\n\n2,000 simulated claims. Total positive payment gap: ${gap:,.2f}.\n\n"
        report += "| Payer | Claims | Positive payment gap | Claims with gaps (%) |\n|---|---:|---:|---:|\n"
        for row in payers:
            report += f"| {row[0]} | {row[1]} | ${row[4]:,.2f} | {row[5]:.2f} |\n"
        report += f"\n{len(queue)} claims exceed the $100 review threshold.\n\n"
        report += f"Start reviewing {payers[0][0]} because it has the largest aggregate positive gap in this sample. Validate contracts and adjustments before treating any amount as recoverable.\n\n"
        report += "All results describe generated data. Payer assignment is random; differences do not establish payer behavior. Denial labels are simulated categories, not official codes. No causal or professional impact claim is made.\n"
        (output / "report.md").write_text(report, encoding="utf-8")
    print("Created synthetic data, SQLite database, SQL summaries, review queue, and report.")

if __name__ == "__main__":
    main()
