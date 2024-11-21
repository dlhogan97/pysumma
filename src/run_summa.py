# %%
import xarray as xr
import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import pysumma as ps
import pysumma.plotting as psp
import warnings

# pysumma has many depreciated packages, this ignores their warnings
warnings.filterwarnings("ignore", category=UserWarning)

# %%
os.chdir('./src')
executable = 'summa.exe'
filemanager = './model/settings/file_manager.txt'

# Create a pySUMMA simulation object
s = ps.Simulation(executable, filemanager)

# Set the simulation start and end times from forcing file
with open('./forcings/forcing_file_list.txt', 'r') as file:
    # Read the contents
    forcing_file = file.read().replace("'", "")
forcing = xr.open_dataset('./forcings/'+forcing_file.strip(), engine='netcdf4')
time = forcing['time']

dt64 = np.datetime64(time.isel(time=0).values)
dt = pd.to_datetime(dt64)
start = dt.strftime('%Y-%m-%d %H:%M')
dt64 = np.datetime64(time.isel(time=-1).values)
dt = pd.to_datetime(dt64)
end = dt.strftime('%Y-%m-%d %H:%M')

s.manager['simStartTime'] = start
s.manager['simEndTime'] = end

# Set params
s.decisions['snowLayers'] = 'jrdn1991'
s.decisions['thCondSnow'] = 'jrdn1991'
s.decisions['snowDenNew'] = 'hedAndPom'
s.decisions['compaction'] = 'consettl'
s.decisions['astability'] = 'mahrtexp'

s.global_hru_params['tempCritRain'] = 274.15
s.global_hru_params['newSnowDenMin'] = 100
s.global_hru_params['densScalGrowth'] = 0.10
s.global_hru_params['densScalOvrbdn'] = 0.025
# s.global_hru_params['fixedThermalCond_snow'] = 0.35

# Add in some additional variables so we can demonstrate plotting capabilities
output_settings = {'period': 1, 'instant': 1, 'sum': 0, 
              'mean': 0, 'variance': 0, 'min': 0, 'max': 0}
layer_vars = ['mLayerTemp', 'mLayerDepth', 'mLayerHeight',
              'mLayerLiqFluxSoil', 'mLayerVolFracIce', 'mLayerVolFracLiq', 
              'mLayerVolFracWat','mLayerMatricHead', 'iLayerHeight', 'scalarSnowDepth', 'nSnow']

# Create the new variables
for var in layer_vars:
    s.output_control[var] = output_settings

# Ensure all variables have the same statistics
all_vars = set(layer_vars + [o.name for o in s.output_control.options])
for var in all_vars:
    s.output_control[var] = output_settings

out_name = os.path.splitext(forcing_file)[0]
# Run the model, specify the output suffix
s.run('local', run_suffix=out_name)

# %%
print(s.status)

# %%



