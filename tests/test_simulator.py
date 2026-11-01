import numpy as np
from simulator.simulator import ber, best_method

def test_ber_falls_as_snr_rises():
    np.random.seed(0)
    for m in ["BPSK", "QPSK", "16-QAM"]:
        assert ber(m, 15) <= ber(m, 0)

def test_scheme_ordering_at_same_snr():
    np.random.seed(0)
    assert ber("BPSK", 8) <= ber("QPSK", 8) <= ber("16-QAM", 8)

def test_high_snr_picks_16qam():
    np.random.seed(0)
    assert best_method(25) == "16-QAM"

def test_very_low_snr_has_no_safe_scheme():
    np.random.seed(0)
    assert best_method(-5) == "None (too noisy)"