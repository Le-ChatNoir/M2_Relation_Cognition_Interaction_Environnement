import matplotlib
import matplotlib.pyplot as plt
import random
import math
import statistics
import pandas as pd

fileExpeVarAngle = "expePsychoResultsVarAngleFixTime.csv"
fileExpeVarTime = "expePsychoResultsFixAngleVarTime.csv"
MC = 0.0
MA = 0.0

def afficheResult(file, angle_or_duration=0):
    num,time,angle,duration,errorX,errorY=[],[],[],[],[],[]
    with open(file, 'r') as f:
        ligne = f.readline()
        ligne = f.readline()
        while(ligne):
            #ligne = f.readline()
            n,t,a,d,eX,eY=ligne.split(';')
            num.append(int(n))
            time.append(float(t))
            duration.append(float(d))
            angle.append(float(a))
            errorX.append(float(eX))
            errorY.append(float(eY)*float(eY))
            ligne=f.readline()
            
            
    data = [num,time,angle,duration,errorX,errorY]   
    data = sorted(zip(*data), key=lambda args: args[2+angle_or_duration])
    data = list(zip(*data))

    
    plt.plot(data[2+angle_or_duration],errorY,"g+")
    plt.xlabel(("angle", "duration")[angle_or_duration])
    plt.ylabel("errorY^2")
    plt.show()
    
def model1(sampleSize, file, angle_or_duration=0):
    global MC #Define MC as a global variable
    randomLines=[]
    num,time,angle,duration,errorX,errorY, errorY2=[],[],[],[],[],[],[]
    with open(file, 'r') as f:
        ligne = f.readline()
        ligne = f.readline()
        while(ligne):
            #ligne = f.readline()
            n,t,a,d,eX,eY=ligne.split(';')
            num.append(int(n))
            time.append(float(t))
            duration.append(float(d))
            angle.append(float(a))
            errorX.append(float(eX))
            errorY.append(float(eY))
            errorY2.append(float(eY)*float(eY))
            ligne=f.readline()
            
    data = [num,time,angle,duration,errorX,errorY, errorY2]

    #Select sizeSample numbers of random rows, num
    randomLines = random.sample(data[0], sampleSize)
    randomLines.sort()
    print("Lines picked: ", randomLines)

    #Extract the errorY, and errorY²
    counter = 0
    errorYArray = []
    simpleY = []
    for item in randomLines:
        #Item is the number of the line picked.
        #Data is cut as [num,time,angle,duration,errorX,errorY,errorY2]
        simpleY.append(data[5][item-1])
        errorYArray.append(data[6][item-1])
        counter += 1

     #Print the result
    i=0
    while i < len(randomLines):
        print("Line  ", randomLines[i], " ErrorY: ", simpleY[i], " ErrorY²: ", errorYArray[i])
        i += 1
        
    #Printing the results
    print("===Model 1 (for ", sampleSize, " values.)===")
    print("    Moyenne (b0): ", statistics.mean(errorYArray))
    print("    Mediane: ", statistics.median(errorYArray))
    print("    Variance: ", statistics.pvariance(errorYArray))
    print("    Ecart type: ", statistics.pstdev(errorYArray))
    print("    Coefficient de variation: ", statistics.pstdev(errorYArray) / statistics.mean(errorYArray))
    print()

    MC = statistics.mean(randomLines)


"""Ybar est la moyenne des erreurs de prédiction, donc ce qui différencie la moyenne/médianne et la vrai erreur. b1 est ce qui est calculé en haut,
et abar la moyenne des angles b1 est l'angle I moins la moyenne des angles par rapport a l'erreur de prédiction Y de l'angle moins la moyenne des
angles de prédiction sur la somme de l'angle I moins la moyenne des angles au carré

Pout Y. On prend la moyenne par exemple, et on la différencie avec l'angle trouvé, par exemple ona une moyenne de 4, on a I = 1, on aura alors un Y de 3."""

