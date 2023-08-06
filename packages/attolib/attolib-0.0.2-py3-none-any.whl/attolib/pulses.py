import numpy as np
from scipy.interpolate import interp1d
import  logging

def sech(x):
    return (1/np.cosh(x))

def spec2ef(freq,Intensity,**args):
    if 'phase' not in args.keys():
        args['phase'] = freq*0
    if 'N' not in args.keys():
        args['N'] = len(freq)
    if 'T' not in args.keys():
        args['T'] = -1
    if 'unit' not in args.keys():
        args['unit'] = 'nm'
    if 'norm' not in args.keys():
        args['norm'] = 'off'
    if 'tzero' not in args.keys():
        args['tzero'] = 'off'

    args['unit'] = args['unit'].lower()
    if args['unit'] == 'phz':
        f = freq
    elif args['unit'] == 'nm':
        f = 300/freq
    elif args['unit'] == 'ev':
        f = freq * 1.6 /6.62607015          # 1/fs
    else:
        f = freq
    
    y_abs = np.sqrt(Intensity)
    y_angle = args['phase']

    if args['T']<0:
        f0 =np.sum(f*Intensity)/np.sum(Intensity)
        args['T'] = args['N']/(f0*20)
    
    deltat = args['T']/args['N']

    ff = np.linspace(0,args['N']-1,args['N'])/args['T']
    t = np.linspace(0,args['N']-1,args['N'])*deltat
    f_r = interp1d(f,y_abs,bounds_error=False,kind = 'linear',fill_value=0)
    f_a = interp1d(f,y_angle,bounds_error=False,kind = 'linear',fill_value=0)
    yy = f_r(ff)*np.exp(1j*f_a(ff))
    E = np.fft.ifft(yy)

    # normalize
    if args['norm']=='on':
        E = E/np.max(abs(E))
    # center at zero
    if args['tzero']=='on':
        Ind = np.argmax(abs(E))
        Indc = np.ceil(args['N']/2).astype(int)
        dis = Indc - Ind
        dis = dis.astype(int)
        E = np.roll(E,dis)
        t = t-t[Indc]
    
    # convert to attosecond
    t = t*1000
    return (t,E)
   
def ShiftPhase(freq,phase,f0=None):
    # freq has to be frequency with units of fs^-1 or eV et.al.
    if f0 is None:
        f0 = np.sum(freq*phase)/np.sum(phase)
    N = len(freq)
    phase = np.unwrap(phase)
    Ind = np.where(freq>=f0)[0][0]
    Ind = max(0,Ind)
    Ind = min(Ind,N-1)
    slope1 = (phase[Ind+1]-phase[Ind])/(freq[Ind+1]-freq[Ind])
    slope2 = (phase[Ind-1]-phase[Ind])/(freq[Ind-1]-freq[Ind])
    slope = (slope1+slope2)/2
    phase = phase - phase[Ind] - slope*(freq-freq[Ind])
    phase = np.unwrap(phase)
    phase = phase - phase[Ind]
    return phase

def envelope(tt,tau,Amp=1,t0=0,type='Gaussian'):
    type = type.lower()
    if type=='gaussian':
        Env = np.sqrt(Amp)*np.exp(-2*np.log(2)*((tt-t0)/tau)**2)
    elif type=='cos2':
        a = 2*np.arccos(1/np.sqrt(2))
        x1 = np.pi/2/a*tau+t0
        x0 = -np.pi/2/a*tau+t0
        x0,x1=(min(x0,x1),max(x0,x1))
        Env = ((tt>=x0) & (tt<=x1))* np.cos((tt-t0)/tau*a)*np.sqrt(Amp)
    elif type=='sech2':
        Env = np.sqrt(Amp)*sech(2*np.log(1+np.sqrt(2))*(tt-t0)/tau)
    elif type=='rect':
        Env = np.sqrt(Amp)*((tt>=(-tau/2+t0)) & (tt<=(tau/2+t0)))
    elif type=='exp':
        Env = np.sqrt(Amp)*np.exp(-1/2*np.log(2)*((tt-t0)/tau)) * (tt>=t0)
    elif type=='symexp':
        Env = np.sqrt(Amp)*np.exp(-np.log(2)*(np.abs(tt-t0)/tau))
    else:
        logging.error(f'undefined envelop type: {type}!')
        Env = tt*0
    return Env

def GaussianPulse(tau,omega0,E0,tt,cep=0,value='real'):
    if value=='real':
        E=E0*np.exp(-2*np.log(2)*(tt/tau)**2)*np.cos(omega0*tt+cep)
    else:
        E=E0*np.exp(-2*np.log(2)*(tt/tau)**2)*np.exp(1j*(omega0*tt+cep))
    return E

def VectorPotential(Et,dt): 
    A = -np.cumsum(Et)*dt
    return A

def MultiGaussianCurve(xx,pos,Amps=[1],width=[1]):
    y = xx*0
    Ma = len(Amps)
    Mw = len(width)
    for ii,x0 in enumerate(pos):
        ia = ii%Ma
        iw = ii%Mw
        y += Amps[ia]*np.exp(-4*np.log(2)*((xx-x0)/width[iw])**2)
    return y

def RandSpec(N=10000):
    pos = np.array([740.5,847.2,719.2,820.9,748.1,722.3,826.7,825.4])
    Amps = np.array([0.2673,0.06955,-0.4141,0.09422,0.3871,0.365,6.078,-5.876])
    width = np.array([10.11,7.03,48.28,8.26,94.98,83.63,23,22.95])*np.sqrt(4*np.log(2))
    xx = np.linspace(400,1000,N)
    N = len(Amps)
    yy = MultiGaussianCurve(xx,pos,Amps,width)
    yy = yy/np.max(yy)
    return(xx,yy)