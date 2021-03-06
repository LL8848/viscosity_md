# Viscosity Prediction through Non-Equilibrium Molecular Dynamics Simulation
Lingnan Lin, April 2020

What this code does
------
* Prepare scripts for standard non-equilibrium molecular dynamics (NEMD) simulation in LAMMPS to compute viscosity.
* Post-process the outputs from LAMMPS and perform comprehensive analysis.
* Users can predict the viscosity of any liquid for various temperature, pressure and shear rate.
* Users can perform block averaging and autocorrelation analysis to evaluate the computing uncertainties and sampling quality.
* Users can fit the shear viscosities to a rheology model to extrapolate the Newtonian viscosity. Supported models include Eyring, Carreau, Carreau-Yasuda, Cross. Users can also add their own models by writing a Python function using the template.
* Several fully equilibrated systems of polyol esters are provided.  Available chemicals include: pentaerythritol tetrapentanoate (POE5), pentaerythritol tetrahexanoate (PEC6), pentaerythritol tetraheptanoate (POE7), and pentaerythritol tetranonanoate (POE9). Temperature ranges from 258 K to 373 K.  Pressure ranges from 0.1 MPa to 300 MPa.  I'll constantly upload the systems I made to share with you.

License & Citation
------
This code is licensed under the Apache v2 license. Feel free to use all or portions for your research or related projects so long as you provide the following citation information:

*Lin, L., Kedzierski, M., 2020. Density and viscosity of a polyol ester lubricant: Measurement and molecular dynamics simulation. Int. J. Refrig. 118, 188–201. https://doi.org/10.1016/j.ijrefrig.2020.07.004*

    @article{Lin2020,
    author = {Lin, Lingnan and Kedzierski, Mark},
    doi = {10.1016/j.ijrefrig.2020.07.004},
    issn = {0140-7007},
    journal = {International Journal of Refrigeration},
    keywords = {Lubrication,Molecular simulation,NEMD,POE oil,Rheology,Transport property},
    pages = {188--201},
    publisher = {Elsevier Ltd},
    title = {{Density and viscosity of a polyol ester lubricant: Measurement and molecular dynamics simulation}},
    url = {https://doi.org/10.1016/j.ijrefrig.2020.07.004},
    volume = {118},
    year = {2020}
    }

Dependencies
------
* The molecular dynamics simulations are done in [LAMMPS](https://lammps.sandia.gov/). 
* The pre- and post-processing code is written in Python 3, which depends on Python libraries including numpy, pandas, matplotlib, scipy, os, etc.  [Anaconda](https://www.anaconda.com/) is the recommended Python platform since it installs all dependencies.

Directory Structure
------
    .

    └── data                  # Data files
        ├── archive_nemd      # Input & output files of NEMD simulations in LAMMPS
        ├── archive_eq        # Input & output files for equilibration in LAMMPS
        ├── visc              # All the viscosity outputs
        ├── eq_system         # Equilibrated systems
        ├── new               # New files are placed here temporarily
    └── src                   # Codes for post-processing LAMMPS outputs
        ├── lmpoutpose.py     # Module for post-processing general output of LAMMPS ave/time fix
        ├── viscpost.py       # Module for post-processing viscosity data
        ├── rheologymodels.py # Module for various rheology models that are used to fit the shear viscosity
        ├── lmpcopy.py        # Module for organizing the files in different folders    
        ├── utility.py        # High-level functions for quick processing and analysis of results
    ├── reports               # Jupyter notebooks that call src modules to analyze the results
    ├── lmpscript             # LAMMPS scripts to perform equilibration and NEMD simulation


General Workflow
------
1.	Use the scripts in ```/lmpscript``` to run equilbration and NEMD simulations using LAMMPS on a HPC server.
2.  When computation completed, download the files from the server to:  ```./data/new```.
3.	Open a iPython-like terminal or a Juypter notebook, cd to ```./data/new```, import the modules in ```/src``` to post-process and analyze the data. Here are some tips:
    * Use ```vba = analyze()``` to quick-check all the viscosity output files in ```./data/new```. ```vba``` is a ```BatchData``` class that has a bunch of useful functions you can play with to analyze the viscosity data.
    * Use ```plot('filename')``` to visualize the output files that compute pressure, energy, etc. as a function of time. This is primarily to check if the equilibration or steady state is reached.
    * Use ```vd = vba.get(srate)``` to quickly retrieve a dataset for a state point where srate is the shear rate (1/s), e.g, 1e8, 1e9. ```vd``` is a ```ViscData``` class that also has a bunch of useful functions for analysis.
    * Deep steady-state check: use ```vd.acf()```, ```vd.ssplot()```, ```vd.setss1()```, etc
    * Check the [Cheatsheet](/cheatsheet.pdf) I made for the complete usage of the functions and classes.
4.	If steady-state is reached and desired statistical accuracy has been achieved, run ```copy('Path')``` to copy the visc_ file to the ```./data/visc```. Move all files in ```./data/new``` to ```./data/archive```. Otherwise go back to LAMMPS for longer simulation until obtaining the desired results.
5.	Create a Jupyter notebook to do analysis and write report using the modules in ```./src``` and the data in ```./data/visc```.  Export results if necessary for publication and making figures using other software.

Tutorials 
------
* How to compute viscosity?
* How to check the equilibrium or steady-state?
* How to fit the shear viscosity to a model and calculate the Newtonian viscosity?
* [Cheatsheet for the post-processing modules](/cheatsheet.pdf).

To-do 
------
- [ ] Complete the tutorials.


Contact 
------
Feel free to contact me should you have any questions:
Lingnan Lin, Ph.D.
Email: lingnan dot lin at nist dot gov
