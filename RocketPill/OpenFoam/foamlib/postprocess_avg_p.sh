#!/usr/bin/env bash
# postprocess_avg_p.sh
set -e
if [ ! -z "$1" ]; then
    cd "$1"
fi
out=latest_avg_p.txt
dirs=(postProcessing/fieldAverage* postProcessing/fieldAverage)
latest=""
for d in "${dirs[@]}"; do
    if [ -d "$d" ]; then
        last=$(ls -1 "$d" 2>/dev/null | sort -V | tail -n1)
        if [ -n "$last" ]; then
            pfile="$d/$last/p"
            if [ -f "$pfile" ]; then
                latest="$pfile"
            fi
        fi
    fi
done
if [ -z "$latest" ]; then
    echo "No averaged pressure found" >&2
    exit 1
fi
val=$(grep -Eo '[-+]?[0-9]*\.?[0-9]+' "$latest" | head -n1)
if [ -z "$val" ]; then
    echo "Could not parse numeric value" >&2
    exit 1
fi
echo "$val" > "$out"
echo "Wrote avg p = $val to $out"
