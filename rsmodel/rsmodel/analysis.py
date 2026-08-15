"""Mathematical analysis tools for the RS model.

This module provides functions for:
- Computing and analyzing equilibria
- Jacobian and stability analysis
- Lyapunov function verification
- Eigenvalue analysis
"""

from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import sympy

from .core import RSModel


def compute_jacobian(model: RSModel, state_vars=None) -> sympy.Matrix:
    """Compute the Jacobian matrix of the RS model.

    Args:
        model: RSModel instance
        state_vars: State variables (default: [model.r, model.s])

    Returns:
        Jacobian matrix as sympy.Matrix
    """
    if state_vars is None:
        state_vars = sympy.Matrix([model.r, model.s])

    f = sympy.Matrix([model.dr, model.ds])
    return f.jacobian(state_vars)


def evaluate_jacobian_at_equilibrium(
    model: RSModel, equilibrium: Dict, e_value: float = None
) -> sympy.Matrix:
    """Evaluate Jacobian at a specific equilibrium point.

    Args:
        model: RSModel instance
        equilibrium: Dictionary with equilibrium point {r: val, s: val}
        e_value: Value of e if equilibrium is parameterized

    Returns:
        Jacobian matrix evaluated at the equilibrium
    """
    J = compute_jacobian(model)
    J_eq = J.subs(equilibrium)

    if e_value is not None:
        J_eq = J_eq.subs(model.e, e_value)

    return J_eq


def get_eigenvalues(matrix: sympy.Matrix) -> List:
    """Get eigenvalues of a symbolic matrix.

    Args:
        matrix: Sympy matrix

    Returns:
        List of eigenvalues (may be symbolic)
    """
    return list(matrix.eigenvals().keys())


def classify_equilibrium_stability(
    model: RSModel, equilibrium: Dict, e_value: float = None
) -> str:
    """Classify stability of an equilibrium point.

    Args:
        model: RSModel instance
        equilibrium: Equilibrium point dictionary
        e_value: Value of e if needed

    Returns:
        String classification: 'stable', 'unstable', 'saddle', or 'undetermined'
    """
    J = evaluate_jacobian_at_equilibrium(model, equilibrium, e_value)
    eigenvals = get_eigenvalues(J)

    # Evaluate eigenvalues numerically if possible
    try:
        eigenvals_numeric = [complex(ev.evalf()) for ev in eigenvals]
        real_parts = [ev.real for ev in eigenvals_numeric]

        if all(rp < 0 for rp in real_parts):
            return "stable"
        elif all(rp > 0 for rp in real_parts):
            return "unstable"
        else:
            return "saddle"
    except:
        return "undetermined"


def analyze_corner_equilibria(model: RSModel, e_value: float = 0.5) -> Dict:
    """Analyze stability of the four corner equilibria.

    The corners are: (r,s) ∈ {(0,0), (1,0), (0,1), (1,1)}

    Args:
        model: RSModel instance
        e_value: Value of external input e

    Returns:
        Dictionary with corner analysis results
    """
    corners = [
        {model.r: 0, model.s: 0},  # p1
        {model.r: 1, model.s: 0},  # p2
        {model.r: 1, model.s: 1},  # p3
        {model.r: 0, model.s: 1},  # p4
    ]

    results = {}
    for i, corner in enumerate(corners, 1):
        J = evaluate_jacobian_at_equilibrium(model, corner, e_value)
        eigenvals = get_eigenvalues(J)
        stability = classify_equilibrium_stability(model, corner, e_value)

        results[f"p{i}"] = {
            "equilibrium": corner,
            "jacobian": J,
            "eigenvalues": eigenvals,
            "stability": stability,
        }

    return results


def lyapunov_function_derivative(model: RSModel, V_expr) -> sympy.Expr:
    """Compute time derivative of a Lyapunov function candidate.

    Args:
        model: RSModel instance
        V_expr: Lyapunov function V(r,s) as sympy expression

    Returns:
        dV/dt = ∇V · f as sympy expression
    """
    state_vars = sympy.Matrix([model.r, model.s])
    f = sympy.Matrix([model.dr, model.ds])

    grad_V = sympy.Matrix([V_expr]).jacobian(state_vars)
    dV = (grad_V * f)[0]

    return dV


