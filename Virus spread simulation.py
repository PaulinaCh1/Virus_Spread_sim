import numpy as np
import matplotlib.pyplot as plt
import math as ma
import statistics as stats
from statistics import NormalDist as nd
from statistics import mean

# Different variables that will change how the simulation will act:

# Vaccine effecacy
vE=0.4
# Infectivity factor
R=20
# Mortality factor 
Xm=1.5
# Policy
flightBan = False
mobilityBan = True
testAndQuarantine = False
qLegnth = 2
vaccination = False

class people():
    def __init__(self, vaccinated , infected , quarantined , age, daysInfected=0,daysQuarantined=0):
        self.vaccinated =vaccinated
        self.infected = infected 
        self.quarantined = quarantined
        self.age = age
        self.daysQuarantined=daysQuarantined
        self.daysInfected=daysInfected
    #Set mobility for each person depending on age
    def mobility(self):
        if mobilityBan == False:
            mobility=nd(30, 10).pdf(self.age)
        else:
            mobility=0
        return mobility

# Inputs needed for countries (int-N,int-Population of country,Str-Name of country) *N is the square root of the number of regions
class country ():
    def __init__(self,N,population,name,deaths=0,infections=0):
        self.name=name
        self.N=N
        self.population=population
        self.deaths=deaths
        self.infections=infections
        #Create a NxN array to represent regions
        regions = np.full([N,N],None,dtype=object)
        for x in range(0, N):
            for y in range(0, N):
                regions[x,y]=[]
# Populate the regions with a population equal to that set by the class initiation
        popLeft = population
        while popLeft>0:
# If vaccination is true then 100% of the population is vccinated and if false then 50% is vaccinated
            vac=False
            if vaccination ==True:
                vac = True
            else:
                if 0.5>np.random.rand():
                    vac =True
# Generate a number between 1-20,21-60 and 61-100 to represent the different age groups then use a function based on probability to choose the age group of that person
            young=np.random.randint(1,20)
            middleAged=np.random.randint(21,60)
            old=np.random.randint(61,100)
            regions[np.random.randint(0,N),np.random.randint(0,N)].append(people(vac,False,False,np.random.choice([young,middleAged,old],p=[0.2,0.6,0.2])))
            popLeft=popLeft-1
# Add 10 infected people to each country
        infLeft = 10
        while infLeft>0:
            randX=np.random.randint(0,N)
            randY=np.random.randint(0,N)
            if regions[randX,randY][np.random.randint(0,len(regions[randX,randY]))].infected==False:
                regions[randX,randY][np.random.randint(0,len(regions[randX,randY]))].infected=True
                infLeft=infLeft-1
        self.regions=regions
# Add each country made to a list of countries that makes it easier to iterate through later
        countries.append(self)

                 
#Deaths every 10 days in troughout all simulations    
walesDeaths=[]
ukDeaths=[]
chinaDeaths=[]
polandDeaths=[]

#Infections every 10 days in troughout all simulations    
walesInf=[]
ukInf=[]
chinaInf=[]
polandInf=[]

#Counter is used as a tool to find bugs in the code
#counter=0
#To create and compare each of the four simulations with the same starting variables it loops four time
simCount=0
while simCount<4:
    simCount+=1
    daysPassed=0
    countries=[]
    Wales = country(4,200,"Wales")
    Uk = country(4,200,"Uk")
    China = country(4,200,"China")
    Poland = country(4,200,"Poland")
#Create lists to capture deaths troughout 10 days 
    wDeaths=[]
    uDeaths=[]
    cDeaths=[]
    pDeaths=[]
    wInf=[]
    uInf=[]
    cInf=[]
    pInf=[]
#Loop that simulates the 360 days in a year
    while daysPassed<=360:
        daysPassed += 1
#Number of infected people in each region in an array to then manage infection and capture initial state in txt file
        for i in countries:
            infectedArray = np.zeros([i.N,i.N],int)
            peopleArray = np.zeros([i.N,i.N],int)
            peopleCounter=0
            infPeopleCounter=0
            for x in range(0,i.N):
                for y in range(0,i.N):        
                    for person in i.regions[x,y]:
                        peopleCounter+=1
                        peopleArray[x,y] +=1
                        if (person.infected==True and person.quarantined ==False and person.daysInfected<=3):
                            infPeopleCounter+=1
                            infectedArray[x,y] +=1
