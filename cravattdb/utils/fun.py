"""Contains a few useful functions."""

import statistics


def special_median(ratios):
    """Calculate median given a set of ratios. Modified with some empirical rules."""
    if not ratios:
        return 0

    if len(ratios) == 2 and 20 in ratios and min(ratios) < 3:
        return min(ratios)

    return statistics.median(ratios)
