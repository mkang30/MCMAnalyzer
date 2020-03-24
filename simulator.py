from lcg import LCG
import time

'''
This class models the object that runs MCM simulations
and stores the data. I decided to factor out this code in
the form of the class (not just module with methods) to
make the project more extensible: though, the simulation data
is not needed in the particular case (predicting the outcome
of a football leauge).
'''
class Simulator:
    '''
    Constructor
    '''
    def __init__(self, data, trials):
        '''
        data argument should be a dictionary object that
        contains pair of values - event:probability
        '''
        self._trials = trials
        self._data = data
        self._processed = self.simulate()
        self._most = self.calcMost()
        self._least = self.calcLeast()

    '''
    Performs MCM simulation
    '''
    def simulate(self):
        processed = {}
        for k in self._data:
            processed[k]=0
        rg = LCG(int(time.time()),1664525,1013904223,2**32)
        for i in range(self._trials):
            rand = rg.binRand()
            for k in self._data:
                if rand<=self._data[k]:
                    processed[k]+=1
                    break
        return processed

    '''
    Calculates the most frequent output under the simulation
    '''
    def calcMost(self):
        mostN = 0
        result = None
        for k in self._processed:
            if self._processed[k]>mostN:
                mostN = self._processed[k]
                result = k
        return result

    '''
    Calculates the least frequent output under the simulation
    '''
    def calcLeast(self):
        leastN = int
        result = None
        start = False
        for k in self._processed:
            if start==False:
                leastN = self._processed[k]
                result = k
                start = True
            else:
                if self._processed[k]<leastN:
                    leastN = self._processed[k]
                    result = k
        return result
