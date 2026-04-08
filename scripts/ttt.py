import os
import numpy as np
import matplotlib.pyplot as plt

RESULTS_DIR = "results"
BENCHES = ["cc1", "perl", "go"]
DEGREES = [1, 2, 4, 8, 16]

def get_stat(path, key):
    with open(path, "r", errors="ignore") as f:
        for line in f:
            if not line or line[0] == '#':
                continue
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0] == key:
                try:
                    return float(parts[1])
                except:
                    return None
    return None

def load_ipc(bench, cfg):
    p = os.path.join(RESULTS_DIR, f"{bench}.{cfg}.simout")
    if not os.path.exists(p):
        raise FileNotFoundError(p)
    return get_stat(p, "sim_IPC")

# ---- pick best degree by IPC per benchmark ----
base_ipc = {}
best_ipc = {}
best_deg = {}

for b in BENCHES:
    base_ipc[b] = load_ipc(b, "baseline")

    best = None
    bestd = None
    for d in DEGREES:
        ipc = load_ipc(b, f"ghb_d{d}")
        if ipc is None:
            continue
        if best is None or ipc > best:
            best = ipc
            bestd = d

    best_ipc[b] = best
    best_deg[b] = bestd

print("Best degree selection:")
for b in BENCHES:
    print(f"  {b}: baseline IPC={base_ipc[b]:.4f}, best IPC={best_ipc[b]:.4f} @ d={best_deg[b]}")

# ---- prepare arrays in benchmark order ----
x = np.arange(len(BENCHES))
labels = BENCHES

base = np.array([base_ipc[b] for b in BENCHES], dtype=float)
best = np.array([best_ipc[b] for b in BENCHES], dtype=float)

norm_base = np.ones_like(base)
norm_best = best / base
impr_pct_best = (best / base - 1.0) * 100.0
impr_pct_base = np.zeros_like(impr_pct_best)

# ---- Figure 1: normalized IPC (baseline=1) ----
plt.figure()
plt.plot(x, norm_base, marker="o", label="baseline")
plt.plot(x, norm_best, marker="o", label="GHB (best degree)")
plt.xticks(x, [f"{b}\n(best={best_deg[b]})" for b in BENCHES])
plt.ylabel("Normalized IPC (baseline=1)")
plt.title("GHB Prefetch Technique Demo: Normalized IPC by Benchmark")
plt.grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("fig_ghb_demo_norm_ipc_by_bench.png", dpi=200)

# ---- Figure 2: IPC improvement (%) ----
plt.figure()
plt.plot(x, impr_pct_base, marker="o", label="baseline")
plt.plot(x, impr_pct_best, marker="o", label="GHB (best degree)")
plt.xticks(x, [f"{b}\n(best={best_deg[b]})" for b in BENCHES])
plt.ylabel("IPC improvement (%)")
plt.title("GHB Prefetch Technique Demo: IPC Improvement by Benchmark")
plt.axhline(0.0, linestyle="--", linewidth=1)
plt.grid(True, linestyle="--", linewidth=0.6, alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("fig_ghb_demo_ipc_improvement_by_bench.png", dpi=200)

print("Wrote:")
print("  fig_ghb_demo_norm_ipc_by_bench.png")
print("  fig_ghb_demo_ipc_improvement_by_bench.png")
