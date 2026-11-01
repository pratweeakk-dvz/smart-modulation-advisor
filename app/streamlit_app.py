import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from simulator.simulator import ber, BITS
st.set_page_config(page_title="Smart Modulation Advisor", layout="wide")
st.title("Smart Modulation Advisor")
st.caption("Recommends the fastest modulation whose bit error rate stays under your limit.")

st.sidebar.header("Controls")
snr = st.sidebar.slider("SNR, Es/N0 (dB)", 0, 25, 12)
exp = st.sidebar.slider("BER limit (10^x)", -4, -1, -3)
limit = 10.0 ** exp
st.sidebar.write(f"BER limit = {limit:.0e}")


@st.cache_data
def compute_curves(max_snr=25):
    np.random.seed(0)
    xs = list(range(0, max_snr + 1))
    return xs, {name: [ber(name, s) for s in xs] for name in BITS}


xs, data = compute_curves()

# Recommendation
ok = [n for n in BITS if data[n][snr] < limit]
if ok:
    best = max(ok, key=BITS.get)
    best_ber = data[best][snr]
    ber_text = f"{best_ber:.1e}" if best_ber > 0 else "below 5e-06 (no errors observed)"
    st.success(
        f"Recommended at {snr} dB: {best}. It carries {BITS[best]} bit(s) per symbol, "
        f"with BER {ber_text}, below the limit of {limit:.0e}."
    )
else:
    st.error(f"No scheme meets the BER limit of {limit:.0e} at {snr} dB. Increase the SNR or relax the limit.")

# Per-scheme cards
cols = st.columns(3)
for col, name in zip(cols, BITS):
    value = data[name][snr]
    with col:
        shown = f"BER {value:.1e}" if value > 0 else "BER < 5e-06"
        st.metric(name, shown)
        st.write(f"Bits per symbol: {BITS[name]}")
        st.write("Meets limit: " + ("yes" if value < limit else "no"))

# Graph
fig, ax = plt.subplots(figsize=(9, 4.5))
for name in BITS:
    ax.semilogy(xs, np.maximum(data[name], 1e-7), "o-", label=name)
ax.axhline(limit, color="red", linestyle="--", label="BER limit")
ax.axvline(snr, color="gray", linestyle=":", label="Selected SNR")
ax.set_ylim(1e-6, 1)
ax.set_xlabel("Es/N0 (dB)")
ax.set_ylabel("Bit error rate")
ax.set_title("BER vs SNR (Monte Carlo simulation, AWGN)")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
st.pyplot(fig)
df = pd.DataFrame({"SNR_dB": xs, **data})
st.subheader("Results table")
st.dataframe(df)
st.download_button("Download CSV", df.to_csv(index=False), "ber_results.csv", "text/csv")