# Reliable LLM Evals

**A reproducible Python toolkit for comparing baseline and candidate AI responses.**

Maintained by **Kamran Rostami**. Independent portfolio project; not affiliated with OpenAI or any employer. All included evaluation examples are synthetic.

## Why this project?

An aggregate accuracy number is not sufficient to decide whether an AI system change is safe to deploy. We need paired comparisons, uncertainty estimates, and transparent regression criteria.

This starter project evaluates **precomputed responses**, so no API keys or paid inference are needed.

## Quickstart

Python 3.10+:

```bash
python -m pip install -e ".[dev]"
pytest -q
python -m reliable_evals.cli examples/synthetic_cases.jsonl
```

The CLI prints a JSON report including accuracy for both systems, candidate-minus-baseline difference, paired bootstrap 95% interval, wins/losses/ties, and a regression-gate result. It exits nonzero if the candidate drops below the allowed accuracy tolerance.

```bash
python -m reliable_evals.cli examples/synthetic_cases.jsonl --tolerance 0.02
```

## Input schema

One JSON object per line, with string fields `id`, `reference`, `baseline_response`, and `candidate_response`. Example:

```json
{"id":"q1","reference":"Paris","baseline_response":"Paris","candidate_response":"Paris"}
```

The starter metric is whitespace-normalized, case-insensitive **exact match**. This is only appropriate for tasks with canonical answers; it is not a semantic, hallucination, or safety evaluator.

## Engineering choices

- **Paired comparisons** hold the evaluation cases constant between baseline and candidate.
- **Bootstrap confidence intervals** resample paired cases with a fixed seed.
- **Explicit regression gates** make pass/fail behavior reproducible.
- **Unit tests and CI** exercise the example and edge cases across Python versions.
- **Synthetic examples** avoid publishing customer or employer information.

## Limitations and roadmap

This is a working **v0.1 starter**, not yet a production-grade LLM evaluation platform. Case-level bootstrap assumes independent examples; repeated sessions or users require cluster-aware resampling. Dataset representativeness, label quality, multiple comparisons, and leakage require separate treatment.

Next iterations: human evaluation rubrics, groundedness and policy evaluation, segment-level reporting, latency/cost metrics, cluster bootstrap, model-provider adapters, and a lightweight dashboard.

## License

MIT.
