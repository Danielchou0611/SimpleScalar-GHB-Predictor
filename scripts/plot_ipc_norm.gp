set terminal pngcairo size 900,420
set output "ipc_norm.png"

set style data histograms
set style histogram clustered gap 1
set style fill solid 0.85 border -1
set boxwidth 0.9

set grid ytics
set ylabel "Normalized IPC (baseline=1.0)"
set yrange [0.995:1.006]
set key outside

plot "plot_data_ipc.tsv" using 2:xtic(1) title "baseline", \
     "" using 3 title "ghb"
