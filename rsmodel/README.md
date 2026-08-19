# rsmodel

A qualitative, two-state dynamical model of the interaction between depressive symptoms
and psychological resilience under external adversity — the **resilience–symptom (RS)
model**:

```
dr/dt = (-s + (1-s)*r) * (1-r) * r
ds/dt = (e*(1+s-r) - s*r) * (1-s) * s
```

where `r ∈ [0,1]` is the resilience level (0 = depleted, 1 = full), `s ∈ [0,1]` the
depressive symptom level (0 = healthy, 1 = severe), and `e ∈ [0,1]` an external adverse
input. The unit square is positively invariant.

This is the reference implementation for

> Björn S. Rüffer & Michael Schönlein, *A mathematical model for depression and
> resilience*.

**Interactive playground, no installation required: <https://rsmodel.org>**

> **Warning**
> Neither the model nor its time scale is calibrated against clinical data. This is a
> qualitative model, not a quantitative one, and it does not represent the effects of
> medication or of any other intervention. It is not a diagnostic or clinical tool.

## Install

```bash
uv add rsmodel
```

## Usage

```python
from rsmodel import RSModel, Patient
from rsmodel.utils import get_predefined_scenarios

model = RSModel()
model.rhs(_r=0.84, _s=0.67, _e=0.3)         # -> (dr/dt, ds/dt)
model.plot_equilibria()                      # equilibrium manifold over e ∈ [0,1]
model.plot_streamlines(external_input=0.2)   # phase portrait at constant e

patient = Patient(s0=0.67, r0=0.84)
patient.get_stimulus_response(get_predefined_scenarios()["multiple adverse events"])
```

Symbolic analysis (`sympy`):

```python
from rsmodel.analysis import compute_jacobian, analyze_corner_equilibria

J = compute_jacobian(RSModel())                     # symbolic 2x2 Jacobian
analyze_corner_equilibria(RSModel(), e_value=0.5)   # stability of the four corners
```

`RS2Model` is the variant with the `3*s*r` coupling term used for comparison in the paper.

## Interactive notebooks

The repository ships three [marimo](https://marimo.io) notebooks — an interactive
playground (also published at <https://rsmodel.org>), the full symbolic analysis, and a
script that regenerates every figure in the manuscript. See
<https://github.com/bjoseru/rsmodel> for details.

## Citation

Cite the paper and the archived software:

```bibtex
@misc{rueffer_schoenlein_rsmodel_software,
  author    = {R{\"u}ffer, Bj{\"o}rn S. and Sch{\"o}nlein, Michael},
  title     = {{rsmodel}: a resilience--symptom dynamical model of depression},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.XXXXXXX},
  url       = {https://rsmodel.org}
}
```

## License

MIT
