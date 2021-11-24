import ROOT
import numpy as np
import pandas as pd
import os

def get_xy_from_TGraph(graph): 
    
    n = graph.GetN()
    x = np.asarray([])
    y = np.asarray([])

    for i in range(n): 
        x = np.append(x, graph.GetPointX(i))
        y = np.append(y, graph.GetPointY(i))
    return x, y


def waveform_integral(xarray,yarray, intmin, intmax): 
    
    xarraycut = np.asarray([xarray[i] for i in range(len(xarray)) if intmin<xarray[i]<intmax])
    yarraycut = np.asarray([yarray[i] for i in range(len(xarray)) if intmin<xarray[i]<intmax])
    
    ymin_extra = np.interp(intmin, xarray, yarray)
    ymax_extra = np.interp(intmax, xarray, yarray)
    
    xarraycut = np.concatenate([[intmin],xarraycut,[intmax]])
    yarraycut = np.concatenate([[ymin_extra],yarraycut,[ymax_extra]])
    
    return np.trapz(yarraycut, x=xarraycut)

def get_half_level_crossing(xarray, yarray, full_height = True):
    
    if full_height == False:

        minimum = 0
        maximum = np.max(yarray)
        index_of_maximum = 0
        indicies_of_maximum = np.where(yarray == maximum)[0]
        
        if len(indicies_of_maximum) != 1:
            index_of_maximum = indicies_of_maximum[1].item()
        else: index_of_maximum = indicies_of_maximum[0].item()
        
        for i in range(index_of_maximum, -1, -1):  
            if yarray[i] <= 1: break  # possibly too low
            minimum = yarray[i]
       
        return (yarray[index_of_maximum-1] - minimum)/2.0     
    else: return np.amax(yarray)/2

    
def get_time(xarray, yarray, full_height = True):
    
    half_max = get_half_level_crossing(xarray, yarray, full_height)
    indicies_of_maximum = np.where(yarray == np.max(yarray))[0]
    if len(indicies_of_maximum) != 1:
        index_of_maximum = indicies_of_maximum[1].item()
    else: index_of_maximum = indicies_of_maximum[0].item()
    
    xarraycut = xarray[:index_of_maximum] 
    yarraycut = yarray[:index_of_maximum]     
  
    return np.interp(half_max, yarraycut, xarraycut) 

#xarraycut = np.asarray([xarray[i] for i in range(len(xarray)) if -20<xarray[i]<20])
#yarraycut = np.asarray([yarray[i] for i in range(len(xarray)) if -20<xarray[i]<20])
#return np.interp(half_max, yarraycut, xarraycut, left=float('NaN'), right=float('NaN')) 

def get_time_index(xarray, yarray, full_height = False): 
    
    half_max = get_half_level_crossing(xarray, yarray, full_height);
    maxindex = np.argmax(yarray)
    
    xarraycut = xarray[0:maxindex+1]
    yarraycut = yarray[0:maxindex+1]
    
    half_max_index = np.where(yarraycut-half_max > 0, yarraycut-half_max, np.inf).argmin()
    
    return half_max_index-1
    

def get_total_area(xarray,yarray): 
    
    minx = np.amin(xarray)
    maxx = np.amax(xarray)
    
    return waveform_integral(xarray,yarray, intmin=minx, intmax=maxx) 

#area of coarse waveform 
def get_total_area_discretepts(xarray,yarray): 
    
    maxindex = np.argmax(yarray)
    #maxindex = get_time_index(xarray, yarray)
    
    beginindex = maxindex - 3
    endindex = maxindex + 25
    
    xarrayint = xarray[beginindex:endindex]
    yarrayint = yarray[beginindex:endindex]
    
    return np.trapz(yarrayint, x=xarrayint)
      

def get_PSD(xarray, yarray): 
    
    time = get_time(xarray, yarray)
    
    total = waveform_integral(xarray,yarray, intmin=-12+time, intmax=200+time)
    tail  =  waveform_integral(xarray,yarray, intmin=44+time, intmax=200+time)
    
    return tail/total

# PSD of waveforms that are very coars 
def get_PSD_discretepts(xarray, yarray):

    # the indicies are 1 prior to 50 after and 11-50 after
    # since we are starting at 1 index befor the 50% level corssing,
    # that total spectrum is [0,51], and the tail is [12,51] 

    time_index = get_time_index(xarray, yarray) 
    start_index = time_index 
    end_index = time_index + 51
    total = np.trapz(yarray[start_index:end_index], x=xarray[start_index:end_index])

    start_index = time_index + 12
    tail = np.trapz(yarray[start_index:end_index], x=xarray[start_index:end_index])
  
    return tail/total
    
    
    






    
