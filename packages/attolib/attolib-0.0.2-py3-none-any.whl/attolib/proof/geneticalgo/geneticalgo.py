import numpy as np
import scipy.interpolate as sci
import matplotlib.pyplot as plt
import logging
import multiprocessing as mp
import attolib

class Parameters:
    def __init__(self):
        self.population = 2000
        self.survivals = 100
        self.nos = 151
        self.pclone = 0.05
        self.mutate1 = 0.2
        self.mutate2 = 0.2
        self.MutPolyPhase=0.2
        self.cross1 = 0.2
        self.cross2 = 0.2
        self.rotate = 0.1
        self.InitMethod = 'polynome'

# GAProcess is used to generate several parallel processes
class ParallelProcess():
    def __init__(self,target,args,N=1,names=[]):
        #args=(U,alpha_0,GAParameters)
        self.N = N
        self.U = args[0]
        self.alpha0 = args[1]
        self.GAParameters = args[2]
        self.procs = []
        self.pipes = []
        self.SharedArrays = []
        self.populations = []
        # process names
        Nname = len(names)
        add_names=[]
        if Nname<N:
            nums = range(Nname+1,N+1)
            add_names = ['Process#'+str(ii) for ii in nums]
        self.names = names + add_names
        # initialize
        for ii in range(N):
            self.SharedArrays.append(mp.Array('d',self.GAParameters.survivals*self.GAParameters.nos))
            #arr = np.frombuffer(self.SharedArrays[ii].get_obj(),c.c_double)  # population and arr share the same memory
            self.populations.append(np.ndarray((self.GAParameters.survivals,self.GAParameters.nos),dtype=np.float64,buffer=self.SharedArrays[ii].get_obj()))  # popu and arr share the same memory
            Alice,Bob = mp.Pipe()
            self.pipes.append({'Alice':Alice,'Bob':Bob})
            self.procs.append(mp.Process(target=target,args=(self.SharedArrays[ii],self.pipes[ii]['Bob'],self.U,self.alpha0,self.GAParameters)))
    
    def start_all(self):
        for p in self.procs:
            p.start()
    
    def start_p(self,i=0):
        self.procs[i].start()
    
    def stop_all(self):
        for p in self.procs:
            p.kill()
            p.terminate()
    
    def stop_p(self,i=0):
        self.procs[i].kill()
        self.procs[i].terminate()

# GAWorld is the function that is executed in parallel processes
def GAWork(population,Bob,U,alpha_0,GAParameters):
    #arr = np.frombuffer(population.get_obj(),c.c_double)  # population and arr share the same memory
    popu = np.ndarray((GAParameters.survivals,GAParameters.nos),dtype=np.float64,buffer=population.get_obj())  # popu and arr share the same memory

    Survivals = PhaseInitial(GAParameters.population,GAParameters.nos,mode=GAParameters.InitMethod,order=12)
    N = 100000

    for ii in range(1,N):
        if ii%1000==0:
            np.copyto(popu,Survivals)
            Bob.send(1)
            flag = Bob.recv()
            # flag==10 indicates that main process has put its population in popu (shared array), which should be added to the current population
            if flag==10:
                Survivals = np.vstack((Survivals,popu))
            # flag==0 indicates that main process did not return anything, the current population should be re-initialized
            if flag==0:
                Survivals = PhaseInitial(GAParameters.population,GAParameters.nos,mode=GAParameters.InitMethod,order=12)
            #print(f'Merge from {name}')
        Survivals,err,alpha_i,BestPhase = EvoOneGen(Survivals,U,alpha_0,GAParameters)

def PhaseInitial(Npopu,Npara,mode='random',order=3):
    mode = mode.lower()
    if mode=='random':
        InitPhase = np.random.rand(Npopu,Npara)
        InitPhase == InitPhase * 2 * np.pi
    elif mode == 'polynome':
        InitPhase = np.zeros((Npopu,Npara))
        x = np.linspace(0,Npara-1,Npara)-Npara/2.0
        for ii in range(0,Npopu):
            ActOrder = int(np.round(np.random.random()*order))
            coef = np.random.rand(ActOrder)*2*np.pi-np.pi
            expon = np.linspace(ActOrder-1,0,ActOrder)
            coef = coef/(10**(expon))
            coef[-2:] = 0                              # the 0-th and 1st order are meaningless
            InitPhase[ii,:] = np.polyval(coef,x)
    else:
        #logging.error(f'Invalid mode {mode:%s}' )
        InitPhase = np.zeros((Npopu,Npara))

    return InitPhase

