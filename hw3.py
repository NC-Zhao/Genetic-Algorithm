# hw3, genetic algorithms
# Neal Zhao (nzhao04)
# 3/8/2022

from random import randint
from random import sample
from random import shuffle
from copy import copy
import numpy as np
weight_list = [20,30,60,90,50,70,30,30,70,20,20,60] # the list of weights of the items
value_list = [6,5,8,7,6,9,4,5,4,9,2,1] # the list of values of the items

# This class represents a combination of items in the backbag using a list of 1/0 to represent 
    # if an item is in the bag. 
class Chromosome:
    # The initialization of the class takes in the item list, 
        # and then automatically compute its value and weight
    # This class also support the fringe operations. 
    # items: the list of 1/0 represents the existence of items in the bag
    def __init__(self, items):
        self.items = copy(items)
        value = 0
        weight = 0
        for i in range(12):
            if items[i] == 1: # if this item is in the bag
                value += value_list[i]
                weight += weight_list[i]
        # if the weight exceeds, the value should be set to 0
        if weight > 250:
            self.value = 0
        else:
            self.value = value
        self.weight = weight
        
    # This function mutate a random gene in the chromosome
    # It returns a NEW chromo
    def mutate(self):
        items = copy(self.items)
        position = randint(0,11) # decides where the mutation happens
        if items[position] == 0:
            items[position] = 1
        else:
            items[position] = 0
        return Chromosome(items)
    
    # This function return two offsprings as the results of a cross-over of a couple
    # Returns a NEW chromo
    def crossOver(A, B):
        p = randint(1,11) # the position where the cross-over happens. All gene at or after `p` will mutate
        items_A = copy(A.items)
        items_B = copy(B.items)
        for i in range(p,12):
            items_A[i] = B.items[i]
            items_B[i] = A.items[i]
        return Chromosome(items_A), Chromosome(items_B)
    
    # override compare, now the comparison is based on their value
    def __lt__(self, other):
        return self.value < other.value
    def __eq__(self, other):
        return self.value == other.value
    def __ge__(self, other):
        return self.value >= other.value
    def __gt__(self, other):
        return self.value > other.value
    def __le__(self, other):
        return self.value <= other.value
    def __ne__(self, other):
        return self.value != other.value



# This class represent the process of evolve
class Evolve:
    # size_population: integer. The number of chromosome in the population. 
        # To avoid unexpected behavior, this should be a **multiply of four**
    # n_iteration: integer. The number of generations this model will run
    def __init__(self, size_population, n_iteration):
        self.size_pop = size_population
        self.n_itr = n_iteration
        self.pop = self.random_initial(self.size_pop) # a ndarray of full population, always sorted. 
        
    # Generate the initial population
        # Considering the total weight of all 12 items are 550, the probability of each 
            # item to be in the bag is 0.4. 
    def random_initial(self, size):
        pop = np.empty(size, Chromosome)
        for i in range(size): # for each 
            items = []
            for j in range(12): #create the item list for a chromosome
                x = randint(1,10) # probability check
                if x <= 4:
                    items.append(1) # 40% to be in the bag
                else:
                    items.append(0) # 60% not in the bag
            pop[i] = Chromosome(items)
        return pop
    
    # Takes in two chromosome A, B. Both will mutate itself, and also reproduce a pair of cross-over
    # Returns four chromosomes as a list
    @staticmethod
    def pair_reproduce(A, B):
        results = np.empty(4, Chromosome)
        results[0] = A.mutate()
        results[1] = B.mutate()
        results[2], results[3] = A.crossOver(B)
        return results
    
    # replace the current population with offsprings of top 50% chromosomes
    def cull_reproduce(self):
        pair = list(range(self.size_pop//2)) # create the indices of top 50% chromosomes
        shuffle(pair) # use this list to shuffle top 50% chromosomes and later pair up by indices. 
        
        new_pop = np.empty(self.size_pop, Chromosome) # slots for new population
        for i in range(self.size_pop//4): #each i represents a couple of chromosome
            # the chromosomes at indices in `pair` at 2i and 2i+1 will be coupled
            four_childs = Evolve.pair_reproduce(self.pop[pair[2*i]], self.pop[pair[2*i+1]]) 
            for j in range(4): # place these 4 childs into the new population
                new_pop[4*i+j] = four_childs[j]
        self.pop = np.sort(new_pop)[::-1] # sort the population
    
    # process the evolving process
    def run(self):
        self.best_chromo = Chromosome([0 for x in range(12)]) # teh global best
        for i in range(self.n_itr): 
            self.cull_reproduce()
            print('Best Chromosome in the generation {}: {}'.format(i, self.pop[0].items))
            print('value: {}, weight: {}'.format(self.pop[0].value, self.pop[0].weight))
            print()
            if self.best_chromo < self.pop[0]: # update the global best chromo
                self.best_chromo = self.pop[0]
        print('------------------------------------------------------')
        print('Best Chromosome in history: {}'.format(self.best_chromo.items))
        print('value: {}, weight: {}'.format(self.best_chromo.value, self.best_chromo.weight))



if __name__ == "__main__":
    print('Please input the following parameters. ')
    # input the population size
    size_population_str = input('The size of population (must be divisible by 4): ')
    try:
        size_pop = int(size_population_str)
    except ValueError:
        raise ValueError('Input is not a integer')
    if size_pop % 4 != 0:
        raise ValueError('Not divisible by 4')
    # input the number of iterations
    n_itr_str = input('The number of generations of the evolving process: ')
    try:
        n_itr = int(n_itr_str)
    except ValueError:
        raise ValueError('Input is not a integer')
    
    E = Evolve(size_pop, n_itr)
    E.run()

