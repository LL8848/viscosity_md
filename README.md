# viscosity_nemd
 Codes for running NEMD to compute viscosity on LAMMPS and post-processing the results



Directory Structure
------
    .
    ├── data                 # All the datafiles for experiments are here, read the readme inside
    ├── lmpscript            # Main fugures are here
    ├── models               # Pretrained LSTM models are here
    ├── paper                # latex files for the paper
    ├── reports              # Supporting python scripts for MD-visualization
    └── data                 # Codes needed to run RNN-MD
        ├── config           # All the configurations for RNN models are in YAML files
        ├── md-codes         # MD codes in python and c++
        ├── model            # Main codebase for RNN-MD
        ├── paper-figures    # Python notebooks used to generate the figures for the paper
        ├── spec.._local     # Python notebook version of the RNN-MD 
        ├── spec.._colab     # google colab notebook version of the RNN-MD 
        ├── temp_data        # temporary data folders for visualization
        ├── DW-Ex..ipynb     # Double well experiment
        ├── LJ-Ex..ipynb     # Lennord Jones experiment
        ├── Ru.-Ex..ipynb    # Rugged potential experiment
        ├── SHO-Ex..ipynb    # SHO experiment        
        ├── Ma.-Ex..ipynb    # Many particle PB experiment 
 
