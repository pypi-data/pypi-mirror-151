import numpy as np
import logging
from scipy.signal import savgol_filter
import scipy.interpolate as si

def tof2eng(tof,tt,ee,noise=0,L=391,t0=3.673):
    """
    covert tof data to energy spectra.

    :param tof: 1D or 2D array like tof data. Each row is a tof measurement if 2D.
    :param tt: time points for tof data (ns)
    :param ee: 1d array,energy points (eV)
    :param L: fly length (mm)
    :param t0: time offset (ns)
    :return energy spectra
    """ 
    tof = np.array(tof)
    tt = np.array(tt)
    ee = np.array(ee)
    MM = len(ee)
    ee = np.append(ee,2*ee[-1]-ee[-2])
    if tof.ndim == 1:
        N = 1
    else:
        N = tof.shape[0]
    
    # remove noise
    inds = np.where(tof<=noise)
    tof[inds] = 0

    spectra = []
    for ii in range(N):
        spec=[]
        for jj in range(MM):
            spec.append(count4eng(tof[ii],tt,ee[jj],ee[jj+1],L,t0))
        spectra.append(spec)
    
    spectra = np.array(spectra)

    return spectra

def count4eng(tof,tt,e0,e1,L=391,t0=3.673):
    """
    count electrons in one energy range.

    :param tof: 1D tof data.
    :param tt: time points for tof data (ns)
    :param e0: energy start point (eV)
    :param e1: energy end point (eV)
    :param L: fly length (mm)
    :param t0: time offset (ns)
    :return counts
    """ 
    te0 = eng2time(e0,L,t0)
    te1 = eng2time(e1,L,t0)
    inds = np.where((tt>=min(te0,te1)) & (tt<max(te0,te1)))[0]
    if len(inds)==0:
        logging.warning(f'energy inteval ({e0},{e1}) is not in tof data')
    return np.sum(tof[inds])

def time2eng(t,L=391,t0=3.673):
    return 2.84375*L**2/((t-t0)**2)

def eng2time(eng,L=391,t0=3.673):
    return L*np.sqrt(2.84375/eng)+t0

def smoothtrace(trace,npoints=31,order=2,axis=0):
    return savgol_filter(trace,npoints, order, axis=axis)

def normtrace(trace,method='sum',axis=1):
    if axis==1:
        trace = trace.T
    
    M = trace.shape[0]
    for ii in range(M):
        if method.lower() == 'max':
            Mdata = np.max(trace[ii,:])
        elif method.lower() == 'sum':
            Mdata = np.sum(trace[ii,:])
        else:
            Mdata = 1
            logging.warn('Unrecognized normalization parameter: {method}')
        trace[ii,:] = trace[ii,:]/Mdata

    if axis==1:
        trace = trace.T
    
    trace = trace/np.max(np.max(trace))
    return trace

def resample(x,y,data,MM):
    T_Range = np.max(x) - np.min(x)
    delta_E = 1/(T_Range*1e-15)*6.626e-34/1.6e-19   # eV
    xx = np.linspace(0, T_Range, MM)
    yy = np.linspace(0, (MM-1)*delta_E, MM)

    ff = si.interp2d(x,y,data,kind="cubic", copy=True, bounds_error=False, fill_value=0)

    Data = ff(xx, yy)
    return (Data,xx,yy)