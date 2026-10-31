import numpy as np
import matplotlib.pyplot as plt
from simulator.simulator import ber, BITS

np.random.seed(0)
snr = np.arange(0, 26, 1)
limit = 1e-3

for name in BITS:
    values = [ber(name, s) for s in snr]
    plt.semilogy(snr, np.maximum(values, 1e-7), "o-", label=name)

plt.axhline(limit, color="red", linestyle="--", label="BER limit")
plt.ylim(1e-6, 1)
plt.xlabel("Es/N0 (dB)")
plt.ylabel("Bit error rate")
plt.title("BER vs SNR")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.savefig("results/ber_curves.png", dpi=150)
plt.show()