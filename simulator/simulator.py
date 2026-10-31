import numpy as np

BITS = {"BPSK": 1, "QPSK": 2, "16-QAM": 4}   # bits per symbol

def constellation(name):
    k = BITS[name]
    idx = np.arange(2 ** k)
    if name == "BPSK":
        pts = 2.0 * idx - 1                        # 0 -> -1, 1 -> +1
    elif name == "QPSK":
        i = 1 - 2 * (idx >> 1)
        q = 1 - 2 * (idx & 1)
        pts = (i + 1j * q) / np.sqrt(2)
    else:  # 16-QAM, Gray mapped
        level = {0: -3, 1: -1, 3: 1, 2: 3}
        i = np.array([level[x >> 2] for x in idx])
        q = np.array([level[x & 3] for x in idx])
        pts = (i + 1j * q) / np.sqrt(10)
    return pts.astype(complex), k                   # average energy = 1

def ber(name, esn0_db, n_symbols=200_000):
    pts, k = constellation(name)
    shifts = np.arange(k - 1, -1, -1)
    bits = np.random.randint(0, 2, (n_symbols, k))
    tx = pts[bits @ (2 ** shifts)]                  # bits -> symbols
    esn0 = 10 ** (esn0_db / 10)
    sigma = np.sqrt(1 / (2 * esn0))
    noise = sigma * (np.random.randn(n_symbols) + 1j * np.random.randn(n_symbols))
    rx = tx + noise                                 # add noise
    nearest = np.argmin(np.abs(rx[:, None] - pts[None, :]), axis=1)
    bits_hat = (nearest[:, None] >> shifts) & 1     # closest point -> bits
    return np.mean(bits_hat != bits)

def best_method(esn0_db, limit=1e-3):
    ok = [m for m in BITS if ber(m, esn0_db) < limit]
    return max(ok, key=BITS.get) if ok else "None (too noisy)"