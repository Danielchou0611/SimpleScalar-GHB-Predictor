set terminal pngcairo size 900,420
set output "ul2_miss_norm.png"

set style data histograms
set style histogram clustered gap 1
set style fill solid 0.85 border -1
set boxwidth 0.9

set grid ytics
set ylabel "Normalized UL2 Miss Rate (baseline=1.0)"
set key outside

# miss rate 變化可能比 IPC 大，先用較寬的範圍；必要時再縮
set yrange [0.90:1.05]

plot "plot_data_ul2.tsv" using 2:xtic(1) title "baseline", \
     "" using 3 title "ghb"
