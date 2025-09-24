    #!/usr/bin/env bash
    caseDir="$1"
    if [ -z "$caseDir" ]; then
        caseDir="."
    fi
    infile="$caseDir/constant/inletMassFlux"
    if [ ! -f "$infile" ]; then
        echo "No inletMassFlux file at $infile"
        exit 1
    fi
    massFlux=$(sed -n '1p' "$infile" | tr -d '# ' )
    area=$(sed -n '2p' "$infile" | tr -d '# ' )
    if [ -z "$massFlux" ] || [ -z "$area" ]; then
        echo "inletMassFlux file must contain massFlux then patch_area on lines 1 and 2"
        exit 1
    fi
    rho=${2:-1.0}
    Umag=$(python3 - <<PY
import sys
m=float(sys.argv[1]); a=float(sys.argv[2]); r=float(sys.argv[3])
if a==0:
    print(0.0)
else:
    print(m/(r*a))
PY
    "$massFlux" "$area" "$rho")
    Ufile="$caseDir/0/U"
    if [ ! -f "$Ufile" ]; then
        echo "No 0/U file at $Ufile"
        exit 1
    fi
    start_marker='/* PATCH inlet START */'
    end_marker='/* PATCH inlet END */'
    awk -v s="$start_marker" -v e="$end_marker" -v U="$Umag" '
    BEGIN{inside=0}
    {
        if(index($0,s)) { print; print "inlet"; print "{"; print "    type            fixedValue;"; printf("    value           uniform (%s 0 0);\n", U); print "}"; inside=1; skip=1; next }
        if(index($0,e)) { inside=0; print; next }
        if(!inside) print
    }' "$Ufile" > "$Ufile.tmp" && mv "$Ufile.tmp" "$Ufile"
    echo "Wrote inlet velocity magnitude $Umag to $Ufile"
