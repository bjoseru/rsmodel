"""Core classes for the Resilience-Symptom (RS) model of depression.

This module implements the mathematical model described in:
Rüffer, B. S., & Schönlein, M. (2025). A mathematical model for depression
and resilience.

The model consists of two coupled first-order differential equations describing:
- r: Resilience level (0 = depleted, 1 = full resilience)
- s: Depression symptom level (0 = healthy, 1 = severe depression)
- e: External adverse input/stressor (0 = no stress; larger values = more severe adversity)
"""

from typing import Callable, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import sympy
from scipy.integrate import solve_ivp


class RSModel:
    """Resilience-Symptom model for depression dynamics.

    The model is defined by the system of differential equations:
        dr/dt = (-s + (1-s)*r) * (1-r) * r
        ds/dt = (e*(1+s-r) - s*r) * (1-s) * s

    where:
        r ∈ [0,1]: resilience level
        s ∈ [0,1]: depression symptom level
        e ≥ 0: external adverse input

    The domain [0,1]² is positively invariant.

    Attributes:
        e, r, s, t: Symbolic variables (sympy.Symbol)
        dr: Symbolic expression for resilience dynamics
        ds: Symbolic expression for symptom dynamics
        model_name: String identifier for this model variant
    """

    # Symbolic variables (class-level, shared by all instances)
    e, r, s, t = sympy.symbols("e r s t")

    # Model equations (can be overridden in subclasses)
    dr = (-s + (1 - s) * r) * (1 - r) * r
    ds = (e * (1 + s - r) - s * r) * (1 - s) * s
    model_name = "RS model"

    def __init__(self):
        """Initialize the RS model.

        Subclasses can override the equations by redefining dr, ds, and model_name
        in their __init__ method.
        """
        pass

    def rhs(self, _r: float, _s: float, _e: float) -> Tuple[float, float]:
        """Evaluate the right-hand side of the ODE system.

        Args:
            _r: Current resilience level
            _s: Current symptom level
            _e: Current external input

        Returns:
            Tuple (dr/dt, ds/dt) evaluated at the given state
        """
        subs = {self.r: _r, self.s: _s, self.e: _e}
        return float(self.dr.subs(subs)), float(self.ds.subs(subs))

    def latex_dr(self) -> str:
        """Return LaTeX representation of the resilience dynamics equation."""
        return r"\dot r = " + sympy.latex(self.dr)

    def latex_ds(self) -> str:
        """Return LaTeX representation of the symptom dynamics equation."""
        return r"\dot s = " + sympy.latex(self.ds)

    def __str__(self) -> str:
        """String representation showing the model equations."""
        return f"""`{self.model_name}` defined by
  $${self.latex_dr()}$$
and
  $${self.latex_ds()}.$$"""

    def get_equilibria(self):
        """Compute equilibrium points of the system.

        Returns:
            List of equilibria as tuples (r_value, s_value).
            Values may be symbolic expressions depending on parameter e.
        """
        return sympy.solve([self.dr, self.ds], [self.r, self.s])

    def plot_equilibria(self, color: str = "#c00", samples: int = 500):
        """Plot the equilibrium manifold in (r,s) space.

        Creates a plot showing all equilibrium points as e varies from 0 to 1.
        Some equilibria are fixed points (corners), others form curves.

        Args:
            color: Color for the equilibrium curve
            samples: Number of samples for parameterized curves

        Returns:
            Matplotlib axes object with the equilibrium plot
        """
        pts_to_plot = []
        e_range = np.linspace(1e-3, 1 - 1e-3, samples)

        for r_val, s_val in self.get_equilibria():
            params = r_val.free_symbols.union(s_val.free_symbols)

            if len(params) == 0:
                # Fixed point (independent of e)
                pts_to_plot.append((float(r_val), float(s_val)))

            elif len(params) == 1:
                # Curve parameterized by e
                try:
                    e = params.pop()
                    r_range = [r_val.subs({e: float(_)}) for _ in e_range]
                    s_range = [s_val.subs({e: float(_)}) for _ in e_range]
                    plt.plot(r_range, s_range, color=color)
                except RuntimeWarning:
                    pass  # Ignore issues like complex values, infinity

        # Plot fixed points
        if pts_to_plot:
            try:
                plt.plot(*zip(*pts_to_plot, strict=False), "o", color=color)
            except RuntimeWarning:
                pass

        plt.title(
            rf'Location of equilibria of "{self.model_name}" (with constant $e\in[0,1]$)'
        )
        plt.xlabel("Resilience $r$")
        plt.ylabel("Symptom $s$")
        plt.grid("both")

        ax = plt.gca()
        ax.set_xlim(-1e-2, 1 + 1e-2)
        ax.set_ylim(-1e-2, 1 + 1e-2)
        ax.spines[["top", "right", "bottom", "left"]].set_visible(False)

        return ax

    def plot_streamlines(self, external_input: float = 0.0, cmap: str = "inferno"):
        """Create a streamline (phase portrait) plot for constant input.

        Shows the vector field and flow lines in the (r,s) phase space
        for a fixed value of the external input e.

        Args:
            external_input: Fixed value of e for the plot
            cmap: Matplotlib colormap for the streamlines

        Returns:
            Matplotlib axes object with the streamline plot
        """
        R, S = np.mgrid[0:1:30j, 0:1:30j]

        def to_float(tpl):
            """Cast a vector into floats."""
            return tuple(map(float, tpl))

        DR, DS = np.vectorize(lambda r, s: to_float(self.rhs(r, s, external_input)))(
            R, S
        )

        speed = np.sqrt(DR**2 + DS**2)

        fig, ax = plt.subplots()

        strm = ax.streamplot(
            R.T,
            S.T,
            DR.T,
            DS.T,
            color=speed.T,
            linewidth=2,
            cmap=cmap,
        )

        fig.colorbar(strm.lines)
        plt.xlabel("Resilience $r$")
        plt.ylabel("Symptom $s$")
        plt.title(f"Streamlines for {self.model_name} with $e={external_input:4.2f}$")

        plt.grid(True)
        ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

        return ax


