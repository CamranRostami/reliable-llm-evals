"""Paired case-level bootstrap. Cases must be independent."""
import random

def paired_bootstrap_delta(baseline: list[int], candidate: list[int], iterations: int = 2000, seed: int = 42) -> tuple[float, float]:
    if not baseline or len(baseline) != len(candidate):
        raise ValueError("Paired samples must have equal nonzero length")
    if iterations < 100 or any(v not in (0,1) for v in baseline + candidate):
        raise ValueError("Invalid iterations or binary outcomes")
    differences = [c-b for b,c in zip(baseline,candidate)]
    n = len(differences)
    rng = random.Random(seed)
    estimates = sorted(sum(differences[rng.randrange(n)] for _ in range(n))/n for _ in range(iterations))
    return estimates[int(.025*(iterations-1))], estimates[int(.975*(iterations-1))]
