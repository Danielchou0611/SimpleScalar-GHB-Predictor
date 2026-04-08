import csv, os

PHASES = [100000, 10000000, 20000000]
BENCHES = ["perl","go"]
CFG = "ghb_d1"

def read_summary(phase):
    path = f"results_phase/ff_{phase}/summary.csv"
    rows = []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)
    return rows

def f(x):
    try:
        return float(x)
    except:
        return None

# collect numbers
ipc_base = { (p,b): None for p in PHASES for b in BENCHES}
ipc_cfg  = { (p,b): None for p in PHASES for b in BENCHES}
ul2_base = { (p,b): None for p in PHASES for b in BENCHES}
ul2_cfg  = { (p,b): None for p in PHASES for b in BENCHES}

for p in PHASES:
    rows = read_summary(p)
    for row in rows:
        bench = row["bench"]
        cfg   = row["cfg"]
        if bench not in BENCHES:
            continue
        ipc = f(row.get("sim_IPC",""))
        ul2 = f(row.get("ul2.miss_rate",""))
        if cfg == "baseline":
            ipc_base[(p,bench)] = ipc
            ul2_base[(p,bench)] = ul2
        if cfg == CFG:
            ipc_cfg[(p,bench)] = ipc
            ul2_cfg[(p,bench)] = ul2

def write_tsv(fname, header, rows):
    with open(fname, "w") as out:
        out.write("\t".join(header) + "\n")
        for r in rows:
            out.write("\t".join(str(x) for x in r) + "\n")

# Figure P1: IPC norm
rows = []
for p in PHASES:
    r = [p]
    for b in BENCHES:
        base = ipc_base[(p,b)]
        cfg  = ipc_cfg[(p,b)]
        val = (cfg/base) if (base and cfg) else "NA"
        r.append(val)
    rows.append(r)
write_tsv("phase_ipc_norm.tsv", ["phase"]+BENCHES, rows)

# Figure P2: UL2 miss norm
rows = []
for p in PHASES:
    r = [p]
    for b in BENCHES:
        base = ul2_base[(p,b)]
        cfg  = ul2_cfg[(p,b)]
        val = (cfg/base) if (base and cfg and base != 0) else "NA"
        r.append(val)
    rows.append(r)
write_tsv("phase_ul2_norm.tsv", ["phase"]+BENCHES, rows)

# Figure P3: IPC improvement %
rows = []
for p in PHASES:
    r = [p]
    for b in BENCHES:
        base = ipc_base[(p,b)]
        cfg  = ipc_cfg[(p,b)]
        val = (100.0*(cfg/base - 1.0)) if (base and cfg) else "NA"
        r.append(val)
    rows.append(r)
write_tsv("phase_ipc_impr_pct.tsv", ["phase"]+BENCHES, rows)

# Figure P4: best-bar (use ff=100k as main)
PMAIN = 100000
rows = []
for b in BENCHES:
    base = ipc_base[(PMAIN,b)]
    cfg  = ipc_cfg[(PMAIN,b)]
    rows.append([b, 1.0, (cfg/base) if (base and cfg) else "NA"])
write_tsv("phase_best_bar.tsv", ["bench","baseline",CFG], rows)

print("Generated: phase_ipc_norm.tsv phase_ul2_norm.tsv phase_ipc_impr_pct.tsv phase_best_bar.tsv")
