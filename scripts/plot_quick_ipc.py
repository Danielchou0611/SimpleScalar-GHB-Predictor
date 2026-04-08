import pandas as pd
import matplotlib.pyplot as plt

# 讀 CSV
df = pd.read_csv("results/summary.csv")

# 如果你同時有 sim_IPC 與 sim_CPI，優先用 sim_IPC
if "sim_IPC" not in df.columns and "sim_CPI" in df.columns:
    df["sim_IPC"] = 1.0 / df["sim_CPI"]

# 只取 baseline
base = df[df["cfg"] == "baseline"]

# 依 benchmark 排序
order = ["cc1", "perl", "go"]
base = base.set_index("bench").loc[order].reset_index()

# 畫圖
plt.figure(figsize=(6,4))
plt.bar(base["bench"], base["sim_IPC"])
plt.ylabel("IPC")
plt.title("Baseline IPC (sanity check)")
plt.tight_layout()
plt.show()