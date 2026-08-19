# /// script
# requires-python = ">=3.12"  # PEP 701: backslashes inside f-string expressions
# dependencies = [
#     "drawdata==0.3.8",
#     "marimo",
#     "matplotlib>=3.8",
#     "numpy>=1.24",
#     "rsmodel>=0.1",
#     "scipy>=1.11",
#     "sympy>=1.12",
# ]
# ///

# Run with nothing installed but `uv`, from the repository root:
#   uvx marimo edit --sandbox notebooks/interactive_playground.py
# `--sandbox` builds a throwaway environment from the PEP 723 header above,
# which pulls rsmodel from PyPI. See the README for the local-checkout variant.

import marimo

__generated_with = "0.24.0"
app = marimo.App(
    width="medium",
    app_title="The Resilience–Symptom Model of Depression",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Resilience&ndash;Symptom Model of Depression

    Use the arrow keys or on-screen controls to navigate slides. Some panels contain interactive elements &mdash; try adjusting the sliders.
    """)
    return


@app.cell
def _(Patient, download_buttons, mo, r0_slider, s0_slider, stimuli):
    def scenario_tab(title, stimulus):
        patient = Patient(
            s0=s0_slider.value, r0=r0_slider.value
        )
        stimulus_response = patient.get_stimulus_response(
            stimulus
        )

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
                                        mo.md(
                                            f"${s0_slider.value:.2f}$"
                                        ),
                                    ],
                                    align="center",
                                ),
                                mo.vstack(
                                    [
                                        mo.md("$r_0$"),
                                        mo.md(f"🔋"),
                                        r0_slider,
                                        mo.md(f"🪫"),
                                        mo.md(
                                            f"${r0_slider.value:.2f}$"
                                        ),
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
    

    mo.vstack([
                mo.md("""
                ## Pre-defined scenarios

                Adjust the sliders on the right-hand-side for different initial levels of (depression) symptom $s_0$ and resilience $r_0$. 
                Select different adverse input scenarios via the tabs above the figure.
                """),    
    mo.ui.tabs(
        {k: scenario_tab(k, v) for k, v in stimuli.items()}
    )])
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
        patient = Patient(
            s0=s0_slider_custom.value,
            r0=r0_slider_custom.value,
        )
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
                        mo.md(
                            f"""number of repetitions:\n\n$n={num_periods.value}$"""
                        ),
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
                                        mo.md(
                                            f"${s0_slider_custom.value:.2f}$"
                                        ),
                                    ],
                                    align="center",
                                ),
                                mo.vstack(
                                    [
                                        mo.md("$r_0$"),
                                        mo.md(f"🔋"),
                                        r0_slider_custom,
                                        mo.md(f"🪫"),
                                        mo.md(
                                            f"${r0_slider_custom.value:.2f}$"
                                        ),
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


    mo.vstack([
        mo.md("""
    ## Make your own custom scenario

    In the following scenario, you can define an "adverse input" graphically by drawing into a figure. The response of the patient is shown in the plot next to the input figure.

    There are options to adjust the time span of the simulation and whether the custom input should be extended periodically, e.g., to model daily, weekly, or otherwise repeated exposures to adverse circumstances.

    """
    ),
    custom_scenario()    
    ])

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Phase-space view of the RS model
    """)
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
                        )
                    ),
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
    from rsmodel.utils import (
        get_predefined_scenarios,
        create_custom_stimulus,
    )
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
    def download_buttons(
        axisobject, basename="figure", style="h"
    ):
        """Show three different download buttons."""
        if style == "h":
            arrange = mo.hstack
        else:
            arrange = mo.vstack
        return arrange(
            [
                download_axisobject(
                    axisobject, basename, format=format
                )
                for format in "pdf png svg".split()
            ],
            gap=1,
            justify="start",
        )

    def download_axisobject(
        axisobject, basename="figure", format="pdf"
    ):
        """Useful helper for in-app downloads of figures."""
        mimetypes = {
            "pdf": "application/pdf",
            "png": "image/png",
            "svg": "image/svg+xml",
        }

        async def __provide_the_data():
            _buf = io.BytesIO()
            axisobject.figure.savefig(
                _buf, format=format, bbox_inches="tight"
            )
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
    s0_slider = mo.ui.slider(
        0,
        1,
        1e-2,
        0.67,
        debounce=True,
        orientation="vertical",
    )
    r0_slider = mo.ui.slider(
        0,
        1,
        1e-2,
        0.84,
        debounce=True,
        orientation="vertical",
    )
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
        0,
        1,
        1e-2,
        0.67,
        debounce=True,
        orientation="vertical",
    )
    r0_slider_custom = mo.ui.slider(
        0,
        1,
        1e-2,
        0.84,
        debounce=True,
        orientation="vertical",
    )
    return num_periods, r0_slider_custom, s0_slider_custom, tf_slider


