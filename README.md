# viscosity_nemd
 Codes for running NEMD to compute viscosity on LAMMPS and post-processing the results



Directory Structure
------
    .

    └── data                 # Data files
        ├── archive_nemd     # Input & output files of NEMD simulations in LAMMPS
        ├── archive_eq       # Input & output files for equilibration in LAMMPS
        ├── visc             # All the viscosity outputs
        ├── eq_system        # Equilibrated systems
    └── src                  # Codes for post-processing LAMMPS outputs
        ├── lmpoutpose.py    # Module for post-processing general output of LAMMPS ave/time fix
        ├── viscpost.py      # Module for post-processing viscosity data
        ├── lmpcopy.py       # Module for organizing the files in different folders    
        ├── utility.py       # High-level functions for quick processing and analysis of results
    ├── reports              # Jupyter notebooks that call src modules to analyze the results
    ├── lmpscript            # LAMMPS scripts to perform equilibration and NEMD simulation
