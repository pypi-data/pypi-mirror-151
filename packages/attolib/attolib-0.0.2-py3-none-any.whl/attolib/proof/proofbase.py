import numpy as np 
import logging
from attolib import ArrShift

def OOF(trace,dt,de,omega0,RelTol=1e-2):
    #trace- 2D array, time across columns, energy across rows
    # dt, de, omega0 are in atomic units
    MM,NN = trace.shape
    NF = int(2**(np.ceil(np.log2(NN))))
    # Calculate NF, which is the number of points used to do FFT
    # NF should be large enough to ensure fi is close to f0
    f0 = omega0/(2*np.pi)
    ferror = RelTol*f0
    error = 1
    while(True):
        df = 1/(NF*dt)
        M = np.round(f0/df)
        error = abs(f0-M*df)
        if(error<ferror):
            break
        else:
            NF = NF*2

    M = int(M)
    Y = np.fft.fft(trace,NF)
    alpha_OOF = np.unwrap(np.angle(Y[:,M]))
    gamma_OOF = np.abs(Y[:,M])
    return (alpha_OOF,gamma_OOF)

def AlphaCalc(Ui,phi):
    # Ui and phi are ndarray with dimensions of 1 or 2
    shapeU = Ui.shape
    shapeP = phi.shape
    # make sure Ui and phi have same dimensions
    if Ui.ndim==1 and phi.ndim==2:
        Ui = np.ones([shapeP[0],1]).dot(np.reshape(Ui,[1,shapeU[0]]))
    elif Ui.ndim==2 and phi.ndim==1:
        phi = np.ones([shapeU[0],1]).dot(np.reshape(phi,[1,shapeP[0]]))
    elif (Ui.ndim>2 or Ui.ndim<1) or (phi.ndim>2 or phi.ndim<1):
        logging.error('Ui and phi must be ndarray with dimensions of 1 or 2')
        Alpha = np.empty_like(phi)
        Alpha.fill(np.nan)
        return Alpha
    
    if Ui.size!=phi.size:
        logging.error('Sizes of Ui and phi do not match!')
        Alpha = np.empty_like(phi)
        Alpha.fill(np.nan)
        return Alpha
    
    U_plus = ArrShift(Ui,-1)
    U_minus = ArrShift(Ui,1)

    phi_plus = ArrShift(phi,-1)
    phi_minus = ArrShift(phi,1)
    C = U_minus*np.cos(phi_minus-phi) - U_plus*np.cos(phi-phi_plus)
    D = U_minus*np.sin(phi_minus-phi) - U_plus*np.sin(phi-phi_plus)
    Alpha = np.arctan2(C,D)
    return Alpha

def identify():
    print('PyAtto.PROOF.proofbase')