class RS2Model(RSModel):
    """Modified version of the RS model with altered symptom dynamics.

    This variant changes the coefficient in the s*r term from 1 to 3:
        ds/dt = (e*(1+s-r) - 3*s*r) * (1-s) * s

    while keeping the resilience dynamics unchanged.
    """

    def __init__(self):
        """Initialize the modified RS model."""
        e, s, r = self.e, self.s, self.r
        # Modified symptom dynamics with stronger resilience effect
        self.ds = (e * (1 + s - r) - 3 * s * r) * (1 - s) * s
        self.dr = (-s + (1 - s) * r) * (1 - r) * r
        self.model_name = "Modified RS model"


class Patient:
    """Individual patient with initial conditions and trajectory tracking.

    A Patient represents an individual experiencing depression dynamics
    according to an RS model. The patient has initial symptom and resilience
    levels and can be simulated under various external input scenarios.

    Attributes:
        r0: Initial resilience level (default: 0.84)
        s0: Initial symptom level (default: 0.67)
        name: Optional patient identifier
        model: The RSModel instance governing dynamics (default: RSModel())
        solution: OdeResult from scipy after simulation (set by get_stimulus_response)
    """

    def __init__(
        self,
        r0: float = 0.84,
        s0: float = 0.67,
        name: str = None,
        model: RSModel = None,
    ):
        """Initialize a patient with initial conditions.

        Args:
            r0: Initial resilience level in [0,1]
            s0: Initial depression symptom level in [0,1]
            name: Optional name/identifier for this patient
            model: RSModel instance (defaults to standard RSModel())
        """
        self.r0 = r0
        self.s0 = s0
        self.name = name
        self.model = model if model is not None else RSModel()
        self.solution = None

    def __str__(self) -> str:
        """String representation of the patient."""
        if self.name is None:
            return (
                f"A patient with initial condition s={self.s0:.2f} & "
                f"r={self.r0:.2f} based on {self.model}"
            )
        else:
            return (
                f"{self.name} with initial condition s={self.s0:.2f} & "
                f"r={self.r0:.2f} based on {self.model}"
            )

    def get_stimulus_response(
        self,
        external_input: Union[float, Callable[[float], float]] = 0,
        t_0: float = 0,
        t_final: float = 20,
        color_s: str = "blue",
        color_r: str = "green",
        color_e: str = "red",
        **kwargs,
    ):
        """Simulate patient response to external input and create plot.

        Solves the ODE system with the given external input function
        and plots the time evolution of all three variables (s, r, e).

        Args:
            external_input: Either a constant value or a function e(t)
            t_0: Initial time
            t_final: Final time
            color_s: Color for symptom trajectory
            color_r: Color for resilience trajectory
            color_e: Color for input signal
            **kwargs: Additional arguments passed to plt.plot()

        Returns:
            Matplotlib axes object with the stimulus-response plot
        """
        # Convert constant input to function if needed
        if not callable(external_input):
            _const = external_input
            external_input = lambda t: _const

        def rhs(t, x, e):
            """Wrapper for scipy's ODE solver."""
            dr, ds = self.model.rhs(x[0], x[1], e(t))
            return (dr, ds)

        # Solve the ODE
        self.solution = solve_ivp(
            rhs,
            (t_0, t_final),
            (self.r0, self.s0),
            t_eval=np.linspace(t_0, t_final, 300),
            dense_output=True,
            args=(external_input,),
        )

        # Extract solution
        r, s = self.solution.y
        t = self.solution.t
        e = [external_input(_) for _ in t]

        # Create plot
        plt.clf()
        plt.plot(
            t,
            s,
            label="Depression symptoms",
            color=color_s,
            linestyle="-",
            **kwargs,
        )
        plt.xlabel("Time")
        plt.ylabel("Magnitude")

        plt.plot(
            t,
            r,
            label="Resilience level",
            color=color_r,
            linestyle="--",
            **kwargs,
        )
        plt.plot(
            t,
            e,
            label="Adverse input",
            color=color_e,
            linestyle=":",
            **kwargs,
        )
        plt.legend()

        plt.title(f"{self.name} w/ $r_0={self.r0:.2f}$, $s_0={self.s0:.2f}$")

        ax = plt.gca()
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[
            [
                "left",
                "bottom",
            ]
        ].set_visible(True)
        # ax.set_xlim([t_0 - 1e-2, t_final + 3e-2])
        ax.set_xlim(min(t_0, t_final) - 1e-2, max(t_0, t_final) + 1e-2)
        ax.set_ylim([-1e-2, 1 + 1e-2])

        return ax
