import numpy


def estimate_N_s_eq9(N_off, alpha, S):
    """
    Returns the required signal N_s to obtain significance S using:
    Eq.9 in Section II, Immediatly estimating the standard deviation of
    the observerd signal.

    Parameters
    ----------
    N_off : float
            Measured counts in all offregions.
    alpha : float
            Exposure-ratio of onregion over offregion.
    S : float
            Targeted significance.
    """
    assert N_off > 0.0
    assert alpha > 0.0
    assert S >= 0.0
    p = S**2 * alpha
    q = -1.0 * S**2 * N_off * alpha * (1 + alpha)
    return -p/2 + numpy.sqrt((p/2)**2 - q)


def estimate_S_eq9(N_on, N_off, alpha):
    """
    Returns the significance S using:
    Eq.9 in Section II, Immediatly estimating the standard deviation of
    the observerd signal N_s.

    Parameters
    ----------
    N_on : float
            Measured count in onregion. This is N_on = N_s + N_B.
            Sum of signal and background in onregion.
    N_off : float
            Measured counts in all offregions.
    alpha : float
            Exposure-ratio of onregion over offregion.
    """
    assert N_on > 0.0
    assert N_off > 0.0
    assert alpha > 0.0
    _N_s = (N_on - N_off * alpha)
    assert _N_s >= 0.0
    return _N_s / numpy.sqrt(alpha * (N_on + N_off))


def estimate_S_eq17(N_on, N_off, alpha):
    """
    Returns the significance S using:
    Eq.17 in Section III, Based on statistical hypotheses test.

    Parameters
    ----------
    N_on : float
            Measured count in onregion. This is N_on = N_s + N_B.
            Sum of signal and background in onregion.
    N_off : float
            Measured counts in all offregions.
    alpha : float
            Exposure-ratio of onregion over offregion.
    """
    assert N_on > 0.0
    assert N_off > 0.0
    assert alpha > 0.0
    _N_s = (N_on - N_off * alpha)
    assert _N_s >= 0.0
    ln = numpy.log
    sqrt = numpy.sqrt
    a = alpha

    _on = (1 + a)/a * N_on / (N_on + N_off)
    _off = (1 + a) * N_off / (N_on + N_off)
    S = sqrt(2) * sqrt(N_on * ln(_on) + N_off * ln(_off))

    return S


def _relative_ratio(a, b):
    return numpy.abs(a - b)/(0.5 * (a + b))


def estimate_N_s_eq17(
    N_off,
    alpha,
    S,
    margin=1e-6,
    max_num_iterations=1000,
    N_s_start=None,
):
    """
    Returns the required signal N_s to obtain significance S using:
    Eq.17 in Section III, Based on statistical hypotheses test.
    This runs an iteration by forward computing S.

    Parameters
    ----------
    N_off : float
            Total counts in all offregions.
    alpha : float
            Exposure-ratio of onregion over offregion.
    S : float
            Targeted significance.
    margin : float, optional
            Required precision S_iteration ~= S to break iteration.
    max_num_iterations : int, optional
            Maximum number of iterations before throwing exception.
    N_s_start : float, optional
            The starting signal for the iteration. Default is an estimate
            based on Eq.9.
    """
    if N_s_start is None:
        N_s_start = estimate_N_s_eq9(N_off=N_off, alpha=alpha, S=S)
    assert N_s_start >= 0.0

    N_s_it = float(N_s_start)
    it = 0
    while True:
        assert it <= max_num_iterations

        N_on_it = N_off * alpha + N_s_it
        S_it = estimate_S_eq17(N_on=N_on_it, N_off=N_off, alpha=alpha)

        ratio = _relative_ratio(S, S_it)

        if ratio < margin:
            break

        rr = ratio / 3
        if S_it > S:
            N_s_it *= (1 - rr)
        else:
            N_s_it *= (1 + rr)

        it += 1

    return N_s_it
