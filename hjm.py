import numpy as np

def build_forward_rates(sigma, pi, q, f0, T, N, tenor, payoff_func):
    #tenor always in months
    delta_time = 1/N
    tau = tenor/12
    n = tau/delta_time

    
    n = round(n)
    phi = sigma/(np.sqrt(q*(1-q)))
    l_fr = []

    for i in range(1, 1+N*T+n):

        fr = np.zeros((i, i))
        T_barr = i
        fr[0,0] = f0[i-1]

        if i == 1:
            l_fr.append(fr)

        else:
            for j in range(1, i):

                term1 = np.log(1 + pi*( np.exp( -T_barr * phi * (delta_time)**(3/2)) -1 ))
                term2 = np.log(1 + pi*( np.exp( -(T_barr-j) * phi * (delta_time)**(3/2)) -1 ))

                for k in range(j+1):
                    fr[k,j] = fr[0,0] + k*phi*np.sqrt(delta_time) + (term1 - term2)/delta_time
               
            
            l_fr.append(fr)
            

    l = [np.array(l_fr[m][:N*T+1, N*T]) for m in range(N*T, N*T+n)]
    somme = 0
    for elt in l:
        somme += elt

    prices_payoff = list(np.exp(-delta_time*somme))
    prices_payoff.reverse()

    # continuous_comp = [-np.log(price)*12/tenor for price in prices_payoff] #because tenor is ALWAYS in months
    simply_comp = [(1-price)*12/(tenor*price) for price in prices_payoff]

    # print("continuous_comp", continuous_comp)

    #Pn,i(1) matrix
    p1 = np.zeros((N*T, N*T))
    for i in range(N*T):
        l = list(l_fr[i][:i+1, i])
        l.reverse()
        l = np.array(l)
        p1[:i+1, i] = np.exp(-delta_time*l)

    # mat_pricing = np.zeros((N*T+1, N*T+1))
    # mat_pricing[:, -1] = np.array([payoff_func(rate) for rate in continuous_comp])

    mat_pricing_simply = np.zeros((N*T+1, N*T+1))
    mat_pricing_simply[:, -1] = np.array([payoff_func(rate) for rate in simply_comp])

    for k in range(N*T-1, -1, -1):
        for i in range(k+1):
            # mat_pricing[i][k] = ((1-pi)*(mat_pricing[i+1][k+1]) + pi*(mat_pricing[i][k+1]))*p1[i][k]
            mat_pricing_simply[i][k] = ((1-pi)*(mat_pricing_simply[i+1][k+1]) + pi*(mat_pricing_simply[i][k+1]))*p1[i][k]

    #compute current rate
    l = f0[:n] 
    price_current = np.exp(-delta_time*sum(l))
    # current_rate = -np.log(price_current)*12/tenor
    current_rate_simply = (1-price_current)*12/(tenor*price_current)

    # price = mat_pricing[0][0]
    price_simply = mat_pricing_simply[0][0]

    return l_fr, prices_payoff, simply_comp, mat_pricing_simply, current_rate_simply, price_simply

