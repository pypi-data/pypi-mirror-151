import math
import numpy as np
import scipy.integrate as si

class Gas:
    def __init__(self, name="He"):
        name = name.lower()
        self.name = name
        if name == "he":
            self.Ip = 24.587/27.212
            self.Z = 1
            self.l = 0
            self.m = 0
        elif name == "ne":
            self.Ip = 21.564/27.212
            self.Z = 1
            self.l = 1
            self.m = 0
        elif name == "ar":
            self.Ip = 15.759/27.212
            self.Z = 1
            self.l = 1
            self.m = 0
        elif name == "kr":
            self.Ip = 13.999/27.212
            self.Z = 1
            self.l = 1
            self.m = 0
        elif name == "xe":
            self.Ip = 12.130/27.212
            self.Z = 1
            self.l = 1
            self.m = 0
        elif name == "h":
            self.Ip = 13.606/27.212
            self.Z = 1
            self.l = 0
            self.m = 0
        else:
            print("Undefined gas: ", name ,"! Helium parameters were used!")
            self.Ip = 24.587/27.212
            self.Z = 1
            self.l = 0
            self.m = 0 

        
    def Display(self):
            print('The ionization potential of %s is %1.3f.' %(self.name,self.Ip))


def ADK_AU(F_E,gas):
    Ip = gas.Ip
    Z = gas.Z
    l = gas.l
    m = gas.m

    F_E = abs(F_E)

    n_star = Z / math.sqrt(2*Ip)
    l_star = n_star - 1

    F0 = (2*Ip)**(3/2)
    Cnl = 2**(2*n_star)/(n_star*math.gamma(n_star+l_star + 1)*math.gamma(n_star-l_star))
    Glm = (2*l+1)*math.factorial(l+abs(m))/(2**abs(m)*math.factorial(abs(m))*math.factorial(l-abs(m)))

    rate_t = Cnl*Glm*Ip*(2*F0/F_E)**(2*n_star-abs(m)-1)*np.exp(-2*F0/(3*F_E))

    return rate_t

def wm(x,m=0):
    m = abs(m)
    fun = lambda t: math.exp(-x**2*t)*(t**m)/math.sqrt(1-t)
    Integ= si.quad(fun,0,1)
    coef = (x**(2*m+1))/2
    Integ = Integ[0]*coef
    return Integ
    
def PPT_AU(F_E,omega0,I0,gas):
    Ip = gas.Ip
    Z = gas.Z
    l = gas.l
    m = gas.m

    F_E = abs(F_E)
    F_peak = math.sqrt(I0)

    n_star = Z / math.sqrt(2*Ip)
    l_star = n_star - 1

    F0 = (2*Ip)**(3/2)
    Cnl = 2**(2*n_star)/(n_star*math.gamma(n_star+l_star + 1)*math.gamma(n_star-l_star))
    Glm = (2*l+1)*math.factorial(l+abs(m))/(2**abs(m)*math.factorial(abs(m))*math.factorial(l-abs(m)))
    
    Keldysh = math.sqrt(2*Ip)*omega0/F_peak
    #print('F0:{0},Cnl:{1},Glm:{2}'.format(F0,Cnl,Glm))
    Up = F_peak**2/4/(omega0**2)
    nv = (Ip+Up)/omega0
    q_min = np.ceil(nv)
    q_min = q_min.astype(int)
    g = 3/2/Keldysh*((1+1/2/Keldysh**2)*math.asinh(Keldysh)-math.sqrt(1+Keldysh**2)/2/Keldysh)
    beta = 2*Keldysh/math.sqrt(1+Keldysh**2)
    alpha = 2*math.asinh(Keldysh)-beta
    q_max = np.ceil(10/alpha)+q_min
    q_max = q_max.astype(int)
    #print('q_min:{0},q_max:{1}'.format(q_min,q_max))

    A = 0
    for jj in range(q_min,q_max):
        xx = jj-nv
        A = A + math.exp(-alpha*xx)*wm(math.sqrt(beta*xx),m)
 
    W = Cnl*Glm*Ip*(2*F0/F_E)**(2*n_star-abs(m)-1)*(np.sqrt(1+Keldysh**2)**(abs(m)+1))
    W = W*4/np.sqrt(3*math.pi)/math.factorial(abs(m))*Keldysh**2/(1+Keldysh**2)
    W = W*np.exp(-2*F0/(3*F_E)*g)*A
    #W = W * np.sqrt(3*F_E/math.pi/F0)

    return W