set terminal pngcairo size 980,420
set output "fig4_baseline_vs_best.png"
set style data histograms
set style histogram clustered gap 1
set style fill solid 0.85 border -1
set boxwidth 0.9
set grid ytics
set ylabel "Normalized IPC (baseline=1.0)"
set key outside
best = system("cat best_degree.txt")
set title sprintf("Baseline vs Best GHB degree (best=%s)", best)

# 你的提升很小，先用 zoom-in 範圍；若你看到超出再調大
set yrange [0.995:1.010]

plot "plot_best_bar.tsv" using 2:xtic(1) title "baseline", \
     "" using 3 title "best-degree"