def verify_lyapunov_function(model: RSModel, V_expr, equilibrium: Dict = None) -> Dict:
    """Verify a Lyapunov function for stability analysis.

    Args:
        model: RSModel instance
        V_expr: Lyapunov function V(r,s)
        equilibrium: Equilibrium point (if None, checks general negativity)

    Returns:
        Dictionary with verification results
    """
    dV = lyapunov_function_derivative(model, V_expr)
    dV_expanded = dV.expand()

    results = {
        "V": V_expr,
        "dV": dV,
        "dV_expanded": dV_expanded,
        "dV_collected": dV_expanded.collect(model.s),
    }

    if equilibrium is not None:
        dV_at_eq = dV.subs(equilibrium)
        results["dV_at_equilibrium"] = dV_at_eq

    return results


def plot_eigenvalue_evolution(
    model: RSModel,
    equilibrium_parameterized: Dict,
    e_range: np.ndarray = None,
    title: str = "Eigenvalue evolution",
):
    """Plot how eigenvalues change as parameter e varies.

    Args:
        model: RSModel instance
        equilibrium_parameterized: Equilibrium point depending on e
        e_range: Range of e values (default: linspace(0,1,100))
        title: Plot title

    Returns:
        Matplotlib axes object
    """
    if e_range is None:
        e_range = np.linspace(0.001, 0.999, 100)

    J = evaluate_jacobian_at_equilibrium(model, equilibrium_parameterized)
    eigenvals = get_eigenvalues(J)

    # Evaluate eigenvalues over e range
    eigenval_data = {i: [] for i in range(len(eigenvals))}

    for e_val in e_range:
        for i, ev in enumerate(eigenvals):
            try:
                val = complex(ev.subs(model.e, e_val).evalf())
                eigenval_data[i].append(val)
            except:
                eigenval_data[i].append(np.nan)

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Real parts
    for i, vals in eigenval_data.items():
        real_parts = [v.real if not np.isnan(v) else np.nan for v in vals]
        ax1.plot(e_range, real_parts, label=f"λ{i + 1}")

    ax1.axhline(y=0, color="k", linestyle="--", linewidth=0.5)
    ax1.set_xlabel("External input $e$")
    ax1.set_ylabel("Real part")
    ax1.set_title(f"{title} - Real parts")
    ax1.legend()
    ax1.grid(True)

    # Imaginary parts
    for i, vals in eigenval_data.items():
        imag_parts = [v.imag if not np.isnan(v) else np.nan for v in vals]
        ax2.plot(e_range, imag_parts, label=f"λ{i + 1}")

    ax2.axhline(y=0, color="k", linestyle="--", linewidth=0.5)
    ax2.set_xlabel("External input $e$")
    ax2.set_ylabel("Imaginary part")
    ax2.set_title(f"{title} - Imaginary parts")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    return ax1


def compute_monotonicity_conditions(model: RSModel) -> Dict:
    """Compute monotonicity conditions for the RS model.

    Analyzes:
    - ∂f₁/∂s (effect of symptoms on resilience dynamics)
    - ∂f₂/∂r (effect of resilience on symptom dynamics)
    - ∂f₁/∂e (direct effect of input on resilience)
    - ∂f₂/∂e (direct effect of input on symptoms)

    Returns:
        Dictionary with partial derivatives and their analysis
    """
    results = {
        "df1_ds": model.dr.diff(model.s),  # negative: symptoms harm resilience
        "df2_dr": model.ds.diff(model.r),  # negative: resilience reduces symptoms
        "df1_de": model.dr.diff(model.e),  # direct input effect on resilience
        "df2_de": model.ds.diff(model.e),  # direct input effect on symptoms
    }

    # Simplify
    for key in results:
        results[key] = results[key].simplify()

    return results


def find_interior_equilibrium_intersection(model: RSModel) -> Dict:
    """Find the interior equilibrium (intersection of nullclines).

    Solves for the point where both dr/dt = 0 and ds/dt = 0 in the interior
    of [0,1]², parameterized by e.

    Returns:
        Dictionary with symbolic solutions
    """
    # Nullclines: dr=0 gives r/(1+r), ds=0 gives (1-r)/(r/e-1)
    # Find intersection
    r, e = model.r, model.e

    # From dr=0 (non-trivial): s = r/(1+r)
    # From ds=0 (non-trivial): s = (1-r)/(r/e-1)
    # Set equal and solve

    s_from_dr = r / (1 + r)
    s_from_ds = (1 - r) / (r / e - 1)

    # Solve for r
    eq = s_from_dr - s_from_ds
    r_solution = sympy.solve(eq, r)

    results = {}
    for i, r_val in enumerate(r_solution):
        s_val = s_from_dr.subs(r, r_val)
        results[f"interior_eq_{i}"] = {
            "r": r_val,
            "s": s_val,
        }

    return results
