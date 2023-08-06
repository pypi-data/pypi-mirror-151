import numpy as np
from attolib import ArrShift
import scipy.optimize

def derivative(delta,U,alpha):
    U_minus = ArrShift(U,1)
    U_minus2 = ArrShift(U,2)
    U_plus = ArrShift(U,-1)
    delta_plus = ArrShift(delta,-1)
    alpha_minus = ArrShift(alpha,1)

    R = np.sqrt(U_minus**2+U_plus**2-2*U_minus*U_plus*np.cos(delta_plus-delta))
    R += 1e-10
    R_minus = ArrShift(R,1,fill_value=1e-10)

    a = U_minus**2*U_plus/(R**3)*np.sin(delta_plus-delta)*np.sin(delta+alpha)
    b = U_minus*U_plus**2/(R**3)*np.sin(delta_plus-delta)*np.sin(delta_plus+alpha)
    a_minus = ArrShift(a,1)
    b_minus = ArrShift(b,1)
    dervs = U_minus*(a_minus-b_minus+U/R_minus*np.cos(delta+alpha_minus))
    dervs += U*(-a+b-U_minus/R*np.cos(delta+alpha))
    return dervs

def ErrorEval(delta,U,alpha):
    U_minus = ArrShift(U,1)
    U_plus = ArrShift(U,-1)
    delta_plus = ArrShift(delta,-1)

    R = np.sqrt(U_minus**2+U_plus**2-2*U_minus*U_plus*np.cos(delta_plus-delta))

    R+=1e-100
    terms = 1-U_minus/R*np.sin(delta+alpha)+U_plus/R*np.sin(delta_plus+alpha)
    terms = U*terms
    #terms = terms/R**2
    return np.sum(terms)

def TermsErrorEval(delta,U,alpha):
    U_minus = ArrShift(U,1)
    U_plus = ArrShift(U,-1)
    delta_plus = ArrShift(delta,-1)

    R = np.sqrt(U_minus**2+U_plus**2-2*U_minus*U_plus*np.cos(delta_plus-delta))

    #terms = U_minus*np.sin(delta+alpha)-U_plus*np.sin(delta_plus+alpha)-R
    #terms = U*(terms*terms)
    #Ind = np.where(abs(R)<1e-50)
    #R[Ind] = 1e-50
    R+=1e-100
    terms = 1-U_minus/R*np.sin(delta+alpha)+U_plus/R*np.sin(delta_plus+alpha)
    terms = U*terms
    return terms

def termC(U,delta):
    U_minus = ArrShift(U,1)
    U_plus = ArrShift(U,-1)
    delta_plus = ArrShift(delta,-1)

    return U_minus*np.cos(delta) - U_plus*np.cos(delta_plus)

def termD(U,delta):
    U_minus = ArrShift(U,1)
    U_plus = ArrShift(U,-1)
    delta_plus = ArrShift(delta,-1)

    return U_minus*np.sin(delta) - U_plus*np.sin(delta_plus)

def termR(U,delta):
    U_minus = ArrShift(U,1)
    U_plus = ArrShift(U,-1)
    delta_plus = ArrShift(delta,-1)

    return np.sqrt(U_minus**2+U_plus**2-2*U_minus*U_plus*np.cos(delta_plus-delta))

def OneIter(delta,U,alpha,hstep=0.1):
    dervs = derivative(delta,U,alpha)
    delta += dervs*hstep
    return delta

def AnalySolution(U,alpha,delta=[],index=[]):
    N = len(U)
    U_minus = ArrShift(U,1)
    U_plus = ArrShift(U,-1)
    if len(delta)!=N:
        delta = alpha*0
    if len(index)==0:
        index = list(range(0,N-1))
    for ii in index:
        #print(U_plus.shape,U_minus.shape,alpha.shape,delta.shape)
        if U_plus[ii]>=U_minus[ii]:
            theta = np.arccos(np.cos(delta[ii]+alpha[ii])*U_minus[ii]/U_plus[ii])
            s = -alpha[ii] + theta
            if np.sin(s)<0:
                delta[ii+1] = s
            else:
                delta[ii+1] = -alpha[ii]-theta
        elif U_plus[ii]>=abs(U_minus[ii]*np.cos(delta[ii]+alpha[ii])) and np.sin(delta[ii]+alpha[ii])>=0:
            theta = np.arccos(np.cos(delta[ii]+alpha[ii])*U_minus[ii]/U_plus[ii])
            s = -alpha[ii] + np.array([theta,-theta])
            if abs(s[0]-delta[ii])<=abs(s[1]-delta[ii]):
                delta[ii+1] = s[0]
            else:
                delta[ii+1] = s[1]
        else:
            #cprint(f'no solution!@{ii}')
            res = scipy.optimize.minimize(fmin1d,-np.pi/2-alpha[ii],args=(U_plus[ii],U_minus[ii],delta[ii],alpha[ii]),tol=0.0001,method='BFGS')
            delta[ii+1] = res.x
            #print(f'{ii}:{res.fun}')
            #delta[ii+1] = np.random.rand()*0.1
    return delta

def fmin1d(x,U_plus,U_minus,delta,alpha):
    R = np.sqrt(U_minus**2+U_plus**2-2*U_minus*U_plus*np.cos(x-delta))
    return (U_plus*np.sin(x+alpha) - U_minus*np.sin(delta+alpha))/R

def delta2phi(delta):
    phi = np.cumsum(delta)
    phi = phi-phi[0]
    phi = np.unwrap(phi)
    phi = -phi
    return phi
