# viscosity_nemd
 Codes for running NEMD to compute viscosity on LAMMPS and post-processing the results

What this code does
------
* Perform standard non-equilibrium molecular dynamics simulation and analysis for liquid (originally aimmed for polyol esters).
* Users can predict the viscosity of a liquid at various temperature, pressure and shear rate. 
* The molecular dynamics simulations are done in LAMMPS. 
* The pre- and post-processing code is written in Python 3, which depends on Python libraries including numpy, pandas, matplotlib, scipy, os, etc.
* Various rheology models can be used to fit the shear viscosity to extrapolate the Newtonian viscosity. Supported models include Eyring, Carreau, Carreau-Yasuda, Cross.

Directory Structure
------
    .

    └── data                 # Data files
        ├── archive_nemd     # Input & output files of NEMD simulations in LAMMPS
        ├── archive_eq       # Input & output files for equilibration in LAMMPS
        ├── visc             # All the viscosity outputs
        ├── eq_system        # Equilibrated systems
        ├── new              # New files are placed here temporarily
    └── src                  # Codes for post-processing LAMMPS outputs
        ├── lmpoutpose.py    # Module for post-processing general output of LAMMPS ave/time fix
        ├── viscpost.py      # Module for post-processing viscosity data
        ├── lmpcopy.py       # Module for organizing the files in different folders    
        ├── utility.py       # High-level functions for quick processing and analysis of results
    ├── reports              # Jupyter notebooks that call src modules to analyze the results
    ├── lmpscript            # LAMMPS scripts to perform equilibration and NEMD simulation


General Workflow
------
1.	Use the scripts in ```/lmpscript``` to run equilbration and NEMD simulations using LAMMPS on a HPC server.
2.  When computation completed, download the files from the server to local:  ```./data/new```.
3.	Open a iPython-like terminal or a Juypter notebook, cd to ```./data/new```, import the modules in ```/src``` to post-process and analyze the data. Here are some tips:
    * Use ```vba = analyze()``` to quick-check all the viscosity output files in ```./data/new```. ```vba``` is a ```BatchData``` class that has a bunch of useful functions you can play with to analyze the viscosity data.
    * Use ```plot('filename')``` to visualize the output files that compute pressure, energy, etc. as a function of time. This is primarily to check if the equilibration or steady state is reached.
    * Use ```vd = vba.get(srate)``` to quickly retrieve a dataset for a state point where srate is the shear rate (1/s), e.g, 1e8, 1e9. ```vd``` is a ```ViscData``` class that also has a bunch of useful functions for analysis.
    * Deep steady-state check: use ```vd.acf()```, ```vd.ssplot()```, ```vd.setss1()```, etc
    * Check the **cheatsheet** below for the complete usage of the functions and classes.
4.	If steady-state is reached and desired statistical accuracy has been achieved, run ```copy('PEC5')``` to copy the visc_ file to the ```./PEC5_visc```. Move all files in ```./data/new``` out to ```./data/archive```. Otherwise go back to LAMMPS for longer simulation until reaching the desired results.
5.	Create a Jupyter notebook (may use an existing template) to do analysis and write report.  Export results if necessary for later OriginLab plot making.


Cheatsheet for the source code
------
