# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "matplotlib>=3.8",
#     "numpy>=1.24",
#     "rsmodel",
#     "scipy>=1.11",
#     "sympy>=1.12",
# ]
#
# [tool.uv.sources]
# rsmodel = { path = "../rsmodel", editable = true }
# ///

# Run without any local Python setup beyond `uv` (from rs-depression-model/):
#   uvx marimo edit --sandbox notebooks/mathematical_analysis.py

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full", app_title="RS Model: Mathematical Analysis")

with app.setup:
    # Initialization code that runs before all other cells
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import sympy as sp
    from rsmodel import RSModel


@app.cell(hide_code=True)
def _():
    # title
    mo.vstack(
        [
            mo.md(r"# Mathematical Analysis of the RS Model"),
            mo.md(
                r"### Theorem Verification and Stability Analysis"
            ),
            mo.md(r"#### Björn S. Rüffer & Michael Schönlein"),
        ],
        align="center",
        gap=2,
    )
    return


@app.cell
def _():
    # Define RS-model instance
    # (provides symbolic formulations of dr, ds, and parameters as well as numerical simulation)
    model = RSModel()

    # Define state vector
    x = sp.Matrix([model.r, model.s])
    f = sp.Matrix([model.dr, model.ds])
    return f, model, x


@app.cell(hide_code=True)
def _(f, model, x):
    mo.md(rf"""
    ## Model Definition

    The RS model is defined by the system of differential equations:

    $$\begin{{aligned}}
    &{model.latex_dr()}\\
    &{model.latex_ds()}\\
    \end{{aligned}}$$

    where $r \in [0,1]$ is the resilience level, $s \in [0,1]$ is the depression symptom level, and $e \geq 0$ is the external adverse input (the analysis below focuses on constant $e \in [0,1]$).

    ### State space symbolic formulation

    The state space formulation is

    $$\dot x = f(x,e)$$

    with
    - State vector: $x = {sp.latex(x)}$
    - Vector field: $f(x,e) = {sp.latex(f)}$
    """)
    return


@app.cell(hide_code=True)
def _(x):
    mo.md(rf"""
    ## Equilibria

    We compute all equilibrium points, i.e., points $x = {sp.latex(x)}$ with $f(x,e)=0$. These may depend on $e$ as a parameter.
    """)
    return


@app.cell
def _(model):
    # compute equilibria symbolically using sympy
    equilibria_raw = sp.solve(
        [model.dr, model.ds], [model.r, model.s], dict=True
    )

    equilibria_raw = sorted(
        sorted(
            equilibria_raw, key=str
        ),  # lexicographical order
        key=lambda _: len(str(_)),
        reverse=False,  # long formulas last
    )

    # ensure we always see them in the same order
    for _eq in equilibria_raw:
        print(_eq)
    return (equilibria_raw,)


@app.cell(hide_code=True)
def _(equilibria_raw):
    mo.md(rf"""
    The raw symbolic representation of these {len(equilibria_raw)} equilibria is
    ```
    {equilibria_raw}
    ```
    however, we need to filter out non-physical equilibria that fall outside the domain $[0,1]^2$.
    """)
    return


@app.cell
def _(equilibria_raw, model):
    # Filter out non-physical equilibria (outside [0,1]²)
    # The solver returns 7 equilibria, but 2 have s < 0:
    # - One has s = -1 (trivially non-physical)
    # - One has s = (-e - sqrt(5e²+4e))/(2e+2) < 0 for e > 0
    # We keep only equilibria where s is 0, 1, or the positive interior formula
    def _is_physical(eq):
        s_val = eq.get(model.s, None)
        # Check if s is exactly -1
        if s_val == -1:
            return False
        # Check if s is a constant 0 or 1 (corner equilibria)
        if s_val in (0, 1):
            return True
        # For symbolic expressions, check is e>=0 produces negatives values for r or s
        for _e_val in (0.1, 0.2, 0.3):
            if eq.get(model.s, None).subs(model.e, _e_val) < 0:
                return False
            if eq.get(model.r, None).subs(model.e, _e_val) < 0:
                return False
        return True


    equilibria = [
        eq for eq in equilibria_raw if _is_physical(eq)
    ]


    mo.md(
        f"""
    Found {len(equilibria)} physical equilibria (in or on boundary of $[0,1]^2$ and parameter dependent on $e$):
    """
        + "\n\n".join(
            [
                f"- $r = {sp.latex(eq[model.r])}$, $s = {sp.latex(eq[model.s])}$"
                for eq in equilibria
            ]
        )
    )
    return (equilibria,)


