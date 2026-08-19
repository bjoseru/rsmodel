# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "matplotlib>=3.8",
#     "numpy>=1.24",
#     "rsmodel>=0.1",
#     "scipy>=1.11",
#     "sympy>=1.12",
# ]
# ///

# Run with nothing installed but `uv`, from the repository root:
#   uvx marimo edit --sandbox notebooks/all_figures.py
# `--sandbox` builds a throwaway environment from the PEP 723 header above,
# which pulls rsmodel from PyPI. See the README for the local-checkout variant.
#
# All figures used in the manuscript are written to ./figures

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full", app_title="RS Model: Manuscript Figures")


@app.cell(hide_code=True)
def _(sample_and_hold):
    scenarios_dict = {
        "Chronic": {
            "stimulus": sample_and_hold(
                (0, 1),
                (10, 0.1),
            ),
            "r0": 0.21,
            "s0": 0.01,
        },
        "Delayed": {
            "stimulus": sample_and_hold(
                (0, 1),
                (5, 0.1),
            ),
            "r0": 0.2,
            "s0": 0.01,
        },
        "Recovery": {
            "stimulus": sample_and_hold(
                (0, 1),
                (9, 0.101),
            ),
            "r0": 0.30,
            "s0": 0.02,
        },
        "Resilience": {
            "stimulus": sample_and_hold(
                (0, 1),
                (10, 0.1),
            ),
            "r0": 0.95,
            "s0": 0.01,
        },
    }
    return (scenarios_dict,)


@app.cell(hide_code=True)
def _(Patient, mo, output_dir, plt, scenarios_dict):
    scenario_plots = {}
    full_scenarios = {}
    for scenario_selector in scenarios_dict.keys():
        scenario = Patient(
            r0=scenarios_dict[scenario_selector]["r0"],
            s0=scenarios_dict[scenario_selector]["s0"],
            name=rf"Scenario `{scenario_selector}`",
        )
        plt.figure()
        scene = scenario.get_stimulus_response(
            external_input=scenarios_dict[
                scenario_selector
            ]["stimulus"],
            t_0=0,
            t_final=50,
            linewidth=2,
        )
        scenario_plots[scenario_selector] = scene
        full_scenarios[scenario_selector] = scenario
        scene.figure.savefig(
            output_dir / f"scenario_{scenario_selector}.pdf"
        )
    mo.ui.tabs(scenario_plots)
    return (full_scenarios,)


@app.cell(hide_code=True)
def _(full_scenarios, line_styles, output_dir, plt):
    for i, (label, s) in enumerate(full_scenarios.items()):
        plt.plot(
            s.solution.t,
            s.solution.y[1],
            label=label,
            linestyle=line_styles[i % len(line_styles)],
            linewidth=2,
        )
        ax = plt.gca()
        ax.set_xlabel("time $t$")
        ax.set_ylabel("depression intensity $s(t)$")
        ax.legend()
    plt.fill(
        *zip(
            (0, 0),
            (50, 0),
            (50, 0.1),
            (10, 0.1),
            (10, 1),
            (0, 1),
            strict=False,
        ),
        color="lightgray",
        alpha=0.3,
        closed=True,
    )
    plt.fill(
        *zip(
            (0, 0),
            (50, 0),
            (50, 0.1),
            (5, 0.1),
            (5, 1),
            (0, 1),
            strict=False,
        ),
        color="lightgray",
        alpha=0.3,
        closed=True,
    )
    plt.fill(
        *zip(
            (0, 0),
            (50, 0),
            (50, 0.1),
            (9, 0.1),
            (9, 1),
            (0, 1),
            strict=False,
        ),
        color="lightgray",
        alpha=0.3,
        closed=True,
    )
    plt.savefig(output_dir / "scenario_comparison.pdf")
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(Patient, output_dir, plt, sample_and_hold):
    alterantive_scenarios = []
    for _stimulus in (
        sample_and_hold((0, 4.6), (30, 0)),  #
        sample_and_hold(
            (0, 4.6),
            (28, 1),
            (30, 1.05),
            (35, 1),
            (40, 1.01),
            (50, 1.05),
        ),  #
        sample_and_hold((0, 4.6), (30, 0.85), (60, 0.7)),  #
        sample_and_hold(
            (0, 4.6),
        ),
    ):
        p = Patient(r0=1, s0=0.01)
        p.get_stimulus_response(
            _stimulus, t_0=0, t_final=100, linewidth=2
        )
        alterantive_scenarios.append(p)
    plt.figure()
    for _a in alterantive_scenarios:
        plt.plot(
            _a.solution.t,
            _a.solution.y[1],
            linewidth=2,
            color="black",
        )
        _ax = plt.gca()
        _ax.set_xlabel("time $t$")
        _ax.set_ylabel("depression intensity $s(t)$")
    plt.savefig(output_dir / "alternative_scenarios.pdf")
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(plt):
    def snapshot_lines(ax=None):
        ax = ax or plt.gca()
        return [
            dict(
                x=_line.get_xdata().copy(),
                y=_line.get_ydata().copy(),
                label=_line.get_label(),
                color=_line.get_color(),
                linestyle=_line.get_linestyle(),
                linewidth=_line.get_linewidth(),
            )
            for _line in ax.get_lines()
        ]

    return (snapshot_lines,)


