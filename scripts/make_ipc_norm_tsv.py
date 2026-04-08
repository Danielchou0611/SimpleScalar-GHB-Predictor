import csv

BENCH = ["cc1","perl","go"]
CFG  = ["baseline","ghb"]

mp = {}
with open("results/summary.csv", newline="") as f:
    r = csv.DictReader(f)
    for row in r:
        if row["cfg"] in CFG and row["bench"] in BENCH:
            mp[(row["cfg"], row["bench"])] = row

def f(x): return float(x)

print("bench\tbaseline\tghb")
for b in BENCH:
    ib = f(mp[("baseline", b)]["sim_IPC"])
    ig = f(mp[("ghb", b)]["sim_IPC"])
    print(f"{b}\t1.0\t{ig/ib:.6f}")
