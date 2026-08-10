from __future__ import annotations

import pytest

from efgm.benchmark_v0_2 import generate_cases
from efgm.experiment_runner_v0_2 import run_experiment


def _single_pair_cases():
    cases = generate_cases()
    pair_id = cases[0]["pair_id"]
    return [case for case in cases if case["pair_id"] == pair_id]


def test_zero_sensitivity_trials_are_rejected():
    with pytest.raises(ValueError, match="positive integer"):
        run_experiment(cases=_single_pair_cases(), sensitivity_trials=0)


def test_negative_sensitivity_trials_are_rejected():
    with pytest.raises(ValueError, match="positive integer"):
        run_experiment(cases=_single_pair_cases(), sensitivity_trials=-1)


@pytest.mark.parametrize("perturbation", [-0.01, 1.01, float("inf"), float("nan")])
def test_out_of_range_or_nonfinite_perturbation_is_rejected(perturbation: float):
    with pytest.raises(ValueError, match="finite number in \\[0, 1\\]"):
        run_experiment(cases=_single_pair_cases(), sensitivity_trials=1, perturbation=perturbation)
