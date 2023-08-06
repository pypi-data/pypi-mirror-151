import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import quad
import  logging
import csaps
import matplotlib.pyplot as plt
import time

def SI2Atom(x,PhyQuan):
    PhyQuan = PhyQuan.lower()
    if PhyQuan == "mass":
        y = x/9.1093897e-31 
    elif PhyQuan == "length":
        y = x/5.29177249e-11
    elif PhyQuan == "time":
        y = x/2.41888129e-17
    elif PhyQuan == "velocity":
        y = x/2.188e6
    elif PhyQuan == "angularfrequency":
        y = x/4.13414251e16
    elif PhyQuan == "energy":
        y = x/(27.211*1.6e-19)
    elif PhyQuan == "charge":
        y = x/1.6e-19
    elif PhyQuan == "efield":
        y = x/5.142e11
    elif PhyQuan == "intensity":
        y = x/3.509e20
    elif PhyQuan == "force":
        y = x/8.239e-8
    else:
        print("Undefined Physical Quantity: ", PhyQuan ,"!")
        y = x
    return y

def DataAlign(E_xuv,E_laser,dt,delay):
    # E_xuv: tuple, E_xuv[0] is the time and E_xuv[1] is the E field of XUV
    # E_laser: tuple E_laser[0] is the time and E_laser[1] is E filed of laser pulse
    # dt is expected time interval of both field (dtau must be an integer multiple of dt)

    # adjust dt
    dtau = delay[1]-delay[0]
    M = int(np.round(dtau/dt))
    dt = dtau/M
    # interpolate E_x
    Nt_xuv = (np.max(E_xuv[0])-np.min(E_xuv[0]))/dt
    Nt_xuv = int(2*(Nt_xuv//2))
    t_xuv_0 = np.round(E_xuv[0][0]/dt)*dt
    t_xuv = np.linspace(0,Nt_xuv-1,Nt_xuv)*dt+t_xuv_0
    fE_x = interp1d(E_xuv[0],E_xuv[1],bounds_error=False,kind = 'cubic',fill_value=0)
    E_x = fE_x(t_xuv)
    E_x = (t_xuv,E_x)

    # interpolate E_l
    D1 = int(np.round(delay[0]/dt))
    tl_bl = t_xuv[0] + D1*dt
    D2 = int(np.round(delay[-1]/dt))
    tl_ul = t_xuv[-1] + D2*dt + dt
    Nt_l = int(np.round((tl_ul-tl_bl)/dt))
    t_l = np.linspace(0,Nt_l-1,Nt_l)*dt+tl_bl
    fE_l = interp1d(E_laser[0],E_laser[1],bounds_error=False,kind = 'cubic',fill_value=0)
    E_l = fE_l(t_l)
    E_l = (t_l,E_l)

    Ind = np.array(range(0,len(delay)))*M

    return (E_x,E_l,dt,Ind)
 
def GetOmega(Et,dt,omega0=None):
    # atomic units
    if omega0 is None:
        fft_M = 2**16
        Y = np.abs(np.fft.fft(Et,fft_M))
        f_max = np.argmax(Y[1:int(fft_M/2)])
        omega_L = f_max/(fft_M*dt)*2*np.pi
    else:
        omega_L = omega0
    return omega_L

def Gate(E_laser,energy,Ip=0.79233,theta=0,phase='full',omega_L=None):
    NN = len(energy)
    MM = len(E_laser[0])
    t = E_laser[0]
    dt = t[1]-t[0]

    A_laser = VectorPotential(E_laser[1],dt)
    # calculate phi_t
    nv = np.sqrt(2*energy)
    if phase.lower()=='term2':
        print('here')
        omega0 = GetOmega(E_laser[1],dt,omega0=omega_L)
        (nv,EE) = np.meshgrid(nv,E_laser[1])
        phi = -nv*EE/(2*omega0**2)
    else:
        A_rev = np.flip(A_laser)
        A_rev = np.vstack([A_rev]*NN).T
        nv = np.vstack([nv]*MM)
        phi = nv*A_rev*np.cos(theta) + A_rev**2/2
        phi = np.cumsum(phi,0)*dt
        phi = np.flip(phi,0)

    P_energy = energy + Ip
    Expo = t.reshape((MM,1))@(P_energy).reshape((1,NN))
    res = np.exp(1j*(phi-Expo))
    return res

def Trace(E_xuv,E_laser,Ind,PE_energy,delay,theta=0,phase='full',omega_L=None):
    # All parameters are Atomic Units
    # E_xuv (1d array) is the E field of attosecond XUV pulse
    # E_laser: tuple, E_laser[0] are the time points and E_laser[1] are the E-field of laser pulse
    # E_laser[Ind,0] is the t0 of E_xuv field
    Ip = 21.56/27.211
    NN = len(PE_energy)
    t = E_laser[0]
    dt = t[1]-t[0]

    M = len(E_xuv)
    Exuv = np.reshape(E_xuv,[1,M])
    GateMat = Gate(E_laser,PE_energy,Ip=Ip,theta=theta,phase=phase,omega_L=omega_L)
    result = np.zeros([NN,len(delay)])
    # loop for delay points
    for ii in range(0,len(delay)):
        temp = Exuv.dot(GateMat[Ind[ii]:Ind[ii]+M,:])*dt
        result[:,ii] = np.abs(temp)**2
    result = result/np.max(result)
    return result

def Trace_phi2(E_xuv,E_laser,Ind,PE_energy,delay,omega_L=None):
    # All parameters have same definition as they do in Trace()

    Ip = 21.56/27.211
    NN = len(PE_energy)
    MM = len(E_laser[0])
    M = len(E_xuv)
    t = E_laser[0]
    dt = t[1]-t[0]

    # calculate phi_t
    EE = E_laser[1]
    if omega_L is None:
        fft_M = 2**16
        Y = np.abs(np.fft.fft(EE,fft_M))
        f_max = np.argmax(Y[1:int(fft_M/2)])
        omega_L = f_max/(fft_M*dt)*2*np.pi
    nv = np.sqrt(2*PE_energy)
    (nv,EE) = np.meshgrid(nv,EE)
    phi = -nv*EE/(2*omega_L**2)

    Exuv = np.reshape(E_xuv,[1,M])
    Expo = np.reshape(t,[MM,1]).dot(np.reshape(PE_energy+Ip,[1,NN]))

    psi = phi-Expo
    Gate = np.exp(1j*psi)
    #Gate = np.cos(psi)+1j*np.sin(psi)

    result = np.zeros([NN,len(delay)])
    # loop for delay points
    for ii in range(0,len(delay)):
        temp = Exuv.dot(Gate[Ind[ii]:Ind[ii]+M,:])*dt
        result[:,ii] = np.abs(temp)**2
    return result

def Trace_CMA(E_xuv,E_laser,Ind,PE_energy,delay):
    # All parameters has same definition as they are in Trace()

    Ip = 21.56/27.211
    NN = len(PE_energy)
    MM = len(E_laser[0])
    M = len(E_xuv)
    t = E_laser[0]
    dt = t[1]-t[0]

    A_laser = VectorPotential(E_laser[1],dt)

    # calculate phi_t
    A_rev = np.flip(A_laser)
    A_rev = np.reshape(A_rev,[MM,1]).dot(np.ones([1,NN]))
    nv = np.sqrt(2*PE_energy)
    nv = np.ones([MM,1]).dot(np.reshape(nv,[1,NN]))
    phi = nv*A_rev + A_rev**2/2
    phi = np.cumsum(phi,0)*dt
    phi = np.flip(phi,0)

    Exuv = np.reshape(E_xuv,[1,M])
    Expo = np.reshape(t,[MM,1]).dot(np.reshape(PE_energy+Ip,[1,NN]))
    Gate = np.exp(1j*(phi-Expo))

    result = np.zeros([NN,len(delay)])
    # loop for delay points
    for ii in range(0,len(delay)):
        temp = Exuv.dot(Gate[Ind[ii]:Ind[ii]+M,:])*dt
        result[:,ii] = np.abs(temp)**2
    return result

def VectorPotential(Et,dt):
    A = -np.cumsum(Et)*dt
    return A

def ArrShift(arr, shift, fill_value=0,axis=1):
    result = np.empty_like(arr)
    shift = int(shift)
    if shift > 0:
        if arr.ndim==1:
            result[:shift] = fill_value
            result[shift:] = arr[:-shift]
        elif arr.ndim==2:
            if axis==0:
                result[:shift,:] = fill_value
                result[shift:,:] = arr[:-shift,:]
            else:
                result[:,:shift] = fill_value
                result[:,shift:] = arr[:,:-shift]
    elif shift < 0:
        if arr.ndim==1:
            result[shift:] = fill_value
            result[:shift] = arr[-shift:]
        elif arr.ndim==2:
            if axis==0:
                result[shift:,:] = fill_value
                result[:shift,:] = arr[-shift:,:]
            else:
                result[:,shift:] = fill_value
                result[:,:shift] = arr[:,-shift:]
    else:
        result[:] = arr
    return result

def smooth(x,balance=0.2,BgSub=True):
    shapeP = x.shape
    # Background substraction
    if BgSub:
        if x.ndim==1:
            x = x-x[0]
        elif x.ndim==2:
            x = x - np.reshape(x[:,0],[shapeP[0],1]).dot(np.ones([1,shapeP[1]]))
    
    phi = np.unwrap(x)
    N = phi.shape[phi.ndim-1]
    xx = np.linspace(0,N-1,N)
    data = csaps.csaps(xx,phi,xx,smooth=balance)
    return data

def RandPoly(N,xmin=-1,xmax=1, order=3):
    x = np.linspace(xmin,xmax,N)
    coef = np.random.rand(order)
    return(np.polyval(coef,x))