# RocketPill
 
This is a data and ML driven simulator for rockets, from launch through flight. The outline is to include the following main components:
1. A time series LLM or other Deep learning model to generate rocket engine's thrust
2. An environmental model to simulate the wind and drag acting on the rocket, such as a pretrained weather DL model to simulate the wind and pressures at the launch site
3. Structural Integrity/Fault Tolerance model: basically a way to simulate how the rocket launch and environmental effects affect the rocket itself and may cause errors and failure.

Datasets and models are pushed to Hugging Face hub: https://huggingface.co/shaddie
