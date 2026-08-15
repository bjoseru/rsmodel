# /// script
# requires-python = ">=3.12"  # PEP 701: backslashes inside f-string expressions
# dependencies = [
#     "drawdata==0.3.8",
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
#   uvx marimo edit --sandbox notebooks/interactive_playground.py

import marimo

__generated_with = "0.23.16"
app = marimo.App(
    width="medium",
    app_title="The Reslience–Symptom Model of Depression",
    layout_file="layouts/interactive_playground.slides.json",
)


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(r"# A Resilience–Symptom Model of Depression"),
            mo.md(r"### Björn S. Rüffer & Michael Schönlein"),
            mo.md(r"#### Bauhaus-Universität Weimar"),
            mo.md("2026"),
        ],
        align="center",
        justify="space-around",
        gap=3,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Scenarios for individual patients
    """)
    return


@app.cell(hide_code=True)
def _(mo, stimuli):
    mo.md(rf"""
    ### Predefined scenarios

    We consider three fixed scenarios that help explain features of the model. The scenarios are defined by particular external input signals modeling adverse events affecting an individual:

    {"    \n".join(map(lambda s: "- _"+s+"_", stimuli.keys()))}.

    For each input signal, you can investigate how an individual with given initial levels of depression and resilience will react.

    The response typically depends on the combination of these two parameters. For each input signal, both outcomes—recovery ($s$ declines towards zero) and development of severe depression ($s$ approaches $1$)—are possible depending on initial configuration.
    """)
    return


@app.cell(hide_code=True)
def _(Patient, download_buttons, mo, r0_slider, s0_slider, stimuli):
    def scenario_tab(title, stimulus):
        patient = Patient(s0=s0_slider.value, r0=r0_slider.value)
        stimulus_response = patient.get_stimulus_response(stimulus)

        return mo.hstack(
            [
                stimulus_response,
                mo.vstack(
                    [
                        mo.hstack(
                            [
                                mo.vstack(
                                    [
                                        mo.md("$s_0$"),
                                        mo.md(f"☹️"),
                                        s0_slider,
                                        mo.md(f"🙂"),
                                        mo.md(f"${s0_slider.value:.2f}$"),
                                    ],
                                    align="center",
                                ),
                                mo.vstack(
                                    [
                                        mo.md("$r_0$"),
                                        mo.md(f"🔋"),
                                        r0_slider,
                                        mo.md(f"🪫"),
                                        mo.md(f"${r0_slider.value:.2f}$"),
                                    ],
                                    align="center",
                                ),
                            ]
                        ),
                        download_buttons(
                            stimulus_response,
                            basename=f"response_{title.replace(' ', '_')}_s0={s0_slider.value:.2f}_r0={r0_slider.value:.2f}",
                            style="v",
                        ),
                    ],
                    align="center",
                ),
            ],
            widths=[12, 1],
        )

    mo.ui.tabs({k: scenario_tab(k, v) for k, v in stimuli.items()})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ### Make your own custom scenario

    In the following scenario, you can define an "adverse input" graphically by drawing into a figure. The response of the patient is shown in the plot next to the input figure.

    There are options to adjust the time span of the simulation and whether the custom input should be extended periodically, e.g., to model daily, weekly, or otherwise repeated exposures to adverse circumstances.

    {mo.callout(mo.md("Note that neither the model as a whole nor the time scale are in any way calibrated and should hence be seen as abstractions.\n\n This is a qualitative model, not a quantitative one.\n\n __This model does not consider the possible benefits of medication or interventions.__"), kind='danger')}
    """)
    return


