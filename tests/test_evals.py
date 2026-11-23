import pytest
from pathlib import Path
from reliable_evals.metrics import compare_cases, match
from reliable_evals.statistics import paired_bootstrap_delta
from reliable_evals.cli import evaluate

def test_normalization():
    assert match("  PARIS  ", "paris") == 1
    assert match("Paris", "London") == 0

def test_example():
    report = evaluate(Path("examples/synthetic_cases.jsonl"))
    assert report["n"] == 6
    assert report["wins"] == 2
    assert report["losses"] == 1
    assert report["delta"] == pytest.approx(1/6)
    assert report["regression_gate_passed"]

def test_empty():
    with pytest.raises(ValueError):
        compare_cases([])

def test_bootstrap():
    assert paired_bootstrap_delta([0,1],[0,1]) == (0.0,0.0)
    assert paired_bootstrap_delta([0,1],[1,1]) == paired_bootstrap_delta([0,1],[1,1])
