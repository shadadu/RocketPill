import os


def ensure_functionObjects_in_controlDict(case_dir, inlet_patch, chamber_region_name="internalCells"):
    """
    Append useful functionObjects (fieldAverage, surfaceRegion/faceSource) into system/controlDict (functions section)
    so that during the run the solver writes:
      - volume-averaged pressure (postProcessing/fieldAverage...),
      - inlet massflow/phi (postProcessing/faceSource... or surfaceRegion).
    This adds a 'functions' section to controlDict if absent. If you already have functions configured, merge manually.
    """
    control = os.path.join(case_dir, "system", "controlDict")
    if not os.path.exists(control):
        raise FileNotFoundError("system/controlDict not found at: " + control)
    text = open(control).read()
    # Simple check — do not duplicate if already present
    if "fieldAverage_chamberPressure" in text:
        print("controlDict already contains functionObjects for averaging — skipping edit.")
        return
    functions_block = f"""
        functions
        {{
            fieldAverage_chamberPressure
            {{
                type            fieldAverage;
                functionObjectLibs ("libfieldFunctionObjects.so");
                enabled         true;
                writeControl    timeStep;
                writeInterval   1;
                log             true;
                fields
                (
                    p
                );
            }}
        
            inlet_massflow
            {{
                type            surfaceFieldValue;
                functionObjectLibs ("libfieldFunctionObjects.so");
                enabled         true;
                writeControl    timeStep;
                writeInterval   1;
                log             true;
                operation       sum;
                regionType      patch;
                regionName      {inlet_patch};
                fields
                (
                    phi
                );
            }}
        
            # Also capture average pressure on the chamberWall patch (optional)
            patchAverage_chamberWall
            {{
                type            patchAverage;
                functionObjectLibs ("libfieldFunctionObjects.so");
                enabled         true;
                writeControl    timeStep;
                writeInterval   1;
                log             true;
                patches
                (
                    chamberWall
                );
                fields
                (
                    p
                );
            }}
        }}
        """
    # append functions before end of file (very naive)
    if "functions" in text:
        print(
            "controlDict already has a functions entry — skipping automatic append. Please add functionObjects manually.")
        return
    text2 = text + "\n\n" + functions_block
    open(control, "w").write(text2)
    print("Appended functionObjects (fieldAverage_inlet_massflow_patchAverage) to system/controlDict")
