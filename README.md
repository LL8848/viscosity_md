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


General Workflow
------
1.	Download files from the server to local:  ```.\data\new```
2.	Open a iPython-like terminal or a Juypter notebook, cd to ```.\data\new```, use ```vba=analyze()``` to quick-check all the new data; use ```plot('filename')``` to visualize pressure, energy, etc.
    * use ```vd = vba.get(srate)``` to quickly retrieve a dataset for a state point
    * deep steady-state check: use ```vd.acf()```, ```vd.ssplot()```, ```vd.setss1()```, etc
3.	If steady-state is reached, run ```copy('PEC5')``` to copy the visc_ file to the ```.\PEC5_visc```. Move all files in ```./data/new``` out to ```./data/archive```. Otherwise go back to LAMMPS for longer simulation until reaching steady-state.
4.	Create a Jupyter notebook (may use an existing template) to do analysis and write report.  Export results if necessary for later OriginLab plot making.


Cheatsheet for the source code
------
