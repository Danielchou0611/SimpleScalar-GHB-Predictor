#!/usr/bin/env bash
set -u
set -o pipefail

SIM=./sim-outorder
PROGDIR=benchmarks_little/Programs
BASE_OUT=results_phase
mkdir -p "$BASE_OUT"

# default window for phases unless overridden below
MAXINST=${MAXINST:-5000000}

# phases (fastfwd points)
PHASES=(100000 10000000 20000000)

# keep only the long-running ones for phase study
BENCHES=(perl go)

# deterministic cfg order
CFG_ORDER=(baseline ghb_d1)

declare -A CFG
CFG[baseline]=""
CFG[ghb_d1]="-ghb:enable -ghb:degree 1"

STAT_KEYS=(
  sim_num_insn sim_num_refs sim_elapsed_time sim_inst_rate sim_cycle sim_IPC sim_CPI
  il1.miss_rate dl1.miss_rate ul2.miss_rate
)

get_stat () {
  local key="$1" file="$2"
  awk -v k="$key" '$1==k {print $2; found=1; exit} END{if(!found) print "NA"}' "$file"
}

run_one () {
  local phase="$1" cfgname="$2" bench="$3"
  local outdir="$BASE_OUT/ff_${phase}"
  mkdir -p "$outdir"

  # phase-specific window length (program-length constraints)
  local maxinst_phase="$MAXINST"
  if [[ "$phase" == "10000000" ]]; then
    maxinst_phase=5000000
  elif [[ "$phase" == "20000000" ]]; then
    maxinst_phase=1000000
  fi

  local bin="$PROGDIR/${bench}.ss"
  local simout="$outdir/${bench}.${cfgname}.simout"
  local progout="$outdir/${bench}.${cfgname}.progout"

  extra_args=()
  if [[ "$bench" == "perl" ]]; then
    extra_args+=(benchmarks_little/Input/perl-tests.pl)
  fi

  echo "[RUN] ff=$phase bench=$bench cfg=$cfgname maxinst=$maxinst_phase"

  # do not let a single failed run kill the whole sweep
  if ! $SIM \
    -fastfwd "$phase" \
    -max:inst "$maxinst_phase" \
    ${CFG[$cfgname]} \
    -redir:sim "$simout" \
    -redir:prog "$progout" \
    "$bin" "${extra_args[@]}" \
    < /dev/null \
    > /dev/null
  then
    echo "[WARN] failed: ff=$phase bench=$bench cfg=$cfgname" >&2
    # ensure the simout exists so summarization doesn't crash
    if [[ ! -f "$simout" ]]; then
      printf "sim_num_insn 0\nsim_IPC NA\nul2.miss_rate NA\n" > "$simout"
    fi
  fi
}

summarize_phase () {
  local phase="$1"
  local outdir="$BASE_OUT/ff_${phase}"
  local csv="$outdir/summary.csv"

  {
    printf "phase,cfg,bench,maxinst"
    for k in "${STAT_KEYS[@]}"; do printf ",%s" "$k"; done
    printf "\n"
  } > "$csv"

  for cfgname in "${CFG_ORDER[@]}"; do
    for bench in "${BENCHES[@]}"; do
      local simout="$outdir/${bench}.${cfgname}.simout"
      # If missing, write NA row instead of dying
      if [[ ! -f "$simout" ]]; then
        {
          printf "%s,%s,%s,%s" "$phase" "$cfgname" "$bench" "$MAXINST"
          for k in "${STAT_KEYS[@]}"; do printf ",NA"; done
          printf "\n"
        } >> "$csv"
        continue
      fi

      {
        printf "%s,%s,%s,%s" "$phase" "$cfgname" "$bench" "$MAXINST"
        for k in "${STAT_KEYS[@]}"; do
          v=$(get_stat "$k" "$simout")
          printf ",%s" "$v"
        done
        printf "\n"
      } >> "$csv"
    done
  done

  echo "[DONE] $csv"
}

# main sweep
for phase in "${PHASES[@]}"; do
  for cfgname in "${CFG_ORDER[@]}"; do
    for bench in "${BENCHES[@]}"; do
      run_one "$phase" "$cfgname" "$bench"
    done
  done
  summarize_phase "$phase"
done

echo "[ALL DONE] Results under: $BASE_OUT/"