@app.cell(hide_code=True)
def _(Patient, sample_and_hold, snapshot_lines):
    recovery_again = Patient(
        name="Recovery from adverse input",
        r0=0.3,
        s0=0.02,
    )

    recovery_again.get_stimulus_response(
        sample_and_hold(
            (0, 1),
            (9, 0.101),
        ),
        t_0=0,
        t_final=50,
        linewidth=2,
    )
    recovery_again_plot = snapshot_lines()
    return recovery_again, recovery_again_plot


@app.cell(hide_code=True)
def _(Patient, np, plt, recovery_again, sample_and_hold, snapshot_lines):
    _t0 = 11

    _r0, _s0 = recovery_again.solution.sol(_t0)
    _recovery_again = Patient(
        name="Recovery with alternative past",
        r0=_r0,
        s0=_s0 + 0.00035,
    )

    recovery_stimulus = sample_and_hold(
        (-15, 1),
        (9, 0.101),
    )

    _recovery_again.get_stimulus_response(
        recovery_stimulus,
        t_0=_t0,
        t_final=50,
        linewidth=2,
    )
    _forward = snapshot_lines()

    _recovery_again.get_stimulus_response(
        recovery_stimulus,
        t_0=_t0,
        t_final=0,
        linewidth=2,
    )
    _backward = snapshot_lines()

    plt.clf()
    _seen_labels = set()
    for _line in _backward + _forward:
        _label = _line["label"]
        if _label in _seen_labels:
            _label = "_nolegend_"
        else:
            _seen_labels.add(_label)
        plt.plot(
            _line["x"],
            _line["y"],
            label=_label,
            color=_line["color"],
            linestyle=_line["linestyle"],
            linewidth=_line["linewidth"],
        )

    _all_t = np.concatenate(
        [l["x"] for l in _backward + _forward]
    )
    plt.xlim(_all_t.min(), _all_t.max())
    plt.legend()

    recovery_alternative_past_plot = snapshot_lines(
        plt.gca()
    )
    return (recovery_alternative_past_plot,)


@app.cell(hide_code=True)
def _(
    np,
    output_dir,
    plt,
    recovery_again_plot,
    recovery_alternative_past_plot,
):
    plt.clf()
    _seen_labels = set()
    for _line in (
        recovery_again_plot + recovery_alternative_past_plot
    ):
        _label = _line["label"]
        if _label in _seen_labels:
            _label = "_nolegend_"
        else:
            _seen_labels.add(_label)
        plt.plot(
            _line["x"],
            _line["y"],
            label=_label,
            color=_line["color"],
            linestyle=_line["linestyle"],
            linewidth=_line["linewidth"],
        )

    _all_t = np.concatenate(
        [
            l["x"]
            for l in recovery_again_plot
            + recovery_alternative_past_plot
        ]
    )
    plt.xlim(_all_t.min(), _all_t.max())
    plt.legend()
    plt.title(
        "Recovery with two alternative pasts ($t_0=11$)"
    )
    plt.gcf().savefig(
        output_dir / "recovery_alternative_pasts.pdf"
    )
    plt.gcf()
    return


