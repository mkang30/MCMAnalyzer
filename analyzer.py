import csv
import urllib.request
import codecs
from simulator import Simulator
from tools import totalPermut
from tools import poisson
from itertools import permutations


'''
This calss models an analyzer that analyzes
data and generates the prediction of the outcome
of the given football league.
'''



class Analyzer:
    '''
    Macro
    '''
    #home team
    HT = 2
    #away team
    AT = 3
    #home team goals
    HTG = 4
    #away team goals
    ATG = 5
    #attacking power home
    APH = 0
    #attacking power away
    APA = 1
    #defensive power home
    DPH = 2
    #defensive power 
    DPA = 3
    
    '''
    Constructor
    '''
    def __init__(self, size, url):
        self._size = size
        self._trials = 5000
        #Reading the csv file from the given url
        self._totalGames = totalPermut(size,2)
        self._data = self.readCSV(url)
        #all the teams
        self._teams = self.findTeams()
        #average goals scored by a home team/ conceded by an away team
        self._avgGH = self.calcAvgGH()
        #average goals scored by an away team/ conceded by an home team
        self._avgGA = self.calcAvgGA()
        #power indexes of all teams
        self._powerIndex = self.calcPI()
        #outcome
        self._outcome = self.mcmAnalyze()
    '''
    Reads the csv data and stores in the list
    '''
    def readCSV(self, url):
        result = []
        stream = urllib.request.urlopen(url)
        data = csv.reader(codecs.iterdecode(stream, 'utf-8'))
        first = True
        for d in data:
            if first == True:
                first = False
            else:
                piece = [d[self.HT],d[self.AT],d[self.HTG],d[self.ATG]]
                result.append(piece)
        self.HT = 0
        self.AT = 1
        self.HTG = 2
        self.ATG = 3
        return result
        
    '''
    Finds all teams participating in the league
    '''
    def findTeams(self):
        teams = []
        i = 0
        for k in self._data:
            if k[self.HT] not in teams:
                teams.append(k[self.HT])
                i += 1
            if i==self._size:
                break
        return teams
                

    '''
    Calculates the average scored by a home team
    '''
    def calcAvgGH(self):
        cum = 0.0
        for d in self._data:
            cum = cum + float(d[self.HTG])
        return cum/self._totalGames

    '''
    Calculates the average scored by an away team team
    '''
    def calcAvgGA(self):
        cum = 0.0
        for d in self._data:
            cum = cum + float(d[self.ATG])
        return cum/self._totalGames


    '''
    Calculates the power indexes for all teams
    Output: dictionary(str:list(int)) where str is a team name and
    list(int) holds APH, APA, DPH, DPA indices
    '''
    def calcPI(self):
        table = {}
        total = (self._size-1)
        for k in self._teams:
            table[k] = [0.0]*4
        for line in self._data:
            table[line[self.HT]][self.APH]+=int(line[self.HTG])
            table[line[self.AT]][self.APA]+=int(line[self.ATG])
            table[line[self.HT]][self.DPH]+=int(line[self.ATG])
            table[line[self.AT]][self.DPA]+=int(line[self.HTG])
        for k in table:
            table[k][self.APH] = table[k][self.APH]/self._avgGH/total
            table[k][self.APA] = table[k][self.APA]/self._avgGA/total
            table[k][self.DPH] = table[k][self.DPH]/self._avgGA/total
            table[k][self.DPA] = table[k][self.DPA]/self._avgGH/total
        return table

    '''
    Calculates the average points earned by teams in the simulation
    
    '''
    def assignPoints(self,data, trials):
        total1 = 0.0
        total2 = 0.0
        for d in data:
            if d=="tone":
                total1 += data[d]*3
            elif d=="draw":
                total1 += data[d]
                total2 += data[d]
            else:
                total2 += data[d]*3
        return [total1/trials,total2/trials]

    '''
    This performs the analyzes based on the expected goal model using
    the Poisson Ditribution and MCM.
    Outpup: dictoinary(str: list(int)) where str is a team name and
    list(int) holds the predicted final standing and total points
    '''
    def mcmAnalyze(self):
        '''
        My method assumes that the teams can only score up to 7 goals, because
        the probability of scoring more than 7 goals is very low, so I am getting
        rid of unnecessary hustles
        '''
        final = {}
        for t in self._teams:
            final[t]=0
        for perm in permutations(self._teams,2):
            prob = {"tone":0.0,"draw":0.0,"ttwo":0.0}
            #expected goals scored by a home team
            expgh = self._powerIndex[perm[0]][self.APH]*self._powerIndex[perm[1]][self.DPA]/self._avgGH
            #expected goals scored by an away team
            expga = self._powerIndex[perm[1]][self.APA]*self._powerIndex[perm[0]][self.DPH]/self._avgGA
            for i in range(8):
                for j in range(8):
                    pr = poisson(expgh,i)*poisson(expga,j)
                    if(i>j):
                        prob["tone"]+=pr
                    elif(i==j):
                        prob["draw"]+=pr
                    else:
                        prob["ttwo"]+=pr
            prob["draw"]= prob["draw"]+prob["tone"]
            prob["ttwo"]= 1
            sim = Simulator(prob, self._trials)
            points = self.assignPoints(sim._processed,self._trials)
            final[perm[0]]+=points[0]
            final[perm[1]]+=points[1]
        for e in final:
            final[e]=round(final[e],2)
        return sorted(final.items(), key=lambda x:x[1], reverse=True)