@app.cell(hide_code=True)
def _(equilibria, model):
    # Name the equilibria for reference (assign by value, not by solver order)
    if len(equilibria) != 5:
        raise ValueError(
            "Expecting exactly 5 equilibria, not more or less."
        )

    def _corner(_r_val, _s_val):
        (_match,) = [
            _eq
            for _eq in equilibria
            if _eq[model.r] == _r_val and _eq[model.s] == _s_val
        ]
        return _match

    p1 = _corner(0, 0)
    p2 = _corner(1, 0)
    p3 = _corner(1, 1)
    p4 = _corner(0, 1)
    (p5,) = [
        _eq for _eq in equilibria if _eq[model.r].free_symbols
    ]

    # p1 = (0,0) - healthy
    # p2 = (1,0) - resilient and healthy
    # p3 = (1,1) - resilient but depressed
    # p4 = (0,1) - depleted and depressed
    # p5 = interior equilibrium (depends on e)

    corner_equilibria = [p1, p2, p3, p4]
    interior_equilibrium = p5

    mo.md(
        r"""
    In accordance with the paper, we denote these equilibria as follows:

    $$\begin{aligned}
    """
        + "\\\\\n".join(
            rf" {_p_latex}  & \coloneqq \left({sp.latex(_p[model.r])}, {sp.latex(_p[model.s])}\right) "
            for _p_latex, _p in (
                ("p_1", p1),
                ("p_2", p2),
                ("p_3", p3),
                ("p_4", p4),
                ("p_5", p5),
            )
        )
        + "\n"
        + r"\end{aligned}$$"
    )
    return corner_equilibria, interior_equilibrium, p5


@app.cell(hide_code=True)
def _(model):
    # there are two more equilibria sets, that we did not discover using the above methods (as we were solving for r and s only, not for e):

    P6 = {model.r: 0, model.s: model.s}  # only if e == 0

    P7 = {model.r: 1, model.s: model.s}  # only if e == 1

    mo.md(rf"""In special circumstances, there are two additional sets of equilibria:

    - If $e=0$ then 
      $P_6 = \left\{{ ({sp.latex(P6[model.r])}, {sp.latex(P6[model.s])}) \colon s\in [0,1]\right\}}$ consists of equilibria and
    - when $e=1$ then 
      $P_7 = \left\{{ ({sp.latex(P7[model.r])}, {sp.latex(P7[model.s])}) \colon s\in [0,1]\right\}}$ consists of equilibria.
          """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Monotonicity Analysis

    We analyze the coupling between the two states by examining partial derivatives.
    """)
    return


@app.cell(hide_code=True)
def _(f, model):
    # Compute partial derivatives
    df1_ds = sp.diff(
        f[0], model.s
    )  # Effect of symptoms on resilience
    df2_dr = sp.diff(
        f[1], model.r
    )  # Effect of resilience on symptoms
    df1_de = sp.diff(
        f[0], model.e
    )  # Direct effect of input on resilience
    df2_de = sp.diff(
        f[1], model.e
    )  # Direct effect of input on symptoms

    mo.md(
        rf"""
    ### Partial derivatives

    The coupling structure is characterized by:

    - $\frac{{\partial f_1}}{{\partial s}} = {sp.latex(df1_ds.expand().collect(model.r))} = {sp.latex(df1_ds.expand().factor(model.r))} \leq0$
      - Symptoms negatively affect resilience dynamics

    - $\frac{{\partial f_2}}{{\partial r}} = {sp.latex(df2_dr)}\leq 0$
      - Resilience negatively affects symptom dynamics

    - $\frac{{\partial f_1}}{{\partial e}} = {sp.latex(df1_de)}$
      - External input has no direct effect on resilience

    - $\frac{{\partial f_2}}{{\partial e}} = {sp.latex(df2_de)}\geq0$
      - External input directly increases symptoms
    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Stability of Corner Equilibria

    We analyze stability properties of the four corner equilibria: $p_1$, $\ldots$, $p_4$.
    """)
    return


@app.cell
def _(corner_equilibria, f, model, x):
    J = f.jacobian(x)

    _corner_analysis_results = []
    for _i, _p in enumerate(corner_equilibria, 1):
        _J_p = J.subs(_p)
        _eigenvals = list(_J_p.eigenvals().keys())

        _corner_analysis_results.append(
            rf"""
    #### Corner point $p_{_i}=\begin{{pmatrix}}{_p[model.r]}\\ {_p[model.s]}\end{{pmatrix}}$

    Jacobian: $Jf(p_{_i})={sp.latex(_J_p)}$

    Eigenvalues: ${", ".join([sp.latex(ev) for ev in _eigenvals])}$
    """
        )

    mo.md("\n\n".join(_corner_analysis_results))
    return (J,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Stability of Interior Equilibrium $p_5$

    The interior equilibrium $p_5$ depends on the parameter $e$. We analyze how its eigenvalues change with $e$.
    """)
    return


