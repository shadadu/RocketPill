# RocketPill

This is a data and ML driven simulator for rockets to aid in general and failure testing before launch. The outline is to include the following main components:
1. A time series LLM (based on the Informer Model) to predict thrust curve for generating launch and flight
2. Pressure curve time series model to generate the chamber and wall pressure in combo
3. Thermoacoustic instability model to predict possible pressure, heat, and acoustic instabilities
4. Structural Integrity/Fault Tolerance model: Deduce or predict how the rocket's structure or walls respond or tolerate the Pressure curve and Thermoacoustic instablities. Currently, we are looking at a Finite Element (FE) Sectional-Tolerance model of the Rocket vehicle. This in a way means scanning the 3D rocket vehicle and combining or splitting components into finite element sections. Each FE section's tolerances (min/max tolerances) in terms of the factors that matter (pressure, heat, acoustic vibrations, etc) are then assigned. This FE tolerance model can then be used to simulate structural integrity during launch and flight. For example: Optimizing structural integrity of a pressure vessel via finite element analysis and machine learning based XGBoost approaches: https://www.nature.com/articles/s41598-025-96472-y
5. An environmental model to simulate the wind and drag acting on the rocket, such as a pretrained weather DL model to simulate the wind and pressures at the launch site
6. A visual or animation component using Unity/C#. Plug the model components into a Unity rocket simulation framework to enable visualizing the rocket launch and flight simulation. 

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


