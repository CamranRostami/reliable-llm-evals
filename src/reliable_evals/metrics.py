"""Deterministic metrics for paired response evaluation."""

def match(response: str, reference: str) -> int:
    return int(" ".join(response.casefold().split()) == " ".join(reference.casefold().split()))

def compare_cases(cases: list[dict]) -> dict:
    if not cases:
        raise ValueError("Dataset cannot be empty")
    required = ("id", "reference", "baseline_response", "candidate_response")
    seen = set()
    outcomes = []
    for row in cases:
        if any(k not in row or not isinstance(row[k], str) for k in required):
            raise ValueError("Missing or invalid required string field")
        if row["id"] in seen:
            raise ValueError("Duplicate case ID")
        seen.add(row["id"])
        outcomes.append((match(row["baseline_response"], row["reference"]), match(row["candidate_response"], row["reference"])))
    n = len(outcomes)
    return {"n": n, "baseline_accuracy": sum(b for b, _ in outcomes)/n,
            "candidate_accuracy": sum(c for _, c in outcomes)/n,
            "delta": sum(c-b for b,c in outcomes)/n,
            "wins": sum(c>b for b,c in outcomes), "losses": sum(c<b for b,c in outcomes),
            "ties": sum(c==b for b,c in outcomes)}
