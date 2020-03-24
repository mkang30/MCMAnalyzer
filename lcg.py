
'''
This class models a random generator that uses LCG
method.
'''
class LCG:
    '''
    Constructor for this class.
    '''
    def __init__(self, xn, a, c, m):
        #LCG constants
        self.inputCheck(xn)
        self.inputCheck(a)
        self.inputCheck(c)
        self.inputCheck(m)
        self._xn = xn
        self._a = a
        self._c = c
        self._m = m

    '''
    Performs LCG to generate a random number.
    '''
    def lcgcalc(self):
        result = (self._xn*self._a+self._c)%self._m
        self._xn = result
        return result

    '''
    Generates a random number from 0 to 1

    '''
    def binRand(self):
        return float(self.lcgcalc())/float(self._m)


    '''
    invalid input handling
    '''
    def inputCheck(self,e):
        if e == None:
            raise ValueError("The input can't be null!")
        if e<0:
            raise ValueError("The input can't be negative!")
    
