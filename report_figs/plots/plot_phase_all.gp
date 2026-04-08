set term pngcairo size 900,520 font "Arial,12"

# ---------- P1: IPC norm ----------
set output "report_figs/png/P1_ipc_norm.png"
set title "Normalized IPC vs Phase (baseline=1)"
set xlabel "fastfwd (phase)"
set ylabel "IPC normalized"
set key left top
set grid
plot "report_figs/data/phase_ipc_norm.tsv" using 1:2 with linespoints title "perl", \
     "report_figs/data/phase_ipc_norm.tsv" using 1:3 with linespoints title "go"

# ---------- P2: UL2 miss norm ----------
set output "report_figs/png/P2_ul2_miss_norm.png"
set title "Normalized UL2 Miss Rate vs Phase (baseline=1)"
set xlabel "fastfwd (phase)"
set ylabel "UL2 miss rate normalized"
set key left top
set grid
plot "report_figs/data/phase_ul2_norm.tsv" using 1:2 with linespoints title "perl", \
     "report_figs/data/phase_ul2_norm.tsv" using 1:3 with linespoints title "go"

# ---------- P3: IPC improvement % ----------
set output "report_figs/png/P3_ipc_impr_pct.png"
set title "IPC Improvement (%) vs Phase"
set xlabel "fastfwd (phase)"
set ylabel "IPC improvement (%)"
set key left top
set grid
plot "report_figs/data/phase_ipc_impr_pct.tsv" using 1:2 with linespoints title "perl", \
     "report_figs/data/phase_ipc_impr_pct.tsv" using 1:3 with linespoints title "go"

# ---------- P4: Baseline vs GHB (ff=100k) ----------
set output "report_figs/png/P4_baseline_vs_ghb_ff100k.png"
set title "Baseline vs GHB (ff=100k, normalized IPC)"
set xlabel "benchmark"
set ylabel "IPC normalized"
set key left top
set grid
set style data histograms
set style histogram clustered gap 1
set style fill solid 0.8 border -1
set boxwidth 0.9
plot "report_figs/data/phase_best_bar.tsv" using 2:xtic(1) title "baseline", \
     "" using 3 title "ghb_d1"
