set terminal pngcairo size 980,420
set output "fig3_pf_per1k_vs_degree.png"
set grid ytics
set xlabel "Prefetch degree"
set ylabel "Prefetches issued per 1K inst"
set key outside
set xtics ("1" 1, "2" 2, "4" 4, "8" 8, "16" 16)
set xrange [0.5:16.5]
set yrange [0:*]

plot "plot_pf_per1k.tsv" using 1:2 with linespoints title "cc1", \
     "" using 1:3 with linespoints title "perl", \
     "" using 1:4 with linespoints title "go"
