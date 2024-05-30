# pysumma

# Local PySumma Setup
Use the `environment.yml` file to set up. 

# Install MiniForge
**Note: to make my life easier, I did a clean install of miniforge, here are the direstions on how to do that:**
Cleaned python install - installed miniforge:
	1. *Important!!!* Save all environments to some local lcations
	2. Uninstall anaconda (this will delete everything, so make sure you're okay with that!)
	3. Uninstalled miniconda (if you have miniconda)
	4. Installed miniforge built through (conda-forge)[https://github.com/conda-forge/miniforge]
	5. Ran miniforge on my computer

Once installed:
	6. Clean.bash_profile to not include any anaconda references
	7. Checked PATH variables to make sure that the correct reference to miniforge is made
	8. I had some issues with creating a new environment from the prior yaml file
		a. Ended up trying to log back into the linux box
			i. This failed because of some issues with running cmd.exe
				1) To solve this I
					a)  removed the anaconda reference is the ps file in WindowsPowershell within my OneDrive - UW documents folder
					b) For windows: I ran this command in powershell: 
					`C:\Windows\System32\reg.exe DELETE "HKCU\Software\Microsoft\Command Processor" /v AutoRun /f`
					From <https://stackoverflow.com/questions/65683807/visual-studio-code-unable-to-ssh-using-the-remote-extension-anymore-error-code-2> 
		- May try running this command conda env export -n py36 -f py36.yml --from-history. Can also do a "--no-builds" which may work
		- This pretty much worked. Lastly had to run mamba init bash in my bash terminal to get it to work there too.
		From <https://stackoverflow.com/questions/55554431/conda-fails-to-create-environment-from-yml> 

# Tips & Tricks
- Even though HRU may be irrelevant, the order of forcing files **MUST** be (time, HRU) within the forcing dataset. 
- Default HRU is 1. 
- variable datatype have to match the requirements (float=float)
- Radiation is all downward input, upwelling radiation is solved later. 
- `s.decisions` lists all the model decisions and a brief description
- `s.global_hru_params` lists the actual parameter value and can be changed by calling the key of interest
- HRU = Hydrologic Response Unit, GRU = Grouped Response Unit.