@app.cell(hide_code=True)
def _(
    Patient,
    custom_stimulus,
    download_buttons,
    mo,
    num_periods,
    r0_slider_custom,
    s0_slider_custom,
    stimulus_input,
    tf_slider,
):
    def custom_scenario():
        patient = Patient(s0=s0_slider_custom.value, r0=r0_slider_custom.value)
        stimulus_response = patient.get_stimulus_response(
            custom_stimulus,
            t_final=tf_slider.value * num_periods.value,
        )
        return mo.hstack(
            [
                mo.vstack(
                    [
                        stimulus_response,
                        mo.md(
                            rf"""
    Draw into this figure to define the adverse input. Only values up to time ${tf_slider.value}$ will be used in the simulation.
    """
                        ),
                        stimulus_input,
                    ]
                ),
                mo.vstack(
                    [
                        mo.md(rf"$t_f={tf_slider.value}$"),
                        tf_slider,
                        mo.md(f"""number of repetitions:\n\n$n={num_periods.value}$"""),
                        num_periods,
                        mo.md(
                            f"simulated time span is thus\n\n $n\\cdot t_f={tf_slider.value * num_periods.value}$"
                        ),
                        mo.hstack(
                            [
                                mo.vstack(
                                    [
                                        mo.md("$s_0$"),
                                        mo.md(f"☹️"),
                                        s0_slider_custom,
                                        mo.md(f"🙂"),
                                        mo.md(f"${s0_slider_custom.value:.2f}$"),
                                    ],
                                    align="center",
                                ),
                                mo.vstack(
                                    [
                                        mo.md("$r_0$"),
                                        mo.md(f"🔋"),
                                        r0_slider_custom,
                                        mo.md(f"🪫"),
                                        mo.md(f"${r0_slider_custom.value:.2f}$"),
                                    ],
                                    align="center",
                                ),
                            ]
                        ),
                        download_buttons(
                            stimulus_response,
                            basename=f"""custom_response_tf={tf_slider.value}_n={num_periods.value}_s0={s0_slider_custom.value:.2f}_r0={r0_slider_custom.value:.2f}""",
                            style="v",
                        ),
                    ],
                    align="center",
                ),
            ]
        )

    custom_scenario()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Structural analysis of the model

    Here we consider the equilibrium points and streamline plots of the RS model.
    """)
    return


@app.cell(hide_code=True)
def _(RSModel, download_buttons, mo, strip_leading_whitespace):
    def equilibrium_analysis():
        model = RSModel()
        equilibria_plot = model.plot_equilibria(samples=300)

        return mo.hstack(
            [
                mo.md(f"""{mo.as_html(equilibria_plot)}"""),
                mo.vstack(
                    [
                        mo.md(
                            strip_leading_whitespace(
                            rf"""We consider the model
                            {model}
                            The figure shows all points $(s,r)$ such that $\dot s = \dot r = 0$ (equilibria). The curve consists of equilibrium points parameterized by $e$.""")
                        ),
                        "Download figure as:",
                        download_buttons(
                            equilibria_plot,
                            basename=f"equilibria_{model.model_name.replace(' ', '_')}",
                        ),
                    ]
                ),
            ],
            align="center",
            widths=[3, 1],
        )

    equilibrium_analysis()
    return


@app.cell(hide_code=True)
def _(
    RSModel,
    download_buttons,
    mo,
    streamline_slider,
    strip_leading_whitespace,
):
    streamline_model = RSModel()
    streamline_plot = streamline_model.plot_streamlines(
        external_input=streamline_slider.value
    )

    mo.hstack(
        [
            mo.vstack(
                [
                    mo.md(
                        rf"""Choose the _constant_ input value to generate a streamlines plot.

    $e={streamline_slider.value}\quad$ ☀️ {streamline_slider} 🌧️"""
                    ),
                    streamline_plot,
                ]
            ),
            mo.vstack(
                [
                    mo.md(
                        strip_leading_whitespace(
                        rf"""
    In this figure we consider the
    {streamline_model}

    This __streamline plot__ shows the flow generated by the differential equations when the input is held constant at $$e={streamline_slider.value}.$$
    """
                    )),
                    "Download figure as:",
                    download_buttons(
                        streamline_plot,
                        f"streamlines_{streamline_model.model_name.replace(' ', '_')}_e={streamline_slider.value:.2f}",
                    ),
                ]
            ),
        ],
        widths=[3, 1],
        align="center",
        gap=2,
    )
    return


@app.cell(hide_code=True)
def _():
    # mo.md(r"""
    # ## Appendix

    # This section contains helper tools and imports.
    # """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from drawdata import BarWidget
    import io
    from rsmodel import RSModel, Patient
    from rsmodel.utils import get_predefined_scenarios, create_custom_stimulus
    import re

    return (
        BarWidget,
        Patient,
        RSModel,
        create_custom_stimulus,
        get_predefined_scenarios,
        io,
        mo,
        np,
        re,
    )