@app.cell
def _(Patient, output_dir, plt):
    fbr = Patient(
        name="Fate by resilience level", r0=0.34, s0=0.15
    )
    fbr.get_stimulus_response(
        external_input=0.3, t_0=0, t_final=100, linewidth=2
    )
    plt.savefig(output_dir / "fate-by-resilience-level-1.pdf")
    plt.show()
    fbr = Patient(
        name="Fate by resilience level", r0=0.35, s0=0.15
    )
    fbr.get_stimulus_response(
        external_input=0.3, t_0=0, t_final=100, linewidth=2
    )
    plt.savefig(output_dir / "fate-by-resilience-level-2.pdf")
    plt.show()
    return


@app.cell
def _(Patient, output_dir, plt):
    fbs = Patient(
        name="Fate by resilience level", r0=0.35, s0=0.15
    )
    fbs.get_stimulus_response(
        external_input=0.3, t_0=0, t_final=100, linewidth=2
    )
    plt.savefig(
        output_dir / "fate-by-depression-symptom-level-1.pdf"
    )
    plt.show()
    fbs = Patient(
        name="Fate by resilience level", r0=0.35, s0=0.16
    )
    fbs.get_stimulus_response(
        external_input=0.3, t_0=0, t_final=100, linewidth=2
    )
    plt.savefig(
        output_dir / "fate-by-depression-symptom-level-2.pdf"
    )
    plt.show()
    return


@app.cell
def _(Patient, output_dir, plt, sample_and_hold):
    trigger_relapse = Patient(
        name="Triggering a relapse by adverse input",
        r0=0.83,
        s0=0.82,
    )
    trigger_relapse.get_stimulus_response(
        external_input=sample_and_hold(
            (0, 0.01),
        ),
        t_0=0,
        t_final=100,
        linewidth=2,
    )
    plt.savefig(output_dir / "trigger-relapse-1.pdf")
    plt.show()
    trigger_relapse.get_stimulus_response(
        external_input=sample_and_hold(
            (0, 0.01),
            (12, 0.3),
            (17, 0.01),
        ),
        t_0=0,
        t_final=100,
        linewidth=2,
    )
    plt.savefig(output_dir / "trigger-relapse-2.pdf")
    plt.show()
    return


@app.cell
def _(Patient, RSModel, mo, output_dir, plt, re, sample_and_hold):
    _title = "Sustained low-grade symptoms"
    _filename = re.sub(r"[^a-zA-Z0-9]", "-", _title).lower()

    # no stable interior point for constant input: integrate backwards from
    # the unstable interior equilibrium
    _e = 0.2

    _m = RSModel()
    _r0, _s0 = _m.get_equilibria()[-1]
    _r0, _s0 = _r0.subs({"e": _e}).n(), _s0.subs({"e": _e}).n()
    _patient = Patient(r0=_r0, s0=_s0)
    _adversity = sample_and_hold(
        (-1, 0.1),
        (10, 0.3),
        (20, _e),
    )
    _patient.get_stimulus_response(_adversity, t_0=100, t_final=0)

    _r0, _s0 = _patient.solution.sol(0)

    plt.title(f"{_title} w/ $r_0={_r0:.2f}$, $s_0={_s0:.2f}$")

    plt.savefig(output_dir / f"{_filename}.pdf", dpi=300)
    mo.md(f"""
        ## {_title}
        {mo.as_html(plt.gcf())}
        """)
    return


