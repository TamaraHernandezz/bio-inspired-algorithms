import random
import numpy

# Implements the random initialization of individuals using the binary representation.
def createIndividual(nbBits):
  return numpy.random.randint(2, size = nbBits)

#esta función no cambia, solo que ahora los 0 y 1 van a definir a que array pertenece cada numero 

# Implements the one point crossover on individuals using the binary representation.
def combine(parentA, parentB, cRate):
  if (random.random() <= cRate):
    cPoint = numpy.random.randint(1, len(parentA))   
    offspringA = numpy.append(parentA[0:cPoint], parentB[cPoint:])
    offspringB = numpy.append(parentB[0:cPoint], parentA[cPoint:])
  else:
    offspringA = numpy.copy(parentA)
    offspringB = numpy.copy(parentB)
  return offspringA, offspringB

# Implements the flip mutation on individuals using the binary representation.
def mutate(individual, mRate):
  for i in range(len(individual)):
    if (random.random() <= mRate):
      if (individual[i] == 0):
        individual[i] = 1        
      else:
        individual[i] = 0        
  return individual

# Implements the fitness function of individuals using the binary representation and solving the max-one problem.
def evaluate(individual, numeros):
  sumaA =numpy.sum(numeros[individual==0])
  sumaB =numpy.sum(numeros[individual==1])
  return abs(sumaA - sumaB)
#cambio igual aquí, esta función ahora recibe a los numeros y al individuo y asigna un array para luego generar la suma de cada uno y la diferencia absoluta posteriormente 


# Implements the tournament selection.
def select(population, evaluation, tournamentSize):
  winner = numpy.random.randint(0, len(population))
  for i in range(tournamentSize - 1):
    rival = numpy.random.randint(0, len(population))
    if (evaluation[rival] < evaluation[winner]): #se hace el cambio de > a < para minimizar diferencia abs
      winner = rival
  return population[winner]

# Implements a genetic algorithm for solving the max-one problem with individuals using the binary representation.
def geneticAlgorithm(numeros, populationSize, cRate, mRate, generations):
  # Creates the initial population (it also evaluates it)
  n=len(numeros) #se añade la longitud del array para poder utilizar create individual 
  population = [None] * populationSize
  evaluation = [None] * populationSize  
  for i in range(populationSize):
    individual = createIndividual(n)
    population[i] = individual
    evaluation[i] = evaluate(individual, numeros)
  # Keeps a record of the best individual found so far
  index = 0;
  for i in range(1, populationSize):
    if (evaluation[i] < evaluation[index]):
      index = i
  bestIndividual = numpy.copy(population[index])
  bestEvaluation = evaluation[index]
  # Runs the evolutionary process    
  for i in range(generations):
    k = 0
    newPopulation = [None] * populationSize    
    for j in range(populationSize // 2):
      parentA = select(population, evaluation, 3)
      parentB = select(population, evaluation, 3)
      newPopulation[k], newPopulation[k + 1] = combine(parentA, parentB, cRate)       
      k = k + 2    
    population = newPopulation
    for j in range(populationSize):
      population[j] = mutate(population[j], mRate)
      evaluation[j] = evaluate(population[j], numeros) #agrego la varaible de numeros
      # Keeps a record of the best individual found so far
      if (evaluation[j] < bestEvaluation): #aqui también se cambia el sentido de la desigualdad para minimizar la diferencia
        bestEvaluation = evaluation[j]
        bestIndividual = population[j]
  return bestIndividual, bestEvaluation

# solves the problem using the genetic algorithm
numeros=numpy.array([12, 45, 78, 23, 56, 89, 10, 34, 67, 90, 15, 88])

solucion, diferencia = geneticAlgorithm(numeros, 40, 0.9, 0.02, 200)

#separacion por bits
grupoA = numeros[solucion == 0]
grupoB = numeros[solucion == 1]

print("Grupo A:", list(grupoA), "| Suma:", sum(grupoA))
print("Grupo B:", list(grupoB), "| Suma:", sum(grupoB))
print("Diferencia mínima lograda:", diferencia)
