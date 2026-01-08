# RocketPill


### About this Project (& Literature Review)
This project builds a digital twin or high fidelity simulation of a rocket vehicle to support combustion instability analysis and vehicle failure prediction and mitigation. 

The strategy is a CFD simulation based on the Navier-Stokes Equations and its proven CFD solutions in the literature. The Navier Stokes equations are famously unsolved for all continuous cases (see the Millenium Price: https://www.claymath.org/millennium/navier-stokes-equation/). This paper Navier Stokes: Singularities and Bifurcations by Santos and Sale, and Singularity of Navier-Stokes Equations Leading to Turbulence by Hua-Shu Dou discusses the global regularity issues, turbulence and singularities pertaining to Navier-Stokes: https://www.researchgate.net/publication/385006962_Navier-Stokes_Singularities_and_Bifurcations, https://arxiv.org/pdf/1805.12053 

An excellent series of lectures on CFD, the Navier Stokes equations, and prediction of turbulent or chaotic scenarios is by Prof S.A.E. Miller: https://www.youtube.com/watch?v=01X5ECv3qIU&list=PLbiOzt50Bx-kV3Lcn5piPyV9EvpmOybJR. This short tutorial "A guide to writing your first CFD solver" by Mark Owkes is also a good start to writing a CFD Solver: https://www.montana.edu/mowkes/research/source-codes/GuideToCFD.pdf.

So, in a nutshell, while there have been successful attempts at solving or fully-analytically describing the solutions of the Navier-Stokes equations for limited conditions and bounds, there is as yet no complete analytical solution of the Navier Stokes, or an analytical result proving that such analytical result is impossible. Hence, the Navier-Stokes millenium challenge is still open. Recently, arguably the closest, attempt was by Terence Tao "Finite Time Blow up for an averaged three-dimensional Navier-Stokes Equation".

While Navier-Stokes isn't analytically solved, numerial solutions of it have found uses in many applications, from aerospace engineering, weather forecasts, geophysical models, rocketry, to name just a few. Data driven and hybrid numerical-deep learning approaches such as Physics Informed Neural Networks(PINNs) have also been applied to provide useful solutions to the Navier Stokes equations.  

Current methods to predict on-set of turbulence or chaos include empirical-numerical methods or methods that can be classified as data science, including PINNs. Empirical numerical methods trigger instabilities with special parameters or factors or specify regions or initial conditions with such triggering behaviors. Data methods collect data with on-set of instabilities and attempt to use time series and other methods to model and then predict the transitions to instability or turbulence or chaos.
 
The chaotic or turbulent regime, and thermoacoustic instability analysis are important approaches that researchers use to study and predict combustion instabilities. This project will start exploring the chaotic or turbulent approach, and then, add the TAI approach per resource and time constraints. 

The aim of this project then is a combustion simulation coupled with a minimal high fidelity vehicle structure simulation to predict how pressure and other combustion-related effects may cause structural integrity issues. To achieve this, we start our simulation implementation from the point of Wang and Chen "Unified Navier-Stokes Flowfield and Performance Analysis of Liquid Rocket Engines": http://ftp.demec.ufpr.br/CFD/bibliografia/propulsao/wang_chen_1993.pdf. As noted in the paper, previous simulation efforts utilized combined piecewise, or assembled composite solutions in series. These stages generally consist of a (1) Combustion chamber (modeled with chemical equilibrium analysis) (2) Supersonic or core flow region (3) Wall and shear layers (4) Nozzle or plume flowfield, modeled with CFD. 

There are unique challenges in developing CFD for Rocket engines, owing mainly to the extreme conditions of and the tightly coupled physics involved. See Swiderski "Current challenges in computational fluid dynamics with regard to rocket engine thrust chamber simulation". The solution deployed by researchers is a chemical-geometric Navier-Stokes system of equations that looks at the  

# CFD References
1. Lecture Notes by S. A. E. Miller: https://www.youtube.com/watch?v=01X5ECv3qIU&list=PLbiOzt50Bx-kV3Lcn5piPyV9EvpmOybJR
2. H. Langtangen, Numerical methods for the Navier-Stokes equations.
3. K. Swiderski, Current challenges in computational fluid dynamics with regard to rocket engine thrust chamber simulation
4. Jameson et al. Numerical Solution of the Euler Equations by Finite Volume Methods and Using Runge-Kutta Time-Stepping Schemes
5. Chen et al. NASA Contractor Report, A Computer Code for Multiphase All-Speed Transient Flows in Complex Geometries: https://ntrs.nasa.gov/api/citations/19920010138/downloads/19920010138.pdf


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