@app.cell
def _(Patient, mo, output_dir, plt, re):
    _title = "Sustained low-grade symptoms equilibrium $P_6$"
    _filename = re.sub(r"[^a-zA-Z0-9]+", "-", _title).lower()

    _patient = Patient(r0=0, s0=0.2)
    _patient.get_stimulus_response(0.0, t_0=0, t_final=100)

    plt.savefig(output_dir / f"{_filename}.pdf", dpi=300)
    mo.md(f"""
        ## {_title}
        {mo.as_html(plt.gcf())}
        """)
    return


@app.cell
def _(Patient, mo, output_dir, plt, re):
    _title = "Sustained low-grade symptoms equilibrium $P_7$"
    _filename = re.sub(r"[^a-zA-Z0-9]+", "-", _title).lower()

    _patient = Patient(r0=1, s0=0.2)
    _patient.get_stimulus_response(1.0, t_0=0, t_final=100)

    plt.savefig(output_dir / f"{_filename}.pdf", dpi=300)
    mo.md(f"""
        ## {_title}
        {mo.as_html(plt.gcf())}
        """)
    return


@app.cell
def _(Patient, mo, output_dir, plt, re, sample_and_hold):
    _title = "Pre-existing symptom improvement"
    _filename = re.sub(r"[^a-zA-Z0-9]", "-", _title).lower()

    _patient = Patient(r0=0.91, s0=0.9, name=_title)
    _adversity = sample_and_hold(
        (-1, 0.01),
    )
    _patient.get_stimulus_response(
        _adversity, t_0=0, t_final=100
    )
    plt.savefig(output_dir / f"{_filename}.pdf", dpi=300)
    mo.md(f"""
        ## {_title}
        {mo.as_html(plt.gcf())}
        """)
    return


@app.cell(hide_code=True)
def _(Patient, mo, output_dir, plt, re, sample_and_hold):
    _title = "Burnout"
    _filename = re.sub(r"[^a-zA-Z0-9]", "-", _title).lower()

    _patient = Patient(r0=0.23097017116, s0=0.15, name=_title)
    _adversity = sample_and_hold(
        (-1, 0.1),
    )
    _patient.get_stimulus_response(
        _adversity, t_0=0, t_final=100
    )
    plt.savefig(output_dir / f"{_filename}.pdf", dpi=300)
    mo.md(f"""
        ## {_title}
        {mo.as_html(plt.gcf())}
        """)
    return


@app.cell
def _(Patient, chain, mo, output_dir, plt, re, sample_and_hold):
    _title = "Multiple adversities and depression episodes"
    _filename = re.sub(r"[^a-zA-Z0-9]", "-", _title).lower()

    _patient = Patient(r0=0.5758142956844, s0=0.2, name=_title)

    _active = 3.0
    _inactive = 17.0
    _high, _low = 1.0, 0.1
    _period = _active + _inactive
    _repetitions = int(100.0 / _period) + 1

    _adversity = sample_and_hold(*chain(*(((_ * _period, _high), (_ * _period + _active, _low))
        for _ in range(_repetitions))))

    _patient.get_stimulus_response(
        _adversity, t_0=0, t_final=100
    )
    plt.savefig(output_dir / f"{_filename}.pdf", dpi=300)
    mo.md(f"""
        ## {_title}
        {mo.as_html(plt.gcf())}
        """)
    return


@app.cell
def _(Patient, mo, output_dir, plt, re, sample_and_hold):
    _title = "Universal threshold at r=s"
    _filename = re.sub(r"[^a-zA-Z0-9]", "-", _title).lower()

    _patient = Patient(r0=0.95, s0=0.95, name=_title)
    _adversity = sample_and_hold(
        (-1, 0.01),
    )
    _patient.get_stimulus_response(
        _adversity, t_0=0, t_final=100
    )
    plt.savefig(output_dir / f"{_filename}.pdf", dpi=300)
    mo.md(f"""
        ## {_title}
        {mo.as_html(plt.gcf())}
        """)
    return