#Ensuring that a person quarantined still counts to the infected
                        elif(person.infected==True and person.quarantined ==True):
                            infPeopleCounter+=1
                        elif(person.infected==True and person.quarantined ==False and person.daysInfected>3):
                            person.quarantined=True
#creating the and appending txt file for the country
            if daysPassed%10==0 or daysPassed==1:    
                fileName=(i.name+" "+"{:05d}".format(daysPassed)+".txt")
                countryTxt= open(fileName,"a+")
                countryTxt.write("\n")
                countryTxt.write("Population - "+str(peopleCounter)+" Infected - "+str(infPeopleCounter))
                countryTxt.close()
                #print (fileName)
                #with open(fileName) as f:
                    #lines = f.readlines()
                    #print (lines)

#Movement for people in airport regions    
        for i in countries:
            removalList=[]
            personIndex=-1
            for person in i.regions[0,0]:
                if (person.mobility())>np.random.rand() and (person.quarantined==False) and flightBan==False:
                    newCountry=np.random.randint(0,len(countries))
                    countries[newCountry].regions[0,0].append(person)
                    personIndex+1
                    i.regions[0,0].pop(i.regions[0,0].index(person))

        for i in countries:
#Decide what actions people do every day
            for x in range(0,i.N):
                for y in range(0,i.N):
                    removalList=[]
                    personIndex= (-1)
                    for person in i.regions[x,y]:
                        if person.quarantined==True:
                            person.daysQuarantined+=1
                        if person.daysQuarantined>qLegnth:
                            person.quarantined=False
                        personIndex+=1
                        if (person.infected==True):#Person is infected
                            person.daysInfected+=1
                            dayAction=np.random.randint(1,3)

                            if (dayAction==0):#moving
                                if (person.mobility())>np.random.rand() and (person.quarantined==False):
                                    if (np.random.randint(0,1)==0):
                                        changeX=-1
                                    else:
                                        changeX=1
                                    if (np.random.randint(0,1)==0):
                                        changeY=-1
                                    else:
                                        changeY=1
                                    newRegionX=x+changeX
                                    newRegionY=y+changeY
                                    i.regions[newRegionX,newRegionY].append(person)
                                    i.regions[x,y].pop(i.regions[x,y].index(person))

                            elif (dayAction==1):#Im Dieing While Infected
                                pD = min(1, (1 - ma.exp( -person.age / 50 ))*Xm )#Xm is the mortality factor 
                                d=np.random.rand()
                                if d <= pD: #if the number from (0,1) generated is <= than the prob of dying, than the person dies
                                    i.regions[x,y].pop(i.regions[x,y].index(person))
                                    i.deaths+=1


                            elif (dayAction==2):#Get Cured
                                pr = 1 - ma.exp( -person.daysInfected / 2 )
                                if 0.90 > pr > 0.66:
                                    p = np.random.choice([ 1 , 2 , 3 ])
                                    if p == 1 :
                                        person.infected=True 
                                    else:#Cured
                                        person.infected=False
                                        person.daysInfected = 0
                                elif pr > 0.90: 
                                    p = np.random.choice([1,2,3,4,5,6,7,8,9,10])
                                    if p == 1 :
                                        person.infected=True 
                                    else:#Cured
                                        person.infected=False
                                        person.daysInfected = 0



                        else:#Person isnt infected
                            dayAction=np.random.randint(0,3)

                            if (dayAction==0):#moving
                                if (person.mobility())>np.random.rand() and (person.quarantined==False):
                                    if (np.random.randint(0,1)==0):
                                        changeX=-1
                                    else:
                                        changeX=1
                                    if (np.random.randint(0,1)==0):
                                        changeY=-1
                                    else:
                                        changeY=1
                                    newRegionX=x+changeX
                                    newRegionY=y+changeY
                                    i.regions[newRegionX,newRegionY].append(person)
                                    i.regions[x,y].pop(i.regions[x,y].index(person))

                            elif (dayAction==1):#Die but healthy
                                pD = min( 1, (1 - ma.exp( -person.age / 50 )))
                                d=np.random.rand()
                                if d <= pD: #if the number from (0,1) generated is <= than the prob of dying, than the person dies
                                    i.regions[x,y].pop(i.regions[x,y].index(person))
                                    i.deaths+=1


                            elif (dayAction==2):#Get Infected
                                N_active=infectedArray[x,y]
                                N_people=peopleArray[x,y]
                                if N_active>0 and N_people>0:
                                    if person.vaccinated == True:
                                        pV= (1- vE)
                                        pInoV= R*(N_active/N_people)
                                        pI= min(1,pInoV*pV)


                                        if pI>np.random.rand():
                                            person.Infected= True
                                            person.daysInfected+=1
                                            i.infections+=1
                                        else:
                                            person.Infected= False

                                    elif person.vaccinated == False:
                                        pI= min(1,R*(N_active/N_people))

                                        if pI>np.random.rand():
                                            person.Infected= True
                                            person.daysInfected+=1
                                            i.infections+=1
                                        else:
                                            person.Infected= False
