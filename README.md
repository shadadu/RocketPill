# RocketPill

Simulation of rocket engines using off-the-shelf simulators and complexity science to support instability analysis and failure prediction in rocket engines and vehicles.

1. A time series LLM (based on the Informer Model) to predict thrust curve for generating launch and flight using thrust curve data
2. Pressure curve time series model to generate the chamber
3. Foamlib/OpenFoam simulation to solve for the wall pressure given the bulk chamber pressure curve
3. A time series and complexity science based model to predict on-set of Thermoacoustic instability: on-set of instabilities are known to be associated with transition from steady states to periodic states. Juniper & Sujith: Sensitivity and Nonlinearity of Thermoacoustic Oscillations  

Datasets and models are pushed to Hugging Face hub: https://huggingface.co/shaddie

## Data Sources
1. thrustcurve.org API: https://www.thrustcurve.org/api/v1
2. NASA Apollo Mission data:
   https://ntrs.nasa.gov/api/citations/19690026499/downloads/19690026499.pdf
   https://web.archive.org/web/20170313142729/http://www.braeunig.us/apollo/saturnV.htm
   https://www.ibiblio.org/apollo/Documents/lvfea-AS506-Apollo11.pdf
   https://elib.dlr.de/140508/1/apollo11_reloaded.pdf
   https://www.ibiblio.org/apollo/Documents/19920075301.pdf
   https://space.stackexchange.com/questions/40074/if-i-wanted-to-reconstruct-an-entire-apollo-missions-crewed-spacecraft-trajecto
3.  


