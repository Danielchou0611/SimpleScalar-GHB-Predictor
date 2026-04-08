import csv

BENCH_ORDER = ["cc1", "perl", "go"]
CFG_ORDER = ["baseline", "ghb"]

rows = []
with open("results/summary.csv", newline="") as f:
    r = csv.DictReader(f)
    for row in r:
        if row["cfg"] in CFG_ORDER and row["bench"] in BENCH_ORDER:
            rows.append(row)

# index by (cfg, bench)
mp = {(row["cfg"], row["bench"]): row for row in rows}

def fnum(x):
    try:
        return float(x)
    except:
        return None

print("bench\tIPC_base\tIPC_ghb\tSpeedup(IPC)\tCPI_base\tCPI_ghb")
for b in BENCH_ORDER:
    base = mp.get(("baseline", b))
    ghb  = mp.get(("ghb", b))
    if not base or not ghb:
        print(f"{b}\t<MISSING>")
        continue

    ipc_b = fnum(base.get("sim_IPC",""))
    ipc_g = fnum(ghb.get("sim_IPC",""))
    cpi_b = fnum(base.get("sim_CPI",""))
    cpi_g = fnum(ghb.get("sim_CPI",""))

    sp = (ipc_g/ipc_b) if (ipc_b and ipc_g) else None
    sp_s = f"{sp:.4f}" if sp is not None else "<NA>"

    print(f"{b}\t{ipc_b:.4f}\t{ipc_g:.4f}\t{sp_s}\t\t{cpi_b:.4f}\t{cpi_g:.4f}")
