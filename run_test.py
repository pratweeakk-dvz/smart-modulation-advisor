from simulator.simulator import best_method
for snr in [4, 8, 12, 20]:
    print(snr, best_method(snr))