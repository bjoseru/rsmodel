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
The layout is positional — one entry per cell — so reordering cells silently reshuffles
the slides rather than raising an error.

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
├── tools/
│   └── export_playground.py      # notebook -> static WASM site
├── .github/workflows/pages.yml   # rebuild + deploy on push
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

## Publishing the playground on the web

[`tools/export_playground.py`](tools/export_playground.py) turns the interactive
playground into a static WebAssembly site — it runs entirely in the visitor's browser via
[Pyodide](https://pyodide.org), with no Python install, no server and no backend:

```bash
uv run tools/export_playground.py            # -> build/site/
uv run tools/export_playground.py --serve    # ...and preview at localhost:8000
```

The script does three things and reports on each:

1. **Bundle.** The `rsmodel` package is inlined into a `with app.setup:` block that
   registers it in `sys.modules`, so the notebook's `import rsmodel` resolves with nothing
   installed. Pyodide cannot see this repository, and `[tool.uv.sources]` path overrides
   mean nothing to it, so vendoring is what makes the notebook portable. The `rsmodel`
   dependency and the path override are stripped from the PEP 723 header.
2. **Export.** `marimo export html-wasm --mode run --no-show-code` renders the bundle. The
   slides layout is staged as a sibling `.json` so marimo's own `inline_layout_file()`
   folds it into `index.html` — passing an already-inlined `data:` URI makes the exporter
   treat the base64 blob as a filename and fail with *File name too long*.
3. **Verify.** `index.html` is parsed back and checked: run mode, code hidden, slides
   layout present with one entry per cell, `rsmodel` actually embedded. Anything wrong is
   a hard failure rather than a quietly broken site.

Useful flags:

| flag | effect |
| --- | --- |
| `-o DIR` | output directory (default `build/site`) |
| `--serve` / `--port N` | serve the result locally when done |
| `--show-code` | show the code in the app instead of hiding it |
| `--execute` | run the notebook first and embed outputs, so the page shows content while Pyodide boots |
| `--no-hint` | suppress the deployment notes (used by CI) |

Any of the three notebooks can be passed as a positional argument.

### Deploying to GitHub Pages

Every asset path in the export is relative, so the site works unchanged at a user site
(`user.github.io`) or a project site (`user.github.io/rsmodel/`).

**With Actions** — [`.github/workflows/pages.yml`](.github/workflows/pages.yml) rebuilds
and deploys on every push that touches `notebooks/`, `rsmodel/rsmodel/` or the export
script. Enable it once under *Settings → Pages → Source → GitHub Actions*. Nothing
generated gets committed.

**Without Actions** — export into a committed folder:

```bash
uv run tools/export_playground.py -o docs
git add -f docs && git commit -m "publish site" && git push
```

then *Settings → Pages → Source → Deploy from a branch → main + /docs*. Note the `-f`:
`build/` and generated output are gitignored.

Caveats worth knowing:

- Pages on a **private** repository requires a paid GitHub plan; public repositories are free.
- The first load pulls Pyodide and the scientific stack (tens of MB) from a CDN. It is
  slow once, then browser-cached.
- `file://` will not work — WASM needs to be served over HTTP. Use `--serve` to test.
- Pyodide runs pure-Python wheels plus a set of precompiled scientific packages. numpy,
  scipy, matplotlib and sympy are supported; `drawdata` is a pure-Python `anywidget`, so
  it installs, but the drawing widget is the piece most worth clicking through locally
  before you publish.

### Will this still work in ten years?

Partly. The exported site splits into two halves with very different lifetimes.

**Your bytes — permanent.** Everything under `build/site/` (about 710 files, 26 MB: the
marimo frontend, fonts, icons, `index.html` with the notebook and `rsmodel` embedded) is
copied into the deployment. Nothing there expires. A GitHub Pages deployment keeps serving
until it is replaced or Pages is switched off; the Actions *artifact* that carried it has a
short retention, but its expiry does not take the live site down — it only means a redeploy
requires re-running the build.

**Third-party runtime — not under your control.** The page is a static shell that fetches
the Python runtime at load time. Three external dependencies, hardcoded in marimo's
compiled worker with no configuration hook to redirect them:

| fetched from | what for | if it disappears |
| --- | --- | --- |
| `cdn.jsdelivr.net/pyodide/v.../full/` | the Pyodide runtime and its scientific wheels | Python never boots |
| `wasm.marimo.app/pyodide-lock.json` | marimo's package lock for that Pyodide build | Python never boots |
| `pypi.org` (via `micropip`) | packages outside the lock, e.g. `drawdata` | that widget fails to load |

So the honest answer is that the interactive page depends on jsDelivr and on marimo
continuing to host a small JSON file. Neither is likely to vanish soon, and neither is a
promise.

Three things make this degrade gracefully rather than break:

1. **Build with `--execute`** (the Pages workflow does). Outputs are rendered into the HTML
   at build time, so a visitor sees the figures and the full text of the slides even if
   Pyodide never loads. Only the sliders and the drawing widget stop working.
2. **Archive the built site, not just the source.** `git add -f` a copy of `build/site`, or
   attach it to a tagged release, so the exact bytes that worked survive independently of
   any rebuild. A rebuild years from now may not reproduce — `uvx marimo` is unpinned and
   the action versions will have moved.
3. **Do not let the URL be the citable artifact.** Cite the repository (ideally with a
   Zenodo DOI, which mints an immutable archive of a tagged release) and offer the
   playground as a convenience link.

If you ever need true self-containment, the remaining option is to vendor Pyodide into the
site and patch the two hardcoded URLs in `build/site/assets/worker-*.js` after export. That
works but is brittle across marimo releases, so it is only worth doing once the paper is
final and the notebook has stopped changing.

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
