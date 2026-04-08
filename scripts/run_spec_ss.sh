#!/usr/bin/env bash
set -euo pipefail

SIM=./sim-outorder
PROGDIR=benchmarks_little/Programs
OUTDIR=results
mkdir -p "$OUTDIR"

# 你要對齊比較的控制參數（建議固定）
FASTFWD=${FASTFWD:-100000000}
MAXINST=${MAXINST:-200000000}

# 你所有「實驗組態」都放在這裡：每組一個 name + 參數字串
# 你之後要比較 baseline vs prefetch / predictor on/off，只要加一行。
declare -A CFG
CFG[baseline]=""
CFG[ghb_d1]="-ghb:enable true -ghb:degree 1"
CFG[ghb_d2]="-ghb:enable true -ghb:degree 2"
CFG[ghb_d4]="-ghb:enable true -ghb:degree 4"
CFG[ghb_d8]="-ghb:enable true -ghb:degree 8"
CFG[ghb_d16]="-ghb:enable true -ghb:degree 16"
# 範例：把你自己的 prefetch / predictor 參數加進來（名稱自行改）
# CFG[prefetch_on]="-ul2:prefetch 1 -prefetch:xxx 1"
# CFG[waypred_on]="-cache:waypred_enable 1 -cache:waypred_hit_latency 1 -cache:waypred_penalty 2"

# --- Benchmark 清單 ---
# 這裡先只寫 .ss 檔名；若要加參數（如 perl 的 flags），可擴充成陣列。
BENCHES=(cc1 perl go )

# --- 抽 stats 的 key（你最常會用的）---
# 你之後要加：把你新增的統計項目 key 加進來就好。
STAT_KEYS=(
  sim_num_insn
  sim_num_refs
  sim_elapsed_time
  sim_inst_rate
  sim_cycle
  sim_IPC
  sim_CPI
)

# 針對 cache/mem 常用（名稱依你的 SimpleScalar 版本 stats 命名為準）
# 你可以先跑一次 baseline，把 results/*.simout 打開，確認 key 長什麼樣。
STAT_KEYS+=(
  il1.miss_rate
  dl1.miss_rate
  ul2.miss_rate
)

# 你自己的 stats（例如你加的 ghb / estride / waypred / bingo）
# STAT_KEYS+=(ghb_trains ghb_lookups ghb_stride_found estride_hits waypred_hits)

# --- 小工具：從 simout 抽一個 key 的值（取第一欄數字）---
get_stat () {
  local key="$1" file="$2"
  # 格式通常是：key  <value>  # comment
  awk -v k="$key" '$1==k {print $2; found=1; exit} END{if(!found) print "NA"}' "$file"
}

# --- 輸出 CSV header ---
CSV="$OUTDIR/summary.csv"
{
  printf "cfg,bench,fastfwd,maxinst"
  for k in "${STAT_KEYS[@]}"; do printf ",%s" "$k"; done
  printf "\n"
} > "$CSV"

run_one () {
  local cfgname="$1"
  local bench="$2"

  local bin="$PROGDIR/${bench}.ss"
  if [[ ! -f "$bin" ]]; then
    echo "[ERROR] missing binary: $bin" >&2
    exit 1
  fi

  local simout="$OUTDIR/${bench}.${cfgname}.simout"
  local progout="$OUTDIR/${bench}.${cfgname}.progout"

  echo "[RUN] bench=$bench cfg=$cfgname"

  ff="$FASTFWD"
  if [[ "$bench" == "cc1" ]]; then
    ff=100000
  fi
  extra_args=()
  if [[ "$bench" == "perl" ]]; then
    extra_args+=(benchmarks_little/Input/perl-tests.pl)
  fi

  $SIM \
    -fastfwd "$ff" \
    -max:inst "$MAXINST" \
    ${CFG[$cfgname]} \
    -redir:sim "$simout" \
    -redir:prog "$progout" \
    "$bin" "${extra_args[@]}" \
    < /dev/null \
    > /dev/null

  # 抽 stats → CSV 一列
  {
    printf "%s,%s,%s,%s" "$cfgname" "$bench" "$ff" "$MAXINST"
    for k in "${STAT_KEYS[@]}"; do
      v=$(get_stat "$k" "$simout")
      printf ",%s" "$v"
    done
    printf "\n"
  } >> "$CSV"
}

# --- 主迴圈：所有 cfg x benches 全跑 ---
for cfgname in ghb_d1 ghb_d2 ghb_d4 ghb_d8 ghb_d16; do
  for bench in "${BENCHES[@]}"; do
    run_one "$cfgname" "$bench"
  done
done

echo
echo "[DONE] CSV: $CSV"
echo "[HINT] Inspect one simout to confirm stat keys:"
echo "       less $OUTDIR/cc1.baseline.simout"
