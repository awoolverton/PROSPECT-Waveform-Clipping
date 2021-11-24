import numpy as np
import pandas as pd
from helper import *

# Takes as imput the x and y arrays representing a waveform template
# Additionally, the clipping_height is specified in order to set where
# clipping begins. Beginning at hmin, the pulse is scaled up to hmax;
# the function returns a dataframe containing how the waveform behaves
# with and without clipping.

def scaling_scan(hmin, hmax, xarray, yarray, clipping_height, descrete = False):
    
    df = pd.DataFrame(columns=['dh', \
                               'scalefactor', \
                               'clipping_height', \
                               'ymax_unclipped', \
                               'ymax_clipped', \
                               'PSD_unclipped', \
                               'PSD_clipped', \
                               'totalarea_unclipped', \
                               'totalarea_clipped', \
                               'time_offset'])
    
    ymax = np.amax(yarray)
    dh_array = np.linspace(hmin, hmax, 500) - ymax
    
    for dh in dh_array: 
        
        scalefactor = (ymax + dh)/ymax
        
        yscaled = yarray*scalefactor
        yscaled_clipped = np.copy(yscaled)
        
        yscaled_clipped[yscaled_clipped > clipping_height] = clipping_height
        
        dh = dh
        scalefactor = scalefactor
        clipping_height = clipping_height
        ymax_unclipped = np.amax(yscaled)
        ymax_clipped = np.amax(yscaled_clipped)
        if descrete:
            PSD_unclipped = get_PSD_discretepts(xarray, yscaled)
            PSD_clipped = get_PSD_discretepts(xarray, yscaled_clipped)
            totalarea_unclipped = get_total_area_discretepts(xarray, yscaled)
            totalarea_clipped = get_total_area_discretepts(xarray, yscaled_clipped) 
        else:  
            PSD_unclipped = get_PSD(xarray, yscaled)
            PSD_clipped = get_PSD(xarray, yscaled_clipped)
            totalarea_unclipped = get_total_area(xarray, yscaled)
            totalarea_clipped = get_total_area(xarray, yscaled_clipped) 

        time_offset = get_time(xarray, yscaled_clipped) - get_time(xarray, yscaled)
        
        df.loc[len(df)] = [dh, \
                           scalefactor, \
                           clipping_height, \
                           ymax_unclipped, \
                           ymax_clipped, \
                           PSD_unclipped, \
                           PSD_clipped, \
                           totalarea_unclipped, \
                           totalarea_clipped, \
                           time_offset]
        
    return df
