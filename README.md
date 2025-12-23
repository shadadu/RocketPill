# RocketPill


### About this Project (& Literature Review)
This project builds a digital twin or high fidelity simulation of a rocket vehicle to support combustion instability analysis and vehicle failure prediction and mitigation. 

The strategy is a CFD simulation based on the Navier-Stokes Equations and its proven CFD solutions in the literature. The Navier Stokes equations are famously unsolved for all continuous cases (see the Millenium Price: https://www.claymath.org/millennium/navier-stokes-equation/). This paper Navier Stokes: Singularities and Bifurcations by Santos and Sale discusses the global regularity issues and singularities pertaining to Navier-Stokes: https://www.researchgate.net/publication/385006962_Navier-Stokes_Singularities_and_Bifurcations  

An excellent series of lectures on CFD, the Navier Stokes equations, and prediction of turbulent or chaotic scenarios is by Prof S.A.E. Miller: https://www.youtube.com/watch?v=01X5ECv3qIU&list=PLbiOzt50Bx-kV3Lcn5piPyV9EvpmOybJR. This short tutorial "A guide to writing your first CFD solver" by Mark Owkes is also a good start to writing a CFD Solver: https://www.montana.edu/mowkes/research/source-codes/GuideToCFD.pdf.  

Current methods to predict on-set of turbulence or chaos include empirical-numerical methods or methods that can be classified as data science. Empirical numerical methods trigger instabilities with special parameters or factors or specify regions or initial conditions with such triggering behaviors. Data methods collect data with on-set of instabilities and attempt to use time series and other methods to model and then predict the transitions to instability or turbulence or chaos.
 
The chaotic or turbulent regime, and thermoacoustic instability analysis are important approaches that researchers use to study and predict combustion instabilities. This project will start exploring the chaotic or turbulent approach, and then, add the TAI approach per resource and time constraints. 

The aim of this project then is a combustion simulation coupled with a minimal high fidelity vehicle structure simulation to predict how pressure and other combustion-related effects may cause structural integrity issues.

# Data Simulation

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