@app.cell(hide_code=True)
def _(io, mo):
    def download_buttons(axisobject, basename="figure", style="h"):
        """Show three different download buttons."""
        if style == "h":
            arrange = mo.hstack
        else:
            arrange = mo.vstack
        return arrange(
            [
                download_axisobject(axisobject, basename, format=format)
                for format in "pdf png svg".split()
            ],
            gap=1,
            justify="start",
        )

    def download_axisobject(axisobject, basename="figure", format="pdf"):
        """Useful helper for in-app downloads of figures."""
        mimetypes = {
            "pdf": "application/pdf",
            "png": "image/png",
            "svg": "image/svg+xml",
        }

        async def __provide_the_data():
            _buf = io.BytesIO()
            axisobject.figure.savefig(_buf, format=format, bbox_inches="tight")
            _buf.seek(0)
            return _buf

        return mo.download(
            data=__provide_the_data,
            filename=f"{basename}.{format}",
            mimetype=mimetypes[format],
            label=format.upper(),
        )

    return (download_buttons,)


@app.cell(hide_code=True)
def _(get_predefined_scenarios):
    stimuli = get_predefined_scenarios()
    return (stimuli,)


@app.cell(hide_code=True)
def _(mo):
    s0_slider = mo.ui.slider(0, 1, 1e-2, 0.67, debounce=True, orientation="vertical")
    r0_slider = mo.ui.slider(0, 1, 1e-2, 0.84, debounce=True, orientation="vertical")
    return r0_slider, s0_slider


@app.cell(hide_code=True)
def _(np, stimulus_input, tf_slider):
    custom_input_data = {
        _["bin"]: float(np.round(_["value"], 2))
        for _ in stimulus_input.data
        if _["bin"] <= tf_slider.value
    }
    return (custom_input_data,)


@app.cell(hide_code=True)
def _(mo):
    tf_slider = mo.ui.slider(7, 40, 1, 40)
    num_periods = mo.ui.slider(1, 10, 1, 1)
    s0_slider_custom = mo.ui.slider(
        0, 1, 1e-2, 0.67, debounce=True, orientation="vertical"
    )
    r0_slider_custom = mo.ui.slider(
        0, 1, 1e-2, 0.84, debounce=True, orientation="vertical"
    )
    return num_periods, r0_slider_custom, s0_slider_custom, tf_slider


@app.cell(hide_code=True)
def _(BarWidget, mo):
    stimulus_input = mo.ui.anywidget(
        BarWidget(height=200, width=700, n_bins=40, collection_names=[])
    )
    return (stimulus_input,)


@app.cell(hide_code=True)
def _(mo):
    streamline_slider = mo.ui.slider(0, 1, 1e-2, 0.2)
    return (streamline_slider,)


@app.cell(hide_code=True)
def _(create_custom_stimulus, custom_input_data, tf_slider):
    custom_stimulus = create_custom_stimulus(custom_input_data, period=tf_slider.value)
    return (custom_stimulus,)


@app.cell(hide_code=True)
def _(re):
    strip_leading_whitespace = lambda s: "\n".join(
        re.sub(r"^\s+","", _) for _ in s.splitlines()    
    )
    return (strip_leading_whitespace,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