#If test and quarantine is true then people have a 50% chance of testing and if they're positive they get quarantined
                        if testAndQuarantine == True and np.random.rand()>0.5 and person.infected == True:
                            person.quarantined=True
                            person.daysQuarantined+=1 
#Every 10 days deaths and infections of each country are noted in lists            
        if daysPassed%10==0:
            wDeaths.append(Wales.deaths)
            uDeaths.append(Uk.deaths)
            cDeaths.append(China.deaths)
            pDeaths.append(Poland.deaths)
 #           Wales.deaths=0
  #          Uk.deaths=0
   #         China.deaths=0
    #        Poland.deaths=0
            wInf.append(Wales.infections)
            uInf.append(Uk.infections)
            cInf.append(China.infections)
            pInf.append(Poland.infections)
#            Wales.infections=0
 #           Uk.infections=0
  #          China.infections=0
   #         Poland.infections=0

#At the end of each of the 4 simulations the lists of the infections and deaths throughout the year are added to another list
    walesDeaths.append(wDeaths)
    ukDeaths.append(uDeaths)
    chinaDeaths.append(cDeaths)
    polandDeaths.append(pDeaths)
    walesInf.append(wInf)
    ukInf.append(uInf)
    chinaInf.append(cInf)
    polandInf.append(pInf)
    

#Function that creates 1 avarage list out of the 4 lists for each country from the 4 simulations
def averaging(list):
    averageList=[]
    n=0
    for i in list[1]:
        numbers=[list[0][n],list[1][n],list[2][n],list[3][n]]
        average=stats.mean(numbers)
        averageList.append(average)
        n+=1
    return averageList
        
        
#Avearage each list of deaths and infections        
avgWalesDeaths=averaging(walesDeaths)
avgUkDeaths=averaging(ukDeaths)
avgChinaDeaths=averaging(chinaDeaths)
avgPolandDeaths=averaging(polandDeaths)
avgWalesInf=(averaging(walesInf))
avgUkInf=(averaging(ukInf))
avgChinaInf=(averaging(chinaInf))
avgPolandInf=(averaging(polandInf))
        

#Graphing

daysPassing=[]
u=0
while u <360:
    u+=10
    daysPassing.append(u)
for i in countries:
    if countries.index(i)==0:
        peopleDead=np.array(avgWalesDeaths)
    elif countries.index(i)==1:
        peopleDead=np.array(avgUkDeaths)
    elif countries.index(i)==2:
        peopleDead=np.array(avgChinaDeaths)
    elif countries.index(i)==3:
        peopleDead=np.array(avgPolandDeaths)
    plt.scatter(daysPassing,peopleDead, color= "r")
    plt.xlabel("Time passed in days")
    plt.ylabel("Number of people dead")
    plt.title("Number of people dieing every 10 days in "+i.name+", starting conditions, policy")
    plt.show()
    
for i in countries:
    if countries.index(i)==0:
        peopleInf=np.array(avgWalesInf)
    elif countries.index(i)==1:
        peopleInf=np.array(avgUkInf)
    elif countries.index(i)==2:
        peopleInf=np.array(avgChinaInf)
    elif countries.index(i)==3:
        peopleInf=np.array(avgPolandInf)
    plt.scatter(daysPassing,peopleInf, color= "b")
    plt.xlabel("Time passed in days")
    plt.ylabel("Number of people infected")
    plt.title("Number of people infected every 10 days in "+i.name+", starting conditions, policy")
    plt.show()
    
    
#The Graph For infections appear as a strait line because the probabilities for infections, deaths and cureing means that most people have been cured or died by the 10th day so the infections all happen in those 10 days. 
#This means that because the graph is cumulative it stays at the amount of infections in that first 10 days     