"""Run a reproducible evaluation from JSONL."""
import argparse
import json
from pathlib import Path
from .metrics import compare_cases, match
from .statistics import paired_bootstrap_delta

def evaluate(path: Path, tolerance: float = 0.0) -> dict:
    if not 0 <= tolerance <= 1:
        raise ValueError("Tolerance must be between zero and one")
    cases = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    report = compare_cases(cases)
    baseline = [match(r["baseline_response"],r["reference"]) for r in cases]
    candidate = [match(r["candidate_response"],r["reference"]) for r in cases]
    report["delta_ci_95"] = paired_bootstrap_delta(baseline,candidate)
    report["regression_gate_passed"] = report["delta"] >= -tolerance
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset",type=Path)
    parser.add_argument("--tolerance",type=float,default=0.0)
    args = parser.parse_args()
    report = evaluate(args.dataset,args.tolerance)
    print(json.dumps(report,indent=2))
    if not report["regression_gate_passed"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