def ErrorEval(alpha_i,alpha_0,Ui):
    # alpha_i is 1d or 2d arrays
    shapeA = alpha_i.shape
    if alpha_i.ndim==2:
        if alpha_0.ndim==1:
            alpha_0 = np.ones([shapeA[0],1]).dot(np.reshape(alpha_0,[1,len(alpha_0)]))
        if Ui.ndim==1:
            Ui = np.ones([shapeA[0],1]).dot(np.reshape(Ui,[1,len(Ui)]))

    errors = Ui*(alpha_i-alpha_0)**2
    return np.sum(errors,alpha_i.ndim-1)

def Roulette(fitness,excludes=[]):
    N = len(fitness)
    prop = np.cumsum(fitness)
    MaxVal = prop[-1]
    pick = -1
    ii = 0
    while ((pick in excludes) or pick<0):
        r = np.random.rand()*MaxVal
        pick = np.where(prop>=r)[0][0]
        ii = ii + 1
        if (ii>1e5):
            logging.warn('Maximum attemps reached!')
            break
    return pick

def Select(fitness,population,N,pclone):
    MM,NN = population.shape
    NewPopulation = np.zeros([N,NN])
    Nmate = int(np.floor((N-N*pclone)/2))
    Nclone = int(N - Nmate*2)
    SortInd = np.flip(np.argsort(fitness))
    # cloned population
    NewPopulation[0:Nclone,:] = population[SortInd[0:Nclone]]
    # reproduced population
    for ii in range(0,Nmate):
        jj = 2*ii+Nclone
        # find parents first
        MotherInd = Roulette(fitness)
        FatherInd = Roulette(fitness,[MotherInd])
        Mother = population[MotherInd]
        Father = population[FatherInd]
        pos = int(np.random.rand()*(NN-2))+1
        NewPopulation[jj,:] = np.append(Mother[0:pos],Father[pos:])
        NewPopulation[jj+1,:] = np.append(Father[0:pos],Mother[pos:])
    return NewPopulation

def Mutate(population,pMut,points='single'):
    MM,NN = population.shape
    for ii in range(1,MM):
        if(np.random.rand()<=pMut):
            pos = int(np.random.rand()*NN)
            if points=='single':
                population[ii][pos] = population[ii][pos]+(np.random.rand()-0.5)*0.2*np.pi
            elif points=='multiple':
                L = int(np.random.rand()*(NN-pos))+1
                population[ii][pos:pos+L] = population[ii][pos:pos+L] + (np.random.rand(L)-0.5)*0.2*np.pi
    return

def Cross(population,pMut,points='single'):
    MM,NN = population.shape
    fitness = np.ones(MM)
    for ii in range(1,MM):
        if(np.random.rand()<=pMut):
            jj = Roulette(fitness,[0,ii])
            pos = int(np.random.rand()*NN)
            if points=='single':
                temp = population[ii][pos].copy()
                population[ii][pos] = population[jj][pos].copy()
                population[jj][pos] = temp
            elif points == 'multiple':
                L = int(np.random.rand()*(NN-pos))+1
                temp = population[ii][pos:pos+L].copy()
                population[ii][pos:pos+L] = population[jj][pos:pos+L].copy()
                population[jj][pos:pos+L] = temp
    return

def MutatePolyPhase(population,pMut):
    MM,NN = population.shape
    for ii in range(1,MM):
        if(np.random.rand()<=pMut):
             population[ii,:] = population[ii,:] + PhaseInitial(1,NN,mode='polynome',order=12)[0]

def Rotate(population,pMut):
    MM,NN = population.shape
    for ii in range(1,MM):
        if(np.random.rand()<=pMut):
            shift = int(np.random.rand()*NN)
            population[ii,:] = np.roll(population[ii,:],shift)

def EvoOneGen(OldPopulation,Ui,alpha_0,GAParas):
    SmoothPopu = attolib.smooth(OldPopulation,balance=0.2,BgSub=True)
    alpha_i = attolib.proof.AlphaCalc(Ui,SmoothPopu)
    errors = ErrorEval(alpha_i,alpha_0,Ui)
    IndBest = np.argmin(errors)
    fitness = 1/errors
    fitness = fitness / np.max(fitness)
    # Evolution
    population = Select(fitness,OldPopulation,GAParas.survivals,GAParas.pclone)
    Mutate(population,GAParas.mutate1,points='single')
    Mutate(population,GAParas.mutate2,points='multiple')
    MutatePolyPhase(population,GAParas.MutPolyPhase)
    Cross(population,GAParas.cross1,points='single')
    Cross(population,GAParas.cross2,points='multiple')
    Rotate(population,GAParas.rotate)
    return (population,errors[IndBest],alpha_i[IndBest,:],SmoothPopu[IndBest,:])

