import numpy as np


def h(pi, delta, t):
    return 1/(pi+(1-pi)*(delta)**t)

def h_et(pi, delta, t):
    return (delta**t)/(pi+(1-pi)*(delta)**t)


def tree(n, i, T0, P, pi, delta, nb_steps):
    
    if T0==0:
        P[n,i,T0]=1
        return P
    
    P[n,i,1]=(P[0,0,n+1]*(delta**(n-i)))/(P[0,0,n]*(pi+(1-pi)*(delta**n))) #calcul de P[n,i,1]
    
    if n<(nb_steps-1):
        if P[n+1,i,T0-1]==0: #le downstate de n+1 n'est pas encore calculé
            
            P[n+1,i,T0-1]=(P[n,i,T0]/P[n,i,1])*h_et(pi,delta,(T0-1))
            P= tree(n+1,i,T0-1,P,pi,delta,nb_steps) #on passe au downstate de l'instant n+1

        if P[n+1,i+1,T0-1]==0: #le upstate de n+1 n'est pas encore calculé
            
            P[n+1,i+1,T0-1]=(P[n,i,T0]/P[n,i,1])*h(pi,delta,(T0-1))
            P= tree(n+1,i+1,T0-1,P,pi,delta,nb_steps) #on passe au Upstate de l'instant n+1
    return P



def Ho_Lee(T, N, tenor, pi, delta, P0):
    delta_time = 1/N
    tau = tenor/12
    n = tau/delta_time 
    n = round(n)
    
    P=np.zeros((N*T+1, N*T+1, N*T+n+1))  
    
    P[0,0]=P0 #P[0 (n=0),0 (i=0)] est donné
    
    for T0 in range(1,N*T+n+1): #on construit tous les prix commençant de la maturité T0 à l'instant 0
        P=tree(0,0,T0,P,pi,delta,N*T+1)
    return P


def p1(n, i, pi, delta, p0):
        return (p0[n+1]*delta**(n-i))/(p0[n]*(pi+(1-pi)*delta**n))

def backward_pricing(f, X, pi, delta, p0):
    size = len(f)
    mat_pricing = np.zeros((size, size))
    mat_pricing[:, -1] = f 

    for n in range(size-2, -1, -1):
        for i in range(n+1):
            mat_pricing[i][n] = (pi*(mat_pricing[i+1][n+1]+X[i+1][n+1]) + (1-pi)*(mat_pricing[i][n+1]+X[i][n+1]))*p1(n,i, pi, delta, p0)

    # mat_pricing = np.round(mat_pricing, 2)
    return mat_pricing


def price_call_option(pi, delta, rate, N, T, tenor, payoff_func):
    
    delta_time = 1/N
    tau = tenor/12
    n = tau/delta_time 
    n = round(n)
    p0 =[np.exp(-rate*(x/N)) for x in range(N*T+n+1)]
    prices = Ho_Lee(T, N, tenor, pi, delta, p0) 
    final_prices = prices[-1, :, n]

    price = p0[n]
    current_rate=(1-price)/(tau*price)
 
    payoffs = [payoff_func((1-price)/(tau*price)) for price in final_prices]
    back_pricing = backward_pricing(payoffs, np.zeros((N*T+1, N*T+1)), pi, delta, p0)
    back_pricing = np.flip(back_pricing, axis=0)

    pricing = np.zeros(())
    m, _ = back_pricing.shape
    pricing = np.zeros((m, m))

    for i in range(m):
        for j in range(i+1):
            pricing[j, i] = back_pricing[m-1-i+j, i]

    # pricing = np.round(pricing, 3)

    return pricing

