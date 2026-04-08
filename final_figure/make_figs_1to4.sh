#!/usr/bin/env bash
set -euo pipefail
python3 make_plot_data.py
gnuplot fig1_ipc_impr.gp
gnuplot fig2_ul2_miss_norm.gp
gnuplot fig3_pf_per1k.gp
gnuplot fig4_best_bar.gp
echo "[DONE] Generated:"
ls -1 fig1_*.png fig2_*.png fig3_*.png fig4_*.png
echo "[INFO] Best degree:" $(cat best_degree.txt)
