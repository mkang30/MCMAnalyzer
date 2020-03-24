from analyzer import Analyzer

'''
Gets the input of the league value
'''
def getLeague():
    while True:
        print("Type 1 for the La Liga")
        print("Type 2 for the EPL")
        print("Type 3 for the Bundesliga")
        inp = str(input())
        if inp == "1":
            return "SP1"
        elif inp == "2":
            return "E0"
        elif inp == "3":
            return "D1"
        else:
            print("Wrong input!")

'''
Returns the size of the league
'''
def getSize(league):
    if league == "SP1" or league == "E0":
        return 20
    return 18

'''
Gets the input of the season value
'''
def getSeason():
    while True:
        print("Type the last 2 digits of the season year from 10 to 17")
        inp = str(input())
        try:
            inp = int(inp)
            if inp<10 or inp>17:
                print("Wrong input!")
            else:
                return inp
        except ValueError:
            print("Wrong input!")
while True:
    league = getLeague()
    size = getSize(league)
    season = getSeason()
    season = str(season)+str(season+1)
    url = "http://www.football-data.co.uk/mmz4281/"+season+"/"+league+".csv"
    anal = Analyzer(size, url)
    title = "Standing                 Team                    Points"
    sep = int(len(title)/2.2)
    print(title)
    stand = 1
    for line in anal._outcome:
        first = sep - len(str(stand))
        second = sep - len(line[0])
        print(str(stand)+" "*first+line[0]+" "*second+str(line[1]))
        stand+=1
