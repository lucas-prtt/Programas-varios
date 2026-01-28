import random
import math
import string
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file = open(os.path.join(script_dir, "materias.cfg"))
configFile = open(os.path.join(script_dir, "settings.cfg"))
config = dict()
for line in configFile.readlines():
    if(line.strip().startswith("#") or line.strip()==""): 
        continue
    k, v = line.split("=")
    if v.__contains__("."):
        v = float(v.strip())
    else:
        v = int(v.strip())
    k = k.strip()
    config[k] = v
# Constraints
cantidadDeCarpetas = config["cantidadDeCarpetas"]
maxMateriasPorCarpeta = config["maxMateriasPorCarpeta"]
maxCarpetasPorDia = config["maxCarpetasPorDia"]
# Configuracion Simulated Annealing
initialTemp = config["initialTemp"]
finalTemp = config["finalTemp"]
coolingRate = config["coolingRate"]
maxIterations = config["maxIterations"]



class Carpeta:
    def __init__(self, carpeta=None):
        if(carpeta == None):
            self.materias = []
        elif(carpeta.__class__ == Carpeta):
            self.materias = list(carpeta.materias)   
        else:
            raise Exception("Error en el constructor de carpeta")
    def __repr__(self):
        return f"(Carpeta: {self.materias})"
    def agregarMateria(self, materia:str):
        if(len(self.materias)>=maxMateriasPorCarpeta):
            raise Exception("Max de materias alcanzada")
        self.materias.append(materia)
    def eliminarMateria(self, materia:str):
        self.materias.remove(materia)
    def obtenerMateriaRandom(self):
        if(len(self.materias) == 0):
            return None
        return self.materias[random.randrange(0, len(self.materias))]
    
def getAlternative(carpetas:list[Carpeta]):
    altCarpetas = list(map(Carpeta, carpetas))
    c1 = altCarpetas.pop(random.randrange(0, len(altCarpetas)))
    c2 = altCarpetas.pop(random.randrange(0, len(altCarpetas)))
    m1 = c1.obtenerMateriaRandom()
    m2 = c2.obtenerMateriaRandom()
    if(m1 != None and m2 != None):
        c1.eliminarMateria(m1)
        c2.eliminarMateria(m2)
        c2.agregarMateria(m1)
        c1.agregarMateria(m2)
    else:
        if(m2 != None):
            c1.agregarMateria(m2)
            c2.eliminarMateria(m2)
        elif(m1 != None):
            c2.agregarMateria(m1)
            c1.eliminarMateria(m1)
    altCarpetas.append(c1)
    altCarpetas.append(c2)
    return altCarpetas
def carpetasLlevadas(carpetas, materias):
    materiasLlevadas = []
    carpetasLlevadas = []
    carpetasNoLlevadas = list(carpetas)
    for materia in materias:
        if(materiasLlevadas.__contains__(materia)):
            continue
        else:
            for c in carpetasNoLlevadas:
                if(c.materias.__contains__(materia)):
                    materiasLlevadas.extend(c.materias)
                    carpetasLlevadas.append(c)
                    carpetasNoLlevadas.remove(c)
                    break
    return carpetasLlevadas

def score(carpetas:list[Carpeta]):
    score = 0
    for dia in dias:
        qcarpetas = len(carpetasLlevadas(carpetas, horarios[dia]))
        score += qcarpetas
    return score


def isValid(carpetas:list[Carpeta]):
    for dia in dias:
        qcarpetas = len(carpetasLlevadas(carpetas, horarios[dia]))
        if(qcarpetas > maxCarpetasPorDia):
            return False
    return True


dias = []
horarios = dict()
for line in file.readlines():
    dia, materias = line.split("=")
    materias = set(map(str.strip, materias.split(",")))
    horarios[dia]=materias
    dias.append(dia)

materias = set(mat for dia in horarios.values() for mat in dia)

if(len(materias) > cantidadDeCarpetas * maxMateriasPorCarpeta):
    print(f"No fue posible organizar {len(materias)} materias en {cantidadDeCarpetas} carpetas de hasta {maxMateriasPorCarpeta} materias cada una")
    input()
    exit()

def getInitialSolution(materias:set[str]):
    materias = list(materias)
    random.shuffle(materias)
    carpetas = [Carpeta() for x in range(0, cantidadDeCarpetas)]
    for c in carpetas:
        while materias:
            try:
                c.agregarMateria(materias[0])
                materias.pop(0)
            except:
                break
    return carpetas


def executeSimulatedAnnealing():
    i=0
    currentSolution = getInitialSolution(materias)
    while(not isValid(currentSolution) and i<maxIterations):
        currentSolution = getInitialSolution(materias)
        i+=1
    bestSolution = currentSolution
    currentScore = score(currentSolution)
    bestScore = currentScore
    temperature = initialTemp
    while(temperature > finalTemp and i < maxIterations):
        nextSolution = getAlternative(currentSolution) 
        nextScore = score(nextSolution)
 
        if nextScore < currentScore:
            currentSolution = nextSolution
            currentScore = nextScore
            if currentScore < bestScore and isValid(currentSolution):
                bestSolution = currentSolution
                bestScore = currentScore
        else:
            acceptanceProb = math.exp((currentScore - nextScore) / temperature)
            if random.random() < acceptanceProb:
                currentSolution = nextSolution
                currentScore = nextScore
        temperature *= coolingRate
        i+=1
    print(f"Simulated Annealing ejecutado con {i} iteraciones") 
    if(isValid(bestSolution)):
        return bestSolution, bestScore
    else:
        raise Exception(f"No se pudo encontrar una solucion que respete el maximo de {maxCarpetasPorDia} carpetas por dia y {maxMateriasPorCarpeta} materias por carpeta")

def printSolutions(mejoresCarpetas, mejorScore):
    def intACodigo(n:int)->str:
        result = []
        while n > 0:
            n -= 1
            remainder = n % 26
            result.append(string.ascii_uppercase[remainder])
            n //= 26
        return "".join(result[::-1])
    print(f"Mejor solucion encontrada con media de {mejorScore/len(horarios):.2f} carpetas por dia")

    codeToCarpeta = dict()
    carpetaToCode = dict()
    outputtedCodes = []
    i = 1
    for c in mejoresCarpetas:
        codeToCarpeta[intACodigo(i)] = c
        carpetaToCode[c] = intACodigo(i)
        outputtedCodes.append(intACodigo(i))
        i+=1
    print("Carpetas:")
    for cod in outputtedCodes:
        print(f" > {cod}   -   {codeToCarpeta[cod].materias}")

    for dia in dias:
        print(f"{dia}: {",".join(list(map(carpetaToCode.get, carpetasLlevadas(mejoresCarpetas, horarios[dia]))))}")
try:
    print(f"\n\n")
    mejoresCarpetas, mejorScore = executeSimulatedAnnealing()
    printSolutions(mejoresCarpetas, mejorScore)
    print(f"\n")
except Exception as e:
    print(f"\n{e}\n")

input()