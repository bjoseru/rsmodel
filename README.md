# A Resilience–Symptom Model of Depression

[![playground](https://img.shields.io/badge/playground-rsmodel.org-2f6f4e)](https://rsmodel.org)
[![PyPI](https://img.shields.io/pypi/v/rsmodel)](https://pypi.org/project/rsmodel/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22018288.svg)](https://doi.org/10.5281/zenodo.22018288)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Reproducible code for the manuscript

> Björn S. Rüffer & Michael Schönlein, *A mathematical model for depression and resilience*.

**Try it in your browser: <https://rsmodel.org>** — no installation, nothing to sign up for.

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

> [!NOTE]
> Always pass `--sandbox`. It is what makes `uv` build the environment from the PEP 723
> header; without it marimo falls back to its own installer and to whatever happens to be
> on your `PYTHONPATH`.

`rsmodel` is resolved from PyPI, so the notebooks work from a clean clone — or from no
clone at all, straight off a raw URL:

```bash
uvx marimo edit --sandbox https://raw.githubusercontent.com/bjoseru/rsmodel/main/notebooks/interactive_playground.py
```

### Working on `rsmodel` itself

If you are changing the package and want a notebook to pick your edits up, point its
header at the local checkout for the duration:

```bash
uv add --script notebooks/interactive_playground.py --editable ./rsmodel
# ... edit rsmodel/rsmodel/*.py, run the notebook, repeat ...
git checkout -- notebooks/interactive_playground.py     # back to the PyPI release
```

That rewrites the `[tool.uv.sources]` block in the header. **Do not commit it**: a CI job
rejects any notebook whose header still carries a path override, because such a notebook
only runs inside a checkout.

## The notebooks

| notebook | what it does |
| --- | --- |
| [`notebooks/interactive_playground.py`](notebooks/interactive_playground.py) | The interactive companion to the paper, and the notebook published at [rsmodel.org](https://rsmodel.org). See below. |
| [`notebooks/mathematical_analysis.py`](notebooks/mathematical_analysis.py) | The symbolic analysis behind the manuscript, done with `sympy`: monotonicity conditions, Jacobian and stability of the four corner equilibria and of the interior equilibrium $p_5$, nullclines, Lyapunov functions (including $W$ for the despair equilibrium at $e = 0$), invariance of the triangle $T = \{s \ge r\}$, bounds used in the bliss stability proof, and the memory–symptom model variant. |
| [`notebooks/all_figures.py`](notebooks/all_figures.py) | Regenerates every figure used in the manuscript and writes them as PDF to `./figures/` (created on first run). Run it with `uvx marimo run --sandbox` and let it execute to completion. Support material for the article: it is not exercised by CI and is not maintained beyond publication. |

### What the playground contains

Four panels of content plus three of front matter, in one long single-column page
(`width="medium"`). There is deliberately **no slides layout**: a slide deck makes it
awkward to put the disclaimer, the Impressum and the Datenschutzerklärung where they
belong, and the vertical scroll keeps them one page away from anything else.

1. **Pre-defined scenarios** — a tab per adversity scenario from
   `rsmodel.utils.get_predefined_scenarios()`, with vertical sliders for the initial
   symptom level $s_0$ and initial resilience $r_0$.
2. **Custom scenario** — *draw* the adverse input into a `drawdata` bar widget, choose the
   simulated time span $t_f$ and a number of repetitions $n$ to model daily, weekly or
   otherwise recurring exposure. The simulation runs over $n\cdot t_f$.
3. **Phase-space view** — streamline plot of the flow at a constant input $e$, with a
   slider for $e$ and the model's equations rendered alongside.
4. Every figure carries **PDF / PNG / SVG download buttons**, with the parameter values
   baked into the filename.
5. **License**, **Impressum & Datenschutzerklärung** (required for a site served from
   Germany) and a **disclaimer** callout close the notebook.

### Requirements

Python ≥ 3.12 for `interactive_playground.py` — the disclaimer cell puts a backslash
inside an f-string expression, which needs [PEP 701](https://peps.python.org/pep-0701/).
Python ≥ 3.11 for the other two, and for the `rsmodel` package itself. `uv` resolves this
for you; the constraint lives in each notebook's header.

## Repository layout

```
.
├── notebooks/
│   ├── interactive_playground.py
│   ├── mathematical_analysis.py
│   └── all_figures.py
├── rsmodel/                      # installable package, shared by all notebooks
│   ├── pyproject.toml
│   └── rsmodel/
│       ├── __init__.py           # __version__ lives here: the single source of truth
│       ├── core.py               # RSModel, RS2Model, Patient
│       ├── analysis.py           # Jacobians, eigenvalues, Lyapunov verification
│       └── utils.py              # predefined scenarios, custom stimuli
├── tools/
│   └── export_playground.py      # notebook -> static WASM site
├── web/                          # Cloudflare Pages host config, copied into the export
│   ├── _headers
│   └── _redirects
├── .github/workflows/
│   ├── ci.yml                    # package builds + imports, export pipeline, secret scan
│   ├── site.yml                  # rebuild + deploy to Cloudflare Pages on push
│   └── release.yml               # tag -> PyPI (trusted publishing) -> GitHub Release -> Zenodo
├── CHANGELOG.md
├── CITATION.cff                  # how to cite
├── .zenodo.json                  # metadata for the archived release
└── LICENSE
```

The notebooks pull `rsmodel` in as an editable local dependency:

```toml
# [tool.uv.sources]
# rsmodel = { path = "../rsmodel", editable = true }
```

so edits under `rsmodel/rsmodel/` take effect on the next notebook run without
reinstalling.

## What is on PyPI

The [`rsmodel`](https://pypi.org/project/rsmodel/) distribution is the package and nothing
else — the notebooks, the export tooling and the CI configuration stay in this repository:

```
wheel                       sdist
rsmodel/__init__.py         rsmodel/{__init__,core,analysis,utils}.py
rsmodel/core.py             pyproject.toml
rsmodel/analysis.py         README.md          <- rsmodel/README.md, the PyPI page
rsmodel/utils.py            LICENSE
LICENSE (dist-info)
```

Note that `rsmodel/README.md` — not the file you are reading — is what PyPI renders.

## Using `rsmodel` on its own

From PyPI:

```bash
uv add rsmodel
```

or against this checkout:

```bash
uv add --editable ./rsmodel
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

The script does four things and reports on each:

1. **Bundle.** The `rsmodel` package is inlined into a `with app.setup:` block that
   registers it in `sys.modules`, so the notebook's `import rsmodel` resolves with nothing
   installed, and the `rsmodel` entry is stripped from the PEP 723 header. Pyodide *could*
   `micropip`-install `rsmodel` from PyPI instead, but vendoring is better on both counts:
   it removes a network dependency at page load, and it guarantees the deployed app runs
   exactly the source in this repository rather than the last release. The site therefore
   tracks `main`, while `uvx marimo edit --sandbox` gives you the released version.
2. **Export.** `marimo export html-wasm --mode run --no-show-code` renders the bundle.
   With `--execute`, marimo has to *run* every cell, so the export is handed to
   `uv run --isolated --no-project --with ...` using the dependency list and the
   `requires-python` floor read back off the bundled notebook — no pre-built environment
   needed on the machine doing the export.
3. **Host config.** Everything in `web/` (`_headers`, `_redirects`) is copied into the
   export root, where Cloudflare Pages picks it up. Other hosts ignore those files.
4. **Verify.** `index.html` is parsed back and checked: run mode, code hidden, layout
   entries consistent with the cell count if a layout is in use, `rsmodel` actually
   embedded. Anything wrong is a hard failure rather than a quietly broken site.

Useful flags:

| flag | effect |
| --- | --- |
| `-o DIR` | output directory (default `build/site`) |
| `--serve` / `--port N` | serve the result locally when done |
| `--show-code` | show the code in the app instead of hiding it |
| `--execute` | run the notebook first and embed outputs, so the page shows content while Pyodide boots |
| `--no-hint` | suppress the deployment notes (used by CI) |

Any notebook without a `with app.setup:` block of its own can be passed as a positional
argument — that is `interactive_playground.py` and `all_figures.py`.
`mathematical_analysis.py` already defines one, and the vendored package would have to be
merged into it by hand, so the script refuses rather than guess. A current export is
about **740 files and 28 MB**, largest single file under 5 MB — comfortably inside
Cloudflare Pages' limits of 20,000 files and 25 MiB per file per deployment.

### Deploying to Cloudflare Pages

Every asset path in the export is relative, so the site works unchanged at `rsmodel.org`,
at a `*.pages.dev` preview URL, or under a subpath.

**With Actions** — [`.github/workflows/site.yml`](.github/workflows/site.yml) rebuilds with
`--execute` and deploys on every push to `main` that touches `notebooks/`,
`rsmodel/rsmodel/`, `tools/` or `web/`. It needs two repository secrets:

| secret | where it comes from |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | Cloudflare dashboard → My Profile → API Tokens, permission *Account → Cloudflare Pages → Edit* |
| `CLOUDFLARE_ACCOUNT_ID` | the hex string in the Cloudflare dashboard URL |

Both live in GitHub's encrypted secret store. **Nothing secret is ever committed to this
repository.** Nothing generated is committed either.

**Without Actions** — from a checkout:

```bash
uv run tools/export_playground.py --execute
npx wrangler pages deploy build/site --project-name=rsmodel
```

`wrangler` keeps its own OAuth credentials in `~/.wrangler`, outside the repository.

Caveats worth knowing:

- The first load pulls Pyodide and the scientific stack (tens of MB) from a CDN. It is
  slow once, then browser-cached.
- `file://` will not work — WASM needs to be served over HTTP. Use `--serve` to test.
- Pyodide runs pure-Python wheels plus a set of precompiled scientific packages. numpy,
  scipy, matplotlib and sympy are supported; `drawdata` is a pure-Python `anywidget`, so
  it installs, but the drawing widget is the piece most worth clicking through locally
  before you publish.
- `web/_headers` deliberately sets **no** Content-Security-Policy: Pyodide needs
  `unsafe-eval` and `wasm-unsafe-eval` and fetches its runtime from a third-party CDN, so
  a policy tight enough to be worth having would break the notebook.

### Will this still work in ten years?

Partly. The exported site splits into two halves with very different lifetimes.

**Your bytes — permanent.** Everything under `build/site/` (about 740 files, 28 MB: the
marimo frontend, fonts, icons, `index.html` with the notebook and `rsmodel` embedded) is
copied into the deployment. Nothing there expires; a Cloudflare Pages deployment keeps
serving until it is replaced.

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

1. **Build with `--execute`** (the deploy workflow does). Outputs are rendered into the
   HTML at build time, so a visitor sees the figures and the full text even if Pyodide
   never loads. Only the sliders and the drawing widget stop working.
2. **Archive the source, not just the URL.** Every tagged release is deposited on Zenodo
   (see below), which mints an immutable DOI. A rebuild years from now may not reproduce —
   `uvx marimo` is unpinned and the action versions will have moved — but the source that
   produced this site is preserved.
3. **Do not let the URL be the citable artifact.** Cite the DOI; offer `rsmodel.org` as a
   convenience link.

If you ever need true self-containment, the remaining option is to vendor Pyodide into the
site and patch the two hardcoded URLs in `build/site/assets/worker-*.js` after export. That
works but is brittle across marimo releases, so it is only worth doing once the paper is
final and the notebook has stopped changing.

## Versioning and releases

`rsmodel/rsmodel/__init__.py` holds `__version__`; `hatchling` reads it, so the package
version has exactly one source. Releases are [semantic](https://semver.org/) and recorded
in [`CHANGELOG.md`](CHANGELOG.md).

To cut a release:

```bash
# 1. bump the version and write the changelog entry
$EDITOR rsmodel/rsmodel/__init__.py CHANGELOG.md CITATION.cff
git commit -am "release 0.2.0"

# 2. tag it -- the tag must match __version__ or CI refuses to publish
git tag -a v0.2.0 -m "rsmodel 0.2.0"
git push origin main v0.2.0
```

[`release.yml`](.github/workflows/release.yml) then checks the tag against `__version__`,
builds an sdist and a wheel with `uv build --no-sources`, publishes to PyPI via
[trusted publishing](https://docs.pypi.org/trusted-publishers/) (PyPI verifies a GitHub
OIDC token — there is no API token to store anywhere), and finally creates a GitHub
Release. Zenodo is subscribed to that release and archives the tagged source.

## Citation

Please cite the paper and the software. [`CITATION.cff`](CITATION.cff) carries the
machine-readable version; GitHub renders a "Cite this repository" button from it.

```bibtex
@misc{rueffer_schoenlein_rsmodel_software,
  author    = {R{\"u}ffer, Bj{\"o}rn S. and Sch{\"o}nlein, Michael},
  title     = {{rsmodel}: a resilience--symptom dynamical model of depression},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.22018288},
  url       = {https://rsmodel.org},
  note      = {Code: \url{https://github.com/bjoseru/rsmodel}}
}
```

The DOI above is the **concept DOI**: it always resolves to the newest archived version.
Each release additionally gets its own version DOI, which is what to cite when the exact
state matters.

## License

MIT — see [LICENSE](LICENSE).
