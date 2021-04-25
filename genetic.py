
import random
from operator import itemgetter

from typing import Callable, List, TypeVar
# type definition

Chromosome = TypeVar('Chromosome', List, List, int)
Population = List[Chromosome]


class GA:
    def __init__(self, populationSize: int, generations: int,
                 generationRange: tuple, fitnessFunction: Callable) -> None:
        self.populationSize = populationSize
        self.generations = generations
        self.fitnessFunction = fitnessFunction
        self.generationRange = generationRange
        self.population: Population = []
        pass

    def valuesToBin(self, values: List):
        # Creating binary representation
        binValues = []
        for v in values:
            binStr = bin(v)[2:]
            binStr = "0"*(4-len(binStr))+binStr
            binVal = [int(x) for x in binStr]
            binValues.append(binVal)
        return binValues

    def createInitialPopulation(self):
        generation = []
        for i in range(self.populationSize):
            a, b = self.generationRange
            # Creating the crhomosome
            C: Chromosome = {
                'values': [random.randint(a, b), random.randint(a, b), random.randint(a, b)],
                'binValues': [],
                'weight': 0
            }

            C['binValues'] = self.valuesToBin(C['values'])

            C['weight'] = self.fitnessFunction(*C['values'])
            generation.append(C)
        self.population.append(generation)

    def tournament(self, generation: List[Chromosome]) -> List[Chromosome]:
        winners: List[Chromosome] = []

        challengers = [x for x in range(len(generation))]

        print("\n**Starting tournament**\n")

        while(len(challengers) > 1):
            a, b = random.choices(challengers, k=2)

            while(a == b):
                a, b = random.choices(challengers, k=2)

            chA, chB = generation[a], generation[b]

            winner: Chromosome = {}
            indexOfWinner = 0

            if(chA['weight'] > chB['weight']):
                winner = chA
                indexOfWinner = a
            else:
                winner = chB
                indexOfWinner = b
            print(f"{a} vs {b} => winner is {indexOfWinner}")

            winners.append(winner)

            challengers = [x for x in challengers if x != a and x != b]

            # Checking fitness of both challengers
        return winners+winners+winners

    def binToVal(self, bin: str):
        return int(bin, 2)

    def cross(self, parentA: Chromosome, parentB: Chromosome, i: int):

        bitsA, bitsB = [], []
        for varA, varB in zip(parentA['binValues'], parentB['binValues']):
            bitsA += varA
            bitsB += varB

        middlePoint = len(bitsA)//2

        if(i == 0):
            candidateBits = bitsA[:middlePoint]+bitsB[middlePoint:]
        elif i == 1:
            candidateBits = bitsA[middlePoint:] + bitsB[:middlePoint]
        elif i == 2:
            candidateBits = bitsB[middlePoint:] + bitsA[:middlePoint]
        else:
            candidateBits = bitsB[:middlePoint] + bitsA[middlePoint:]

        # Check if it could be a potential solution
        if(candidateBits != bitsA and candidateBits != bitsB):
            candidate: Chromosome = {
                'values': [], 'binValues': [], 'weight': 0}

            candidate['binValues'] = [candidateBits[0:4],
                                      candidateBits[4:8], candidateBits[8:]]

            for x in candidate['binValues']:
                candidate['values'].append(self.binToVal(
                    "".join(map(str, x))))

            candidate['weight'] = self.fitnessFunction(*candidate['values'])

            return candidate
        return -1

    def newGen(self):

        # Launching a tournament and gettin winners
        winners = self.tournament(self.population[-1])

        # Cutting out excess of members
        winners = winners[0:self.populationSize]

        print("--Winners are: \n")

        for w in winners:
            print(str(w['binValues'])+f" -> {w['weight']}")

        print("\n==Cross proccess==\n")

        # Choosing 2 different parents from winners iteratively winners/2 times

        potentialNewChromosomes = winners

        for _ in range(len(winners)//2):
            parentA, parentB = random.choices(winners, k=2)
            while(parentA['binValues'] == parentB['binValues']):
                parentA, parentB = random.choices(winners, k=2)

            print("::Choosen parents are::\n")
            print(str(parentA['binValues'])+f"=>{parentA['weight']}\t"+str(
                parentB['binValues'])+f"=>{parentB['weight']}\n")

            # Cross operation
            print(" ||Potential candidates from those parents||")
            for i in range(3):
                x = self.cross(parentA, parentB, i)
                if(x != -1):
                    print(x)
                    potentialNewChromosomes.append(x)

        newGen = sorted(potentialNewChromosomes,
                        key=itemgetter('weight'), reverse=True)
        newGen = newGen[:self.populationSize]

        print("~~~~~~~~~~~~New generation is~~~~~~~~~~~~~\n")
        for chromosome in newGen:
            print(chromosome)

        self.population.append(newGen)

    def evolve(self):
        for _ in range(self.generations):
            self.newGen()


def f(x, y, z): return x+y**2+z**3


populationSize = int(input("Enter population size: "))
generations = int(input("Enter generation number: "))
a, b = [int(x) for x in input(
    "Enter range, separated by spaces: ").split(" ")]


x = GA(populationSize,  generations, [a, b], f)

x.createInitialPopulation()

for i in range(len(x.population)):
    generation = x.population[i]
    print("-"*5+f"Generation {i}"+"-"*5)
    for chromosome in generation:
        print(chromosome)


x.evolve()
