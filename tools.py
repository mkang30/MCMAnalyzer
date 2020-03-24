import math

#This module contains helper method
#needed in the project


'''
Calculates number of permutations with given n and r
'''
def totalPermut(n,r):
    nrfact = 1
    nfact = 1
    for i in range(1,(n-r)+1):
        nrfact *= i
    for i in range(1, n+1):
        nfact *= i
    return int(nfact/nrfact)

'''
Calculates the probability of the event under the
Posisson distribution
'''
def poisson(m, x):
    return math.exp(-m)*(m**x)/math.factorial(x)


        
    