@app.cell(hide_code=True)
def _(BarWidget, mo):
    stimulus_input = mo.ui.anywidget(
        BarWidget(
            height=200,
            width=700,
            n_bins=40,
            collection_names=[],
        )
    )
    return (stimulus_input,)


@app.cell(hide_code=True)
def _(mo):
    streamline_slider = mo.ui.slider(0, 1, 1e-2, 0.2)
    return (streamline_slider,)


@app.cell(hide_code=True)
def _(create_custom_stimulus, custom_input_data, tf_slider):
    custom_stimulus = create_custom_stimulus(
        custom_input_data, period=tf_slider.value
    )
    return (custom_stimulus,)


@app.cell(hide_code=True)
def _(re):
    strip_leading_whitespace = lambda s: "\n".join(
        re.sub(r"^\s+", "", _) for _ in s.splitlines()
    )
    return (strip_leading_whitespace,)


@app.cell(hide_code=True)
def license(mo):
    mo.md(r"""
    # The MIT License (MIT)
    Copyright © 2026 Björn Rüffer & Michael Schönlein

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    """)
    return


@app.cell(hide_code=True)
def impressum(mo):
    mo.md(r"""
    # Impressum &amp; Datenschutzerkl&auml;rung

    __Impressum:__ Prof. Dr. Bj&ouml;rn R&uuml;ffer, Coudraystr. 13B, 99423 Weimar. E-Mail: bjoern.rueffer@uni-weimar.de. Verantwortlich f&uuml;r den Inhalt nach &sect; 5 DDG.

    __Datenschutz:__ Diese Seite ist eine statische Anwendung. Sie setzt keine Cookies, verwendet keine Analyse- oder Tracking-Dienste und speichert selbst keine personenbezogenen Daten. Gehostet wird sie &uuml;ber Cloudflare Pages (Cloudflare, Inc., 101 Townsend St., San Francisco, CA 94107, USA); dabei werden technische Zugriffsdaten (z.&nbsp;B. IP-Adresse, Zeitstempel, angeforderte Ressource) automatisch verarbeitet, um die Auslieferung technisch zu erm&ouml;glichen und abzusichern (Art.&nbsp;6 Abs.&nbsp;1 lit.&nbsp;f DSGVO). Zur Ausf&uuml;hrung des Python-Codes im Browser l&auml;dt die Seite die Laufzeitumgebung Pyodide vom Content-Delivery-Network jsDelivr sowie eine Paketliste von `wasm.marimo.app` nach; dabei wird Ihre IP-Adresse an die jeweiligen Anbieter &uuml;bermittelt. Die &Uuml;bermittlung in Drittl&auml;nder erfolgt auf Grundlage der EU-Standardvertragsklauseln. Kontakt f&uuml;r Datenschutzanfragen: bjoern.rueffer@uni-weimar.de.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(f"""
    # Disclaimer

    {mo.callout(mo.md("Note that neither the model as a whole nor the time scale are in any way calibrated and should hence be seen as abstractions.\n\n This is a qualitative model, not a quantitative one.\n\n __This model does not consider the possible benefits of medication or interventions.__"), kind="danger")}
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