@app.cell
def _(Patient, mo, np, output_dir, plt, re, sample_and_hold, snapshot_lines):
    _title = "Monotonicity"
    _filename = re.sub(r"[^a-zA-Z0-9]", "-", _title).lower()

    _patient = Patient(r0=0.6125, s0=0.45, name=_title)
    _adversity = sample_and_hold(
        (-1, 0.2),
        (10, 0.1),
        (20, 0.2),
        (30, 0.3),
    )
    _patient.get_stimulus_response(
        _adversity, t_0=0, t_final=40
    )

    _case1 = snapshot_lines()

    _offset = 0.025
    _patient = Patient(_patient.r0 + _offset, _patient.s0 - _offset, name=_title)
    _adversity = sample_and_hold(
        (-1, 0.2 - _offset),
        (5, 0.1 - _offset),
        (25, 0.2 - _offset),
        (35, 0.3 - _offset),
    )
    _patient.get_stimulus_response(
        _adversity, t_0=0, t_final=40
    )

    _case2 = snapshot_lines()

    plt.clf()
    _seen_labels = set()
    for _line in _case1 + _case2:
        _label = _line["label"]
        _color = _line["color"]
        if _label in _seen_labels:
            _label = "_nolegend_"
            _color = "black"
        else:
            _seen_labels.add(_label)
        plt.plot(
            _line["x"],
            _line["y"],
            label=_label,
            color=_color,
            linestyle=_line["linestyle"],
            linewidth=_line["linewidth"],
        )

    _all_t = np.concatenate(
        [l["x"] for l in _case1 + _case2]
    )
    plt.xlim(_all_t.min(), _all_t.max())
    plt.legend(loc=(0.3, 0.7))
    plt.title(r"Monotonicity w/ $r_0=0.61$, $s_0=0.45$ and again slighly shifted")

    plt.savefig(output_dir / f"{_filename}.pdf", dpi=300)
    mo.md(f"""
        ## {_title}
        {mo.as_html(plt.gcf())}
        """)
    return


@app.cell
def _(RSModel, np, output_dir, plt, sp):
    # eigenvalues of Jf(p5) as a function of e
    _m = RSModel()
    _J = sp.Matrix([_m.dr, _m.ds]).jacobian(
        sp.Matrix([_m.r, _m.s])
    )
    _r5, _s5 = _m.get_equilibria()[-1]
    _J_p5 = _J.subs({_m.r: _r5, _m.s: _s5})

    _p5_eigenvals = [
        (_e, sorted(_J_p5.subs(_m.e, _e).eigenvals().keys()))
        for _e in np.linspace(1e-6, 1 - 1e-6, 100)
    ]
    _p5_ev_1 = [(_e, _evs[0]) for _e, _evs in _p5_eigenvals]
    _p5_ev_2 = [(_e, _evs[1]) for _e, _evs in _p5_eigenvals]
    plt.figure()
    plt.plot(*zip(*_p5_ev_1), label=r"$\lambda_1$")
    plt.plot(
        *zip(*_p5_ev_2), label=r"$\lambda_2$", linestyle="--"
    )
    plt.gca().set_xlabel("External input $e$")
    plt.gca().set_ylabel(r"$\lambda_i$")
    plt.title("Eigenvalues of $Jf(p_5)$")
    plt.gca().legend()
    plt.grid()

    plt.savefig(output_dir / "eigenvalues-Jfp5.pdf")
    plt.gcf()
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import sympy as sp

    from rsmodel import Patient, RSModel
    from rsmodel.utils import sample_and_hold

    line_styles = ["-", "--", "-.", ":"]
    import re
    from pathlib import Path
    from itertools import chain

    output_dir = Path("./figures")
    output_dir.mkdir(exist_ok=True)
    return (
        Patient,
        RSModel,
        chain,
        line_styles,
        mo,
        np,
        output_dir,
        plt,
        re,
        sample_and_hold,
        sp,
    )


if __name__ == "__main__":
    app.run()
