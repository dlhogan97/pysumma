# pysumma

# Local PySumma Setup
Use the `environment.yml` file to set up. 

# Install MiniForge (Highly recommended! Maybe even required?)
**Note: to make my life easier, I did a clean install of miniforge, here are the directions on how to do that:**

Clean python install - installed miniforge:

	1. *Important!!!* Save all environments to a local location
	2. Uninstall Anaconda (this will delete everything, so make sure you're okay with that!)
	3. Uninstall miniconda (if you have miniconda)
	4. Install miniforge build through (conda-forge)[https://github.com/conda-forge/miniforge]
	5. Run miniforge on your computer

Once installed:

	6. Clean .bash_profile to not include any anaconda references
	7. Check PATH variables to make sure that the correct reference to miniforge is made
	8. I had some issues with creating a new environment from the yaml files I saved in step 1.
		a. I ended up trying to log back into the linux box
			i. This failed because of some issues with running cmd.exe
				1) To solve this I
					a)  removed the Anaconda reference is the ps file in WindowsPowershell within my OneDrive - UW documents folder
					b) For windows: I ran this command in powershell: 
					`C:\Windows\System32\reg.exe DELETE "HKCU\Software\Microsoft\Command Processor" /v AutoRun /f`
					From <https://stackoverflow.com/questions/65683807/visual-studio-code-unable-to-ssh-using-the-remote-extension-anymore-error-code-2> 
		- Ran this command: conda env export -n py36 -f py36.yml --from-history. Can also do a "--no-builds" which may work
	9. Lastly run - mamba init bash - in bash terminal to get it to work there too.
		From <https://stackoverflow.com/questions/55554431/conda-fails-to-create-environment-from-yml> 

### To produce forcing file:
1. Ensure `metpy`, `metloom`, and `metsim` are installed (this should automatically be done if using the default environment file)
2. Run the `snotel_to_pysumma.ipynb` notebook *note that this file will be updated to a script in the future*, this will create a number of folders in the root directory.
### To run pysumma on this new file:
1. In the `tutorial/data` folder copy the `cues` folder and rename the copied folder to relate to your file (`my_site`).
2. Move the new forcing file in `./model/forcings` to the `tutorial/data/my_site/data` folder.
3. Copy this name file to the `tutorial/data/my_site/summa_setup/` folder.
4. Open `tutorial/data/my_site/summa_setup/forcing_file_list.txt` and change the filename to be the name of your forcing file.
5. Open `tutorial/data/my_site/summa_setup/file_manager.txt` and change *simEndTime* and *simStartTime* to reflect the start and end times of your forcing file. These are printed out at the end of the `snotel_to_pysumma.ipynb`.
6. In this same file, ensure that *settingsPath*, *forcingPath*, and *outputPath* are all correct. It is likely that they need to be updated to your site name.
7. Open `summa_run_tutorial.ipynb` and update `filemanager` variable in the first cell to the locaiton of `tutorial/data/my_site/summa_setup/file_manager.txt`
8. Run the code and get your SUMMA run!


# Tips & Tricks
- Even though HRU may be irrelevant, the order of forcing files **MUST** be (time, HRU) within the forcing dataset. 
- Default HRU is 1. 
- variable datatype have to match the requirements (float=float)
- Radiation is all downward input, upwelling radiation is solved later. 
- `s.decisions` lists all the model decisions and a brief description
- `s.global_hru_params` lists the actual parameter value and can be changed by calling the key of interest
- HRU = Hydrologic Response Unit, GRU = Grouped Response Unit.
