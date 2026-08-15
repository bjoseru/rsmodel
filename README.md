# A Resilience–Symptom Model of Depression

Reproducible code for the manuscript

> Björn S. Rüffer & Michael Schönlein, *A mathematical model for depression and resilience*.

The **RS model** is a qualitative, two-state dynamical model of the interaction between
depressive symptoms and psychological resilience under external adversity:

$$\dot r = \bigl(-s + (1-s)\,r\bigr)(1-r)\,r$$

$$\dot s = \bigl(e\,(1+s-r) - s\,r\bigr)(1-s)\,s$$

with

| symbol | range | meaning |
| --- | --- | --- |
| $r$ | $[0,1]$ | resilience level ($0$ = depleted, $1$ = full) |
| $s$ | $[0,1]$ | depressive symptom level ($0$ = healthy, $1$ = severe) |
| $e$ | $[0,1]$ | external adverse input (stressor) |

The unit square $[0,1]^2$ is positively invariant.

> [!WARNING]
> Neither the model nor its time scale is calibrated against clinical data. This is a
> **qualitative** model, not a quantitative one, and it does not represent the effects of
> medication or of any other intervention. It is not a diagnostic or clinical tool.

## Quick start

The only prerequisite is [`uv`](https://docs.astral.sh/uv/getting-started/installation/).
No virtual environment, no `pip install`: each notebook carries its dependencies in a
[PEP 723](https://peps.python.org/pep-0723/) header, and `--sandbox` makes `uv` build a
throwaway environment from it.

```bash
git clone https://github.com/bjoseru/rsmodel.git
cd rsmodel

uvx marimo run  --sandbox notebooks/interactive_playground.py    # app view (read-only UI)
uvx marimo edit --sandbox notebooks/interactive_playground.py    # editable notebook
```

Swap in any of the three notebooks below. Use `run` to *use* a notebook and `edit` to see
and change the code.

## The notebooks

| notebook | what it does |
| --- | --- |
| [`notebooks/interactive_playground.py`](notebooks/interactive_playground.py) | The interactive companion to the paper. Three predefined adversity scenarios with sliders for the initial state $(s_0, r_0)$; a custom scenario where you *draw* the adverse input and optionally repeat it periodically; equilibrium and streamline plots with an adjustable constant input. Every figure has PDF/PNG/SVG download buttons. Has a slides layout — see below. |
| [`notebooks/mathematical_analysis.py`](notebooks/mathematical_analysis.py) | The symbolic analysis behind the manuscript, done with `sympy`: monotonicity conditions, Jacobian and stability of the four corner equilibria and of the interior equilibrium $p_5$, nullclines, Lyapunov functions (including $W$ for the despair equilibrium at $e = 0$), invariance of the triangle $T = \{s \ge r\}$, bounds used in the bliss stability proof, and the memory–symptom model variant. |
| [`notebooks/all_figures.py`](notebooks/all_figures.py) | Regenerates every figure used in the manuscript and writes them as PDF to `./figures/` (created on first run). Run this one with `uvx marimo run --sandbox` and let it execute to completion. |

`interactive_playground.py` opens in slides mode via
[`notebooks/layouts/interactive_playground.slides.json`](notebooks/layouts/interactive_playground.slides.json).
Keep that file next to the notebook, or marimo falls back to the normal vertical layout.

### Requirements

Python ≥ 3.12 for `interactive_playground.py` (it uses backslashes inside f-string
expressions, PEP 701); ≥ 3.11 for the other two. `uv` resolves this for you — the version
constraint is in each notebook's header.

## Repository layout

```
.
├── notebooks/
│   ├── interactive_playground.py
│   ├── mathematical_analysis.py
│   ├── all_figures.py
│   └── layouts/
│       └── interactive_playground.slides.json
├── rsmodel/                      # installable package, shared by all notebooks
│   ├── pyproject.toml
│   └── rsmodel/
│       ├── core.py               # RSModel, RS2Model, Patient
│       ├── analysis.py           # Jacobians, eigenvalues, Lyapunov verification
│       └── utils.py              # predefined scenarios, custom stimuli
├── molab/                        # generated single-file build (see below)
├── tools/
│   └── build_molab.py            # generator for molab/
└── LICENSE
```

The notebooks pull `rsmodel` in as an editable local dependency:

```toml
# [tool.uv.sources]
# rsmodel = { path = "../rsmodel", editable = true }
```

so edits under `rsmodel/rsmodel/` take effect on the next notebook run without reinstalling.

## Using `rsmodel` on its own

```bash
uv add --editable ./rsmodel        # or: uv pip install -e ./rsmodel
```

```python
from rsmodel import RSModel, Patient
from rsmodel.utils import get_predefined_scenarios

model = RSModel()
model.rhs(_r=0.84, _s=0.67, _e=0.3)      # -> (dr/dt, ds/dt)
model.plot_equilibria()                   # equilibrium manifold over e ∈ [0,1]
model.plot_streamlines(external_input=0.2)

patient = Patient(s0=0.67, r0=0.84)
patient.get_stimulus_response(get_predefined_scenarios()["multiple adverse events"])
```

Analysis helpers:

```python
from rsmodel.analysis import compute_jacobian, analyze_corner_equilibria, verify_lyapunov_function

J = compute_jacobian(RSModel())                       # symbolic 2×2 sympy.Matrix
analyze_corner_equilibria(RSModel(), e_value=0.5)     # stability of the four corners
```

`RS2Model` is the variant with the $3\,s\,r$ coupling term used for comparison in the paper.

## Running the playground on molab

[molab](https://molab.marimo.io) hosts a marimo notebook as a single file and resolves its
dependencies from PyPI, so it cannot follow the `[tool.uv.sources]` path override that
points at `../rsmodel`. [`tools/build_molab.py`](tools/build_molab.py) solves this by
inlining the package:

```bash
uv run tools/build_molab.py
# -> molab/interactive_playground_molab.py
```

The generated file is the original notebook with a `with app.setup:` block prepended. That
block holds the `rsmodel` sources verbatim as strings and registers them in `sys.modules`
before any cell runs, so every `import rsmodel` in the notebook body works unchanged. The
`rsmodel` dependency and the `[tool.uv.sources]` table are dropped from the PEP 723 header,
and `layout_file=` is removed because the layouts JSON is not uploaded. Nothing else
differs from `notebooks/interactive_playground.py`.

To publish: open [molab.marimo.io](https://molab.marimo.io), create a new notebook, and
paste or upload `molab/interactive_playground_molab.py`. No GitHub access is required, so
this works while the repository is still private.

The generated file is committed, which means it can go stale. Rebuild after any change to
`rsmodel/` or to the source notebook, and verify with:

```bash
uv run tools/build_molab.py --check     # non-zero exit + diff if stale
```

## License

MIT — see [LICENSE](LICENSE).

## Citation

```bibtex
@misc{rueffer_schoenlein_rs_model,
  author = {R{\"u}ffer, Bj{\"o}rn S. and Sch{\"o}nlein, Michael},
  title  = {A mathematical model for depression and resilience},
  year   = {2026},
  note   = {Code: \url{https://github.com/bjoseru/rsmodel}}
}
```
