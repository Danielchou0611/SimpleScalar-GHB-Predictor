import re
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# 基本設定
# -----------------------------
RESULTS_DIR = Path("results")
BENCHES = ["cc1", "perl", "go"]
DEGREES = [1, 2, 4, 8, 16]

# 正則工具
def get_value(pattern, text):
    m = re.search(pattern, text)
    return float(m.group(1)) if m else None

def parse_simout(path):
    txt = path.read_text()

    return {
        "sim_num_insn": get_value(r"sim_num_insn\s+([0-9.]+)", txt),
        "sim_IPC": get_value(r"sim_IPC\s+([0-9.]+)", txt),
        "ul2_miss_rate": get_value(r"ul2.miss_rate\s+([0-9.]+)", txt),
        "ghb_pref_issued": get_value(r"ghb_pref_issued\s+([0-9.]+)", txt),
    }

# -----------------------------
# 讀資料
# -----------------------------
data = {}

for bench in BENCHES:
    data[bench] = {"baseline": None, "deg": {}}

    # baseline
    base = RESULTS_DIR / f"{bench}.baseline.simout"
    data[bench]["baseline"] = parse_simout(base)

    # degree sweep
    for d in DEGREES:
        f = RESULTS_DIR / f"{bench}.ghb_d{d}.simout"
        data[bench]["deg"][d] = parse_simout(f)

# -----------------------------
# Figure A：IPC vs degree
# -----------------------------
plt.figure(figsize=(6, 4))

for bench in BENCHES:
    y = [data[bench]["deg"][d]["sim_IPC"] for d in DEGREES]
    plt.plot(DEGREES, y, marker="o", label=bench)

plt.xlabel("GHB prefetch degree")
plt.ylabel("IPC")
plt.title("IPC vs GHB Prefetch Degree")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("fig_ipc_vs_degree.png", dpi=300)
plt.close()

# -----------------------------
# Figure B：UL2 miss rate vs degree
# -----------------------------
plt.figure(figsize=(6, 4))

for bench in BENCHES:
    y = [data[bench]["deg"][d]["ul2_miss_rate"] for d in DEGREES]
    plt.plot(DEGREES, y, marker="o", label=bench)

plt.xlabel("GHB prefetch degree")
plt.ylabel("UL2 miss rate")
plt.title("UL2 Miss Rate vs GHB Prefetch Degree")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("fig_ul2_miss_vs_degree.png", dpi=300)
plt.close()

# -----------------------------
# Figure C：Prefetch / 1K instructions
# -----------------------------
plt.figure(figsize=(6, 4))

for bench in BENCHES:
    y = []
    for d in DEGREES:
        pref = data[bench]["deg"][d]["ghb_pref_issued"]
        insn = data[bench]["deg"][d]["sim_num_insn"]
        y.append(pref / insn * 1000.0)

    plt.plot(DEGREES, y, marker="o", label=bench)

plt.xlabel("GHB prefetch degree")
plt.ylabel("Prefetches per 1K instructions")
plt.title("Prefetch Traffic vs GHB Prefetch Degree")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("fig_prefetch_per_1k_vs_degree.png", dpi=300)
plt.close()

print("Generated figures:")
print("  fig_ipc_vs_degree.png")
print("  fig_ul2_miss_vs_degree.png")
print("  fig_prefetch_per_1k_vs_degree.png")
