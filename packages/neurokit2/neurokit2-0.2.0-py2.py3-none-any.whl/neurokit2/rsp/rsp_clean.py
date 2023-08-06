# -*- coding: utf-8 -*-
from warnings import warn

import numpy as np
import pandas as pd
import scipy.signal

from ..misc import NeuroKitWarning, as_vector
from ..signal import signal_detrend, signal_filter


def rsp_clean(rsp_signal, sampling_rate=1000, method="khodadad2018"):
    """**Preprocess a respiration (RSP) signal**

    Clean a respiration signal using different sets of parameters, such as:

    * ``"khodadad2018"``: Linear detrending followed by a fifth order 2Hz low-pass IIR Butterworth
      filter)
    * ``"BioSPPy"``: Second order 0.1-0.35 Hz bandpass Butterworth filter followed by a constant
      detrending).

    Parameters
    ----------
    rsp_signal : Union[list, np.array, pd.Series]
        The raw respiration channel (as measured, for instance, by a respiration belt).
    sampling_rate : int
        The sampling frequency of :func:`.rsp_signal` (in Hz, i.e., samples/second).
    method : str
        The processing pipeline to apply. Can be one of ``"khodadad2018"`` (default) or
        ``"biosppy"``.

    Returns
    -------
    array
        Vector containing the cleaned respiratory signal.

    See Also
    --------
    rsp_findpeaks, signal_rate, rsp_amplitude, rsp_process, rsp_plot

    Examples
    --------
    .. ipython:: python

      import pandas as pd
      import neurokit2 as nk

      rsp = nk.rsp_simulate(duration=30, sampling_rate=50, noise=0.01)
      signals = pd.DataFrame({
          "RSP_Raw": rsp,
          "RSP_Khodadad2018": nk.rsp_clean(rsp, sampling_rate=50, method="khodadad2018"),
          "RSP_BioSPPy": nk.rsp_clean(rsp, sampling_rate=50, method="biosppy")
      })
      @savefig p_rsp_clean1.png scale=100%
      signals.plot()
      @suppress
      plt.close()

    References
    ----------
    * Khodadad, D., Nordebo, S., Müller, B., Waldmann, A., Yerworth, R., Becher, T., ... & Bayford,
      R. (2018). Optimized breath detection algorithm in electrical impedance tomography.
      Physiological measurement, 39(9), 094001.

    """
    rsp_signal = as_vector(rsp_signal)

    # Missing data
    n_missing = np.sum(np.isnan(rsp_signal))
    if n_missing > 0:
        warn(
            f"There are {n_missing} missing data points in your signal."
            " Filling missing values by using the forward filling method.",
            category=NeuroKitWarning,
        )
        rsp_signal = _rsp_clean_missing(rsp_signal)

    method = method.lower()  # remove capitalised letters
    if method in ["khodadad", "khodadad2018"]:
        clean = _rsp_clean_khodadad2018(rsp_signal, sampling_rate)
    elif method == "biosppy":
        clean = _rsp_clean_biosppy(rsp_signal, sampling_rate)
    else:
        raise ValueError(
            "NeuroKit error: rsp_clean(): 'method' should be one of 'khodadad2018' or 'biosppy'."
        )

    return clean


# =============================================================================
# Handle missing data
# =============================================================================
def _rsp_clean_missing(rsp_signal):

    rsp_signal = pd.DataFrame.pad(pd.Series(rsp_signal))

    return rsp_signal


# =============================================================================
# Khodadad et al. (2018)
# =============================================================================
def _rsp_clean_khodadad2018(rsp_signal, sampling_rate=1000):
    """The algorithm is based on (but not an exact implementation of) the "Zero-crossing algorithm with amplitude
    threshold" by `Khodadad et al. (2018)

    <https://iopscience.iop.org/article/10.1088/1361-6579/aad7e6/meta>`_.

    """
    # Slow baseline drifts / fluctuations must be removed from the raw
    # breathing signal (i.e., the signal must be centered around zero) in order
    # to be able to reliable detect zero-crossings.

    # Remove baseline by applying a lowcut at .05Hz (preserves breathing rates
    # higher than 3 breath per minute) and high frequency noise by applying a
    # highcut at 3 Hz (preserves breathing rates slower than 180 breath per
    # minute).
    clean = signal_filter(
        rsp_signal,
        sampling_rate=sampling_rate,
        lowcut=0.05,
        highcut=3,
        order=2,
        method="butterworth",
    )

    return clean


# =============================================================================
# BioSPPy
# =============================================================================
def _rsp_clean_biosppy(rsp_signal, sampling_rate=1000):
    """Uses the same defaults as `BioSPPy.

    <https://github.com/PIA-Group/BioSPPy/blob/master/biosppy/signals/resp.py>`_.

    """
    # Parameters
    order = 2
    frequency = [0.1, 0.35]
    frequency = (
        2 * np.array(frequency) / sampling_rate
    )  # Normalize frequency to Nyquist Frequency (Fs/2).

    # Filtering
    b, a = scipy.signal.butter(N=order, Wn=frequency, btype="bandpass", analog=False)
    filtered = scipy.signal.filtfilt(b, a, rsp_signal)

    # Baseline detrending
    clean = signal_detrend(filtered, order=0)

    return clean
