import csv

BENCH = ["cc1","perl","go"]
CFG  = ["baseline","ghb"]

mp = {}
with open("results/summary.csv", newline="") as f:
    r = csv.DictReader(f)
    for row in r:
        if row["cfg"] in CFG and row["bench"] in BENCH:
            mp[(row["cfg"], row["bench"])] = row

def ul2_miss_rate(row):
    keys = list(row.keys())
    return float(row[keys[-1]])  # assume last column is ul2 miss rate

print("bench\tbaseline\tghb")
for b in BENCH:
    mb = ul2_miss_rate(mp[("baseline", b)])
    mg = ul2_miss_rate(mp[("ghb", b)])
    print(f"{b}\t1.0\t{mg/mb:.6f}")