@app.cell(hide_code=True)
def _(J, interior_equilibrium, model, p5):
    J_p5 = J.subs(interior_equilibrium)
    eigenvals_p5 = list(J_p5.eigenvals().keys())

    mo.md(
        rf"""
    ### Interior equilibrium

    At $p_5=\begin{{pmatrix}}{sp.latex(p5[model.r])}\\ {sp.latex(p5[model.s])}\end{{pmatrix}}$ the 
    Jacobian is

    $$Jf(p_5)={sp.latex(J_p5)}$$

    with Eigenvalues

    $${sp.latex(eigenvals_p5[0])}$$

    and

    $${sp.latex(eigenvals_p5[1])}.$$

    For specific values of $e$ this simplifies quite a bit:

    |e|Eigenvalue 1|Eigenvalue 2|
    |---|---|---|
    """
        + "\n".join(
            rf"|${_e:.2f}$| ${eigenvals_p5[0].subs(model.e, _e):.2f}$ | ${eigenvals_p5[1].subs(model.e, _e):.2f}$ | "
            for _e in (
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.85,
                0.9,
                0.95,
            )
        )
        + rf"""

    However, some of the values appear unreasonable and might be numerical artefacts. 

    """
    )
    return (J_p5,)


@app.cell(hide_code=True)
def _(J_p5, model):
    _p5_eigenvals = [
        (_e, sorted(J_p5.subs(model.e, _e).eigenvals().keys()))
        for _e in np.linspace(1e-6, 1 - 1e-6, 100)
    ]
    _p5_ev_1 = [(_e, _evs[0]) for _e, _evs in _p5_eigenvals]
    _p5_ev_2 = [(_e, _evs[1]) for _e, _evs in _p5_eigenvals]
    plt.plot(*zip(*_p5_ev_1), label=r"$\lambda_1$")
    plt.plot(
        *zip(*_p5_ev_2), label=r"$\lambda_2$", linestyle="--"
    )
    plt.gca().set_xlabel("External input $e$")
    plt.gca().set_ylabel(r"$\lambda_i$")
    plt.title("Eigenvalues of $Jf(p_5)$")
    plt.gca().legend()
    plt.grid()

    # figure written to file by all_figures.py

    mo.vstack(
        [
            mo.md(f"""
    So instead of evaluating the symbolic expressions, we first substitute the value of $e$ into $Jf(p_5)$ to obtain a numerical matrix. Computing the eigenvalues of this matrix is potentially more stable and we plot the results next."""),
            plt.gcf(),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Interpretation

    One eigenvalue is positive for all $e \in (0,1)$, indicating that $p_5$ is **unstable** (a saddle point).
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Lyapunov Function Analysis

    We verify the Lyapunov function $V = (1-r) + s$ for stability analysis.
    """)
    return


@app.cell
def _(f, model, x):
    V = (1 - model.r) + model.s

    grad_V = sp.Matrix([V]).jacobian(x)
    dV = (grad_V * f)[0]
    dV_expanded = dV.expand()
    dV_collected = dV_expanded.collect(model.s)

    mo.md(
        rf"""
    ### Lyapunov function candidate

    Let $V(r,s) = {sp.latex(V)}$

    Then $\nabla V = {sp.latex(grad_V)}$

    The derivative along trajectories is:

    $$\dot V = \nabla V \cdot f = {sp.latex(dV)}$$

    Expanded and collected by powers of $s$:

    $$\dot V = {sp.latex(dV_collected)}$$
    """
    )
    return (dV_collected,)


@app.cell
def _(dV_collected, model):
    # decomposition used in paper
    dV_Michael = (
        -(1 - model.r) * model.r**2
        + ((1 - model.r**2) * model.r + model.e * (1 - model.r))
        * model.s
        - model.r * (1 - model.e) * model.s**2
        - (model.e - model.r) * model.s**3
    )

    # Verify they're equal
    difference = (
        dV_Michael.expand() - dV_collected.expand()
    ).simplify()

    mo.md(
        rf"""
    ### Alternative form (decomposition shown in paper)

    $$\dot V = {sp.latex(dV_Michael)}$$

    Verification: difference = ${sp.latex(difference)}$ ✓
    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Nullclines

    We compute the nullclines of the system and their intersection, which recovers the interior equilibrium $p_5$.
    """)
    return


@app.cell
def _(model):
    # Interior equilibrium intersection point
    # From dr=0 (non-trivial): s = r/(1+r)
    # From ds=0 (non-trivial): s = (1-r)/(r/e-1)

    r_sym = model.r
    e_sym = model.e

    s_from_dr = r_sym / (1 + r_sym)
    s_from_ds = (1 - r_sym) / (r_sym / e_sym - 1)

    eq_intersection = sp.Eq(s_from_dr, s_from_ds)
    r_intersection_solutions = sp.solve(eq_intersection, r_sym)

    _sols = ", ".join(
        rf"${sp.latex(sol)}$"
        for sol in r_intersection_solutions
    )

    mo.md(
        rf"""
    ### Nullcline intersection

    The nullclines are:
    - From $\dot r = 0$: $s = \frac{{r}}{{1+r}}$
    - From $\dot s = 0$: $s = \frac{{1-r}}{{r/e-1}}$

    Setting these equal and solving for $r$:

    ${sp.latex(eq_intersection)}$

    Solutions: {_sols}

    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Lyapunov Function $W$ for Despair ($e=0$)

    We verify the Lyapunov function $W = r + (1-s)$ used in the proof of the stability of despair for $e=0$.
    """)
    return


@app.cell
def _(f, model, x):
    W = model.r + (1 - model.s)
    grad_W = sp.Matrix([W]).jacobian(x)
    dW = (grad_W * f)[0]
    dW_e0 = dW.subs(model.e, 0)

    # factored form used in the paper
    dW_paper = model.r * (
        ((1 - model.s) * model.r - model.s) * (1 - model.r)
        + (1 - model.s) * model.s**2
    )
    dW_check = (dW_e0 - dW_paper).simplify()

    mo.md(
        rf"""
    ### Derivative along trajectories

    Let $W(r,s) = {sp.latex(W)}$. For $e=0$:

    $$\dot W\big|_{{e=0}} = \nabla W \cdot f\big|_{{e=0}} = {sp.latex(sp.expand(dW_e0))}$$

    Factored form used in the paper:

    $$\dot W\big|_{{e=0}} = r \Big( \big( (1-s)r - s \big)(1-r) + (1-s)s^2 \Big)$$

    Verification: difference = ${sp.latex(dW_check)}$ ✓

    Note the **plus** sign in front of $r(1-s)s^2$: for $e=0$ one has $f_2 = -r s^2 (1-s) \leq 0$, and $\partial W/\partial s = -1$.
    """
    )
    return dW, dW_e0


@app.cell
def _(dW_e0, model):
    # grid check of the paper bound on U_delta with delta = 1/3
    delta_w = 1 / 3
    dW_fn = sp.lambdify((model.r, model.s), dW_e0, "numpy")
    _r = np.linspace(0, delta_w, 201)[:-1]  # r < delta
    _s = np.linspace(1 - delta_w, 1, 201)[1:]  # s > 1 - delta
    _R, _S = np.meshgrid(_r, _s, indexing="ij")
    _vals = dW_fn(_R, _S)

    mo.md(
        rf"""
    ### Grid check on $U_{{1/3}} = \{{(r,s) \colon r < \tfrac13,\ s > \tfrac23\}}$

    $\max \dot W = {_vals.max():.3g} \leq 0$; restricted to $r>0$: $\max \dot W = {_vals[_R > 0].max():.3g} < 0$. ✓

    (Equality $\dot W = 0$ holds exactly on $\{{r=0\}}$.)
    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Invariance of the Triangle $T = \{s \geq r\}$
    """)
    return


@app.cell
def _(dW, model):
    dW_diag = sp.factor(dW.subs(model.r, model.s))

    mo.md(
        rf"""
    Along the diagonal $s = r$ (general $e$):

    $$\dot W(s,s) = {sp.latex(dW_diag)} = (s^2 - s)\, e \leq 0 \quad \text{{for }} e \geq 0,\ s \in [0,1].$$

    Since $T = \{{s \geq r\}} = \{{W \leq 1\}}$, trajectories cannot cross the diagonal outward: $T$ is positively invariant.
    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Memory--Symptom Model

    Under the change of variables $m = 1-r$ (so $\dot m = -\dot r$) the RS model becomes the memory--symptom model. We verify the transformed vector field, its Kamke conditions, the interior equilibrium, and the invariant triangle.
    """)
    return


@app.cell
def _(f, model):
    m = sp.symbols("m")

    # transformed field via substitution r = 1 - m
    g = sp.Matrix(
        [-f[0].subs(model.r, 1 - m), f[1].subs(model.r, 1 - m)]
    )

    # forms displayed in the paper
    g_paper = sp.Matrix(
        [
            (model.s - (1 - model.s) * (1 - m)) * (1 - m) * m,
            (model.e * (model.s + m) - model.s * (1 - m))
            * (1 - model.s)
            * model.s,
        ]
    )
    g_check = sp.simplify(g - g_paper)

    mo.md(
        rf"""
    ### Vector field

    $$\begin{{pmatrix}} \dot m \\ \dot s \end{{pmatrix}} = g(m,s,e) = {sp.latex(g_paper)}$$

    Verification against the transformed RS model: difference = ${sp.latex(g_check.T)}$ ✓
    """
    )
    return g_paper, m


@app.cell
def _(g_paper, m, model):
    dg1_ds = sp.factor(sp.diff(g_paper[0], model.s))
    dg2_dm = sp.factor(sp.diff(g_paper[1], m))
    dg1_de = sp.diff(g_paper[0], model.e)
    dg2_de = sp.factor(sp.diff(g_paper[1], model.e))

    mo.md(
        rf"""
    ### Kamke conditions (south-west cone $K_m$)

    - $\frac{{\partial g_1}}{{\partial s}} = {sp.latex(dg1_ds)} = m(1-m)(2-m) \geq 0$
    - $\frac{{\partial g_2}}{{\partial m}} = {sp.latex(dg2_dm)} = s(1-s)(e+s) \geq 0$
    - $\frac{{\partial g_1}}{{\partial e}} = {sp.latex(dg1_de)}$
    - $\frac{{\partial g_2}}{{\partial e}} = {sp.latex(dg2_de)} = s(1-s)(s+m) \geq 0$

    matching the displays in the paper.
    """
    )
    return


@app.cell
def _(model, p5):
    # q5 = image of p5 under m = 1 - r
    q5_m = sp.simplify(1 - p5[model.r])
    q5_m_paper = (
        model.e + 2 - sp.sqrt(5 * model.e**2 + 4 * model.e)
    ) / (2 * (model.e + 1))
    q5_check = sp.simplify(q5_m - q5_m_paper)

    mo.md(
        rf"""
    ### Interior equilibrium $q_5$

    The $m$-component of $q_5 = (1 - p_5^{{(r)}},\, p_5^{{(s)}})$ matches the paper formula
    $\frac{{e + 2 - \sqrt{{5e^2+4e}}}}{{2(e+1)}}$ (difference = ${sp.latex(q5_check)}$ ✓), with endpoints
    $q_5(0) = ({sp.latex(q5_m.subs(model.e, 0))}, {sp.latex(p5[model.s].subs(model.e, 0))}) = q_2$ and
    $q_5(1) = ({sp.latex(q5_m.subs(model.e, 1))}, {sp.latex(p5[model.s].subs(model.e, 1))})$.
    """
    )
    return


@app.cell
def _(g_paper, m, model):
    # invariant triangle U = {m + s >= 1}: boundary m + s = 1
    d_mps_on_boundary = sp.factor(
        sp.simplify((g_paper[0] + g_paper[1]).subs(m, 1 - model.s))
    )

    # the set {m >= s} is NOT invariant: d/dt(m - s) on m = s
    d_mms_on_diag = sp.factor(
        sp.simplify((g_paper[0] - g_paper[1]).subs(model.s, m))
    )
    counterexample = d_mms_on_diag.subs(
        {m: sp.Rational(1, 10), model.e: 0}
    )

    mo.md(
        rf"""
    ### Invariant triangle

    The image of $T = \{{s \geq r\}}$ under $m = 1-r$ is $U = \{{m + s \geq 1\}}$. On its boundary $m+s=1$:

    $$\tfrac{{d}}{{dt}}(m+s) = {sp.latex(d_mps_on_boundary)} = e\,s(1-s) \geq 0,$$

    so trajectories cannot leave $U$: it is positively invariant.

    By contrast, $\{{m \geq s\}}$ is **not** invariant: on $m=s$,

    $$\tfrac{{d}}{{dt}}(m-s) = {sp.latex(d_mms_on_diag)},$$

    which is negative e.g. at $m=s=\tfrac{{1}}{{10}}$, $e=0$: value ${sp.latex(counterexample)} < 0$.
    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Bounds Used in the Bliss Stability Proof

    The proof of the (asymptotic) stability of bliss bounds $\dot V = p_r(s)$ by $a_1(r) \leq 3(1-r)$ and $a_2(r)s^2 + a_3(r)s^3 \leq (1-r)s^2$, so that $\dot V \leq (1-r)(-r^2 + 3s + s^2) < 0$ on $\Omega_{1/6} \cap \{r < 1\}$, uniformly in $e \in [0,1]$.
    """)
    return


@app.cell
def _(dV_collected, model):
    dV_bound = (1 - model.r) * (
        -model.r**2 + 3 * model.s + model.s**2
    )
    _gap_fn = sp.lambdify(
        (model.r, model.s, model.e),
        dV_bound - dV_collected,
        "numpy",
    )
    _grid = np.linspace(0, 1, 51)
    _R, _S, _E = np.meshgrid(_grid, _grid, _grid, indexing="ij")
    gap_min = _gap_fn(_R, _S, _E).min()

    _dV_fn = sp.lambdify(
        (model.r, model.s, model.e), dV_collected, "numpy"
    )
    delta_v = 1 / 6
    _r2 = np.linspace(1 - delta_v, 1, 101)[1:-1]  # 1-delta < r < 1
    _s2 = np.linspace(0, delta_v, 101)[:-1]  # 0 <= s < delta
    _R2, _S2, _E2 = np.meshgrid(_r2, _s2, _grid, indexing="ij")
    _omega = (1 - _R2) + _S2 < delta_v
    dV_max_omega = _dV_fn(_R2, _S2, _E2)[_omega].max()

    mo.md(
        rf"""
    Grid checks:

    - $\min\big[(1-r)(-r^2+3s+s^2) - \dot V\big] = {gap_min:.3g}$ on $[0,1]^3$ (nonnegative up to floating point) ✓
    - $\max \dot V = {dV_max_omega:.3g} < 0$ on $\Omega_{{1/6}} \cap \{{r<1\}}$ for all $e \in [0,1]$ ✓
    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Interactive Analysis

    Use the slider below to visualize the vector field and nullclines for different values of $e$.
    """)
    return


@app.cell
def _():
    e_slider = mo.ui.slider(
        0.01, 0.99, 0.01, 0.2, label="External input e"
    )
    e_slider
    return (e_slider,)


@app.cell
def _(e_slider, model, p5):
    _e_val_plot = e_slider.value

    # Create meshgrid
    _r_grid, _s_grid = np.mgrid[0:1:20j, 0:1:20j]

    # Compute vector field
    _dr_grid = np.zeros_like(_r_grid)
    _ds_grid = np.zeros_like(_s_grid)

    for _i in range(_r_grid.shape[0]):
        for _j in range(_r_grid.shape[1]):
            _r_val = _r_grid[_i, _j]
            _s_val = _s_grid[_i, _j]
            _dr_val = float(
                model.dr.subs(
                    {model.r: _r_val, model.s: _s_val}
                )
            )
            _ds_val = float(
                model.ds.subs(
                    {
                        model.r: _r_val,
                        model.s: _s_val,
                        model.e: _e_val_plot,
                    }
                )
            )
            _dr_grid[_i, _j] = _dr_val
            _ds_grid[_i, _j] = _ds_val

    fig_vec, _ax_vec = plt.subplots(figsize=(6.4, 6.4))

    # Vector field
    _ax_vec.quiver(
        _r_grid, _s_grid, _dr_grid, _ds_grid, alpha=0.5
    )

    # Nullclines
    _r_range = np.linspace(0.001, 0.999, 200)

    # dr=0 nullcline: s = r/(1+r)
    _s_nullcline_dr = _r_range / (1 + _r_range)
    _ax_vec.plot(
        _r_range,
        _s_nullcline_dr,
        "b-",
        linewidth=2,
        label=r"$\dot r = 0$",
    )

    # ds=0 nullcline: s = (1-r)/(r/e-1)
    _r_range_ds = _r_range[_r_range > _e_val_plot + 0.01]
    _s_nullcline_ds = (1 - _r_range_ds) / (
        _r_range_ds / _e_val_plot - 1
    )
    _valid = (_s_nullcline_ds >= 0) & (_s_nullcline_ds <= 1)
    _ax_vec.plot(
        _r_range_ds[_valid],
        _s_nullcline_ds[_valid],
        "r-",
        linewidth=2,
        label=r"$\dot s = 0$",
    )

    _ax_vec.set_xlim(0, 1)
    _ax_vec.set_ylim(0, 1)
    _ax_vec.set_xlabel("Resilience $r$")
    _ax_vec.set_ylabel("Symptoms $s$")
    _ax_vec.set_title(
        f"Vector field and nullclines for $e={_e_val_plot:.2f}$"
    )
    _ax_vec.legend()
    _ax_vec.grid(True, alpha=0.3)

    plt.tight_layout()

    _ax_vec.plot(0, 1, "ro", markersize=8)  # red circle
    _ax_vec.annotate(
        "$p_4$=despair",
        xy=(0, 1),
        xytext=(-25, 20),
        arrowprops=dict(
            arrowstyle="->", connectionstyle="arc3,rad=0"
        ),
        textcoords="offset points",
    )

    _ax_vec.plot(1, 0, "bo", markersize=8)  # blue circle
    _ax_vec.annotate(
        "$p_2$=bliss",
        xy=(1, 0),
        xytext=(25, 20),
        arrowprops=dict(
            arrowstyle="->", connectionstyle="arc3,rad=0"
        ),
        textcoords="offset points",
    )

    _ax_vec.plot(1, 1, "ko", markersize=8)  # black circle
    _ax_vec.annotate(
        "$p_3$",
        xy=(1, 1),
        xytext=(25, 20),
        arrowprops=dict(
            arrowstyle="->", connectionstyle="arc3,rad=0"
        ),
        textcoords="offset points",
    )

    _ax_vec.plot(0, 0, "ko", markersize=8)  # black circle
    _ax_vec.annotate(
        "$p_1$",
        xy=(0, 0),
        xytext=(-25, 20),
        arrowprops=dict(
            arrowstyle="->", connectionstyle="arc3,rad=0"
        ),
        textcoords="offset points",
    )

    _xy = (
        p5[model.r].subs(model.e, _e_val_plot),
        p5[model.s].subs(model.e, _e_val_plot),
    )

    _ax_vec.plot(*_xy, "ko", markersize=8)  # black circle
    _ax_vec.annotate(
        "$p_5$",
        xy=_xy,
        xytext=(25, 20),
        arrowprops=dict(
            arrowstyle="->", connectionstyle="arc3,rad=0"
        ),
        textcoords="offset points",
    )

    fig_vec
    return


if __name__ == "__main__":
    app.run()
