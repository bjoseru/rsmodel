"""Utility functions and predefined scenarios for the RS model.

This module provides:
- Predefined stimulus scenarios
- Visualization helpers
- Download utilities
"""

import io
from typing import Callable, Dict


def from_bad_to_worse_then_better(t: float) -> float:
    """Scenario: Initial stress, brief relief, severe stress, then recovery.

    Timeline:
    - t < 1: Very low stress (e=0.01)
    - 1 ≤ t < 1.5: High stress (e=0.7)
    - 1.5 ≤ t < 5: Low stress (e=0.1)
    - 5 ≤ t < 6.5: Very high stress (e=0.9)
    - 6.5 ≤ t ≤ 8.5: Low stress (e=0.1)
    - t > 8.5: Minimal stress (e=0.01)

    Args:
        t: Time value

    Returns:
        External input value e(t)
    """
    if t < 1:
        return 0.01
    elif t < 1.5:
        return 0.7
    elif t < 5:
        return 0.1
    elif t < 6.5:
        return 0.9
    elif t <= 8.5:
        return 0.1
    return 0.01


def multiple_adverse_events(t: float) -> float:
    """Scenario: Multiple stress episodes with varying intensity.

    Timeline:
    - t < 1: Low stress (e=0.1)
    - 1 ≤ t < 3: High stress (e=0.9)
    - 3 ≤ t < 6: Low stress (e=0.1)
    - 6 ≤ t < 6.5: Moderate stress (e=0.3)
    - 6.5 ≤ t < 15.5: Very low stress (e=0.05)
    - 15.5 ≤ t < 16: High stress (e=0.9)
    - 16 ≤ t < 18.5: Very low stress (e=0.05)
    - 18.5 ≤ t < 19: Moderate stress (e=0.3)
    - 19 ≤ t ≤ 20: Very low stress (e=0.05)
    - t > 20: Minimal stress (e=0.01)

    Args:
        t: Time value

    Returns:
        External input value e(t)
    """
    if t < 1:
        return 0.1
    if t < 3:
        return 0.9
    if t < 6:
        return 0.1
    if t < 6.5:
        return 0.3
    if t < 15.5:
        return 0.05
    if t < 16:
        return 0.9
    if t < 18.5:
        return 0.05
    if t < 19:
        return 0.3
    if t <= 20:
        return 0.05
    return 0.01


def from_bad_to_less_bad_to_not_great(t: float) -> float:
    """Scenario: Fluctuating stress levels without full recovery.

    Timeline:
    - t < 1: Low stress (e=0.1)
    - 1 ≤ t < 2: High stress (e=0.9)
    - 2 ≤ t < 5: Low stress (e=0.1)
    - 5 ≤ t < 5.5: Moderate stress (e=0.5)
    - 5.5 ≤ t ≤ 20: Low-moderate stress (e=0.2)
    - t > 20: Moderate stress (e=0.3)

    Args:
        t: Time value

    Returns:
        External input value e(t)
    """
    if t < 1:
        return 0.1
    if t < 2:
        return 0.9
    if t < 5:
        return 0.1
    if t < 5.5:
        return 0.5
    if t <= 20:
        return 0.2
    return 0.3


def get_predefined_scenarios() -> Dict[str, Callable[[float], float]]:
    """Get dictionary of all predefined stimulus scenarios.

    Returns:
        Dictionary mapping scenario names to stimulus functions
    """
    return {
        "from bad to worse then better": from_bad_to_worse_then_better,
        "multiple adverse events": multiple_adverse_events,
        "from bad to less bad to not great": from_bad_to_less_bad_to_not_great,
    }


def create_custom_stimulus(
    input_data: Dict[float, float], period: float = None
) -> Callable[[float], float]:
    """Create a custom stimulus function from data points.

    Creates a piecewise constant (sample-and-hold) function from
    a dictionary of time points and values.

    Args:
        input_data: Dictionary mapping time points to input values
        period: If specified, the stimulus repeats with this period

    Returns:
        Stimulus function e(t)
    """

    def stimulus(t: float) -> float:
        if period is not None:
            t = t % period

        for _t, _e in sorted(input_data.items(), key=lambda a: a[0]):
            if t <= _t + 0.5:
                return _e
        return 0

    return stimulus


def sample_and_hold(*samples) -> Callable[[float], float]:
    """Create a sample-and-hold signal from jump specifications.

    Args:
        *samples: Variable number of (time, value) tuples

    Returns:
        Sample-and-hold function

    Example:
        >>> signal = sample_and_hold((0, 0.1), (5, 0.9), (10, 0.2))
        >>> signal(3)  # Returns 0.1
        >>> signal(7)  # Returns 0.9
    """

    def signal(t):
        _samples = sorted((*samples, (-1, 0)), key=lambda _: _[0], reverse=True)
        for _t, _v in _samples:
            if _t < t:
                return _v
        return 0

    signal.__doc__ = f"Sample-and-hold signal: {sorted(samples)}"
    return signal


def download_figure_data(
    axisobject, basename: str = "figure", format: str = "pdf"
) -> io.BytesIO:
    """Create downloadable figure data.

    Args:
        axisobject: Matplotlib axes object
        basename: Base filename (without extension)
        format: File format ('pdf', 'png', 'svg')

    Returns:
        BytesIO buffer with figure data
    """
    buf = io.BytesIO()
    axisobject.figure.savefig(buf, format=format, bbox_inches="tight")
    buf.seek(0)
    return buf


def get_mimetype(format: str) -> str:
    """Get MIME type for file format.

    Args:
        format: File format ('pdf', 'png', 'svg')

    Returns:
        MIME type string
    """
    mimetypes = {
        "pdf": "application/pdf",
        "png": "image/png",
        "svg": "image/svg+xml",
    }
    return mimetypes.get(format, "application/octet-stream")
