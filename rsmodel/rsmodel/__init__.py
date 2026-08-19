"""RS Model: A Resilience-Symptom model for depression dynamics.

This package implements the mathematical model described in:
Rüffer, B. S., & Schönlein, M. (2025). A mathematical model for depression
and resilience.

The model consists of two coupled first-order differential equations:
    dr/dt = (-s + (1-s)*r) * (1-r) * r
    ds/dt = (e*(1+s-r) - s*r) * (1-s) * s

where:
    r ∈ [0,1]: resilience level
    s ∈ [0,1]: depression symptom level
    e ∈ [0,1]: external adverse input

Basic usage:
    >>> from rsmodel import RSModel, Patient
    >>> model = RSModel()
    >>> patient = Patient(s0=0.67, r0=0.84)
    >>> ax = patient.get_stimulus_response(external_input=0.5, t_final=20)

For predefined scenarios:
    >>> from rsmodel.utils import get_predefined_scenarios
    >>> scenarios = get_predefined_scenarios()
    >>> ax = patient.get_stimulus_response(scenarios["from bad to worse then better"])

For mathematical analysis:
    >>> from rsmodel.analysis import compute_jacobian, analyze_corner_equilibria
    >>> J = compute_jacobian(model)
    >>> corner_analysis = analyze_corner_equilibria(model, e_value=0.5)
"""

__version__ = "0.1.2"
__author__ = "Björn S. Rüffer & Michael Schönlein"
__license__ = "MIT"

# Core classes
# Analysis functions
from .analysis import (
    analyze_corner_equilibria,
    classify_equilibrium_stability,
    compute_jacobian,
    compute_monotonicity_conditions,
    evaluate_jacobian_at_equilibrium,
    find_interior_equilibrium_intersection,
    get_eigenvalues,
    lyapunov_function_derivative,
    plot_eigenvalue_evolution,
    verify_lyapunov_function,
)
from .core import Patient, RS2Model, RSModel

# Utility functions
from .utils import (
    create_custom_stimulus,
    from_bad_to_less_bad_to_not_great,
    from_bad_to_worse_then_better,
    get_predefined_scenarios,
    multiple_adverse_events,
    sample_and_hold,
)

__all__ = [
    # Core
    "RSModel",
    "RS2Model",
    "Patient",
    # Analysis
    "compute_jacobian",
    "evaluate_jacobian_at_equilibrium",
    "get_eigenvalues",
    "classify_equilibrium_stability",
    "analyze_corner_equilibria",
    "lyapunov_function_derivative",
    "verify_lyapunov_function",
    "plot_eigenvalue_evolution",
    "compute_monotonicity_conditions",
    "find_interior_equilibrium_intersection",
    # Utils
    "from_bad_to_worse_then_better",
    "multiple_adverse_events",
    "from_bad_to_less_bad_to_not_great",
    "get_predefined_scenarios",
    "create_custom_stimulus",
    "sample_and_hold",
]