def model2(sampleSize, file, angle_or_duration=0):
    global MA #Define MA as a global variable
    randomLines=[]
    num,time,angle,duration,errorX,errorY, errorY2=[],[],[],[],[],[],[]
    print("OPENING FILE")
    with open(file, 'r') as f:
        ligne = f.readline()
        ligne = f.readline()
        while(ligne):
            #print(ligne)
            #ligne = f.readline()
            n,t,a,d,eX,eY=ligne.split(';')
            num.append(int(n))
            time.append(float(t))
            duration.append(float(d))
            angle.append(float(a))
            errorX.append(float(eX))
            errorY.append(float(eY))
            errorY2.append(float(eY)*float(eY))
            ligne=f.readline()
            
    data = [num,time,angle,duration,errorX,errorY,errorY2]

    #Select sizeSample numbers of random rows, num
    randomLines = random.sample(data[0], sampleSize)
    randomLines.sort()
    print("Lines picked: ", randomLines)

    #Extract the errorY, angle, and errorY²
    counter = 0
    simpleY = []
    errorYArray = []
    anglesArray = []
    for item in randomLines:
        #Item is the number of the line picked.
        #Data is cut as [num,time,angle,duration,errorX,errorY,errorY2]
        simpleY.append(data[5][item-1])
        errorYArray.append(data[6][item-1])
        anglesArray.append(data[2][item-1])
        counter += 1

    #Print the result
    i=0
    while i < len(randomLines):
        print("Line  ", randomLines[i], " Angle: ", anglesArray[i], " ErrorY: ", simpleY[i], " ErrorY²: ", errorYArray[i])
        i += 1

    #Il faut faire la moyenne de toutes les erreurY et tous les angles associés, puis pour chaque angle avoir Yi et Ai pour calculer la somme (Ai - Abar)*(Yi - Ybar)
    moyErrY = statistics.mean(errorYArray)
    moyAngles = statistics.mean(anglesArray)

    #Consitution des valeurs du "haut" et du "bas" de l'operation b1
    i=0
    sumTop = 0
    sumBot = 0
    while i < len(randomLines):
        sumTop += (anglesArray[i] - moyAngles)*(errorYArray[i] - moyErrY)
        sumBot += pow((anglesArray[i] - moyAngles), 2)
        i += 1

    #Calcul b1 et b0
    b1 = sumTop/sumBot
    b0 = moyErrY - b1 * moyAngles

    #Printing the results
    print("===Model 2 (for ", sampleSize, " values.)===")
    print("    b1: ", b1)
    print("    b0: ", b0)
    print("    Moyenne: ", statistics.mean(errorYArray))
    print("    Mediane: ", statistics.median(errorYArray))
    print("    Variance: ", statistics.pvariance(errorYArray))
    print("    Ecart type: ", statistics.pstdev(errorYArray))
    print("    Coefficient de variation: ", statistics.pstdev(errorYArray) / statistics.mean(errorYArray))
    print()

    MA = b1

def PRE(MC, MA):
	#MC est Eyi, et MA est b1 de model2
	#ERREUR(MC) et ERREUR(MA) sont les sommes du carré des erreurs
	print("MC: ", MC, "MA: ", MA)
	preResult = (MC-MA)/MC
	print("La Proportion de Réduction de l'Erreur est de : ", preResult)



#===========MAIN==============

afficheResult(fileExpeVarAngle)

#model1(3, fileExpeVarAngle)
model1(10, fileExpeVarAngle)
#model1(60, fileExpeVarAngle)

#model2(3, fileExpeVarAngle)
model2(10, fileExpeVarAngle)
#model2(60, fileExpeVarAngle)

PRE(MC,MA)

#Pour test a 3: PRE = 1.0006904820108737
#Pour test a 10: PRE = 0.9999464298866454
#Pour test a 60: PRE = 1.0014151900079447

#On a une PRE proche de 1 à chaque coup. Une valeur PRE proche de 1 veut dire qu'il y a une prediciton quasi parfaite, l'erreur est completement eliminee.
#On peut donc deduire que connaitre l'angle a une correlation forte avec la prediction de l'erreurY.
#La modele 2 est donc grandement supperieur au modele 1