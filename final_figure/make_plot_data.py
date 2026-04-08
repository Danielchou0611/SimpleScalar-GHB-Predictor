import csv, math

BENCH = ["cc1","perl","go"]
DEG   = [1,2,4,8,16]
CFG_BASE = "baseline"

def fnum(x):
    try: return float(x)
    except: return None

def parse_simout_value(path, key):
    with open(path) as f:
        for line in f:
            if line.startswith(key):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        return float(parts[1])
                    except:
                        return None
    return None

mp = {}
with open("results/summary.csv", newline="") as f:
    r = csv.DictReader(f)
    for row in r:
        mp[(row["cfg"], row["bench"])] = row

def get_stat(cfg, bench, key):
    row = mp.get((cfg, bench))
    if not row: return None
    return fnum(row.get(key, "NA"))

# ---------- Fig1: IPC improvement (%) ----------
with open("plot_ipc_impr.tsv", "w") as f:
    f.write("degree\t" + "\t".join(BENCH) + "\n")
    for d in DEG:
        cfg = f"ghb_d{d}"
        f.write(str(d))
        for b in BENCH:
            ipc_b = get_stat(CFG_BASE, b, "sim_IPC")
            ipc_c = get_stat(cfg, b, "sim_IPC")
            impr = (ipc_c/ipc_b - 1.0) * 100.0 if (ipc_b and ipc_c) else None
            f.write("\t" + (f"{impr:.6f}" if impr is not None else "NA"))
        f.write("\n")

# ---------- Fig2: UL2 miss rate normalized ----------
with open("plot_ul2_miss_norm.tsv", "w") as f:
    f.write("degree\t" + "\t".join(BENCH) + "\n")
    for d in DEG:
        cfg = f"ghb_d{d}"
        f.write(str(d))
        for b in BENCH:
            m_b = get_stat(CFG_BASE, b, "ul2.miss_rate")
            m_c = get_stat(cfg, b, "ul2.miss_rate")
            norm = (m_c/m_b) if (m_b and m_c is not None) else None
            f.write("\t" + (f"{norm:.6f}" if norm is not None else "NA"))
        f.write("\n")

# ---------- Fig3: prefetch issued per 1K inst ----------
with open("plot_pf_per1k.tsv", "w") as f:
    f.write("degree\t" + "\t".join(BENCH) + "\n")
    for d in DEG:
        cfg = f"ghb_d{d}"
        f.write(str(d))
        for b in BENCH:
            simout = f"results/{b}.{cfg}.simout"
            insts  = parse_simout_value(simout, "sim_num_insn")
            issued = parse_simout_value(simout, "ghb_pref_issued")
            per1k = (issued/insts*1000.0) if (insts and issued is not None) else None
            f.write("\t" + (f"{per1k:.6f}" if per1k is not None else "NA"))
        f.write("\n")

# ---------- pick best degree by geomean IPC ratio ----------
best_d = None
best_gm = -1e9
for d in DEG:
    cfg = f"ghb_d{d}"
    ratios = []
    ok = True
    for b in BENCH:
        ipc_b = get_stat(CFG_BASE, b, "sim_IPC")
        ipc_c = get_stat(cfg, b, "sim_IPC")
        if not (ipc_b and ipc_c):
            ok = False
            break
        ratios.append(ipc_c/ipc_b)
    if not ok:
        continue
    gm = math.exp(sum(math.log(x) for x in ratios)/len(ratios))
    if gm > best_gm:
        best_gm = gm
        best_d = d

with open("best_degree.txt","w") as f:
    f.write(str(best_d if best_d is not None else "NA") + "\n")

# ---------- Fig4: baseline vs best (normalized IPC) ----------
with open("plot_best_bar.tsv", "w") as f:
    f.write("bench\tbaseline\tbest\n")
    for b in BENCH:
        ipc_b = get_stat(CFG_BASE, b, "sim_IPC")
        ipc_c = get_stat(f"ghb_d{best_d}", b, "sim_IPC") if best_d else None
        norm_best = (ipc_c/ipc_b) if (ipc_b and ipc_c) else None
        f.write(f"{b}\t1.0\t{norm_best:.6f}\n" if norm_best is not None else f"{b}\t1.0\tNA\n")

# ---------- Fig5 placeholder (NA until you add useful counter) ----------
with open("plot_pf_accuracy.tsv","w") as f:
    f.write("degree\t" + "\t".join(BENCH) + "\n")
    for d in DEG:
        f.write(f"{d}\tNA\tNA\tNA\n")
