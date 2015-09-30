'''
Created on May 5, 2015

@author: julian
'''
import math
import random
import matplotlib.pyplot as plt
from Chromosome import *

REGION_SIZE = 100.0
    
NUMBER_OF_CITIES = 10
    
NUMBER_OF_CHROMOSOMES = 100
    
NUMBER_OF_EPOCHS = 100
    
MUTATION_PROBABILITY = 0.25

RANDOM_SEED = 9876

cities = {}

def plot_cities(chromosome=None, epoch=None):
    plt.xlim((-REGION_SIZE*0.1,REGION_SIZE*1.1))
    plt.ylim((-REGION_SIZE*0.1,REGION_SIZE*1.1))

    plt.scatter([p[0] for p in cities.itervalues()], [p[1] for p in cities.itervalues()])  
    for name,xy in cities.iteritems():
        plt.annotate(name,xy=xy,xytext=(xy[0]+1,xy[1]-1))

    if chromosome:
        plt.plot([cities[c][0] for c in chromosome], [cities[c][1] for c in chromosome])
        plt.text(cities[chromosome[0]][0] + 2.0, cities[chromosome[0]][1] + 2.0, 'Start')
        plt.text(cities[chromosome[-1]][0] + 2.0, cities[chromosome[-1]][1] + 2.0, 'Finish')
    
    if epoch:
        plt.title('EPOCH '+str(epoch))
    
    plt.show()


def main():
    # create a set of cities in a spiral in a square region
    
    # choose an angle for the start of the spiral
    phi = 0
    # set the spiral twist loop number
    loops = 1.5
    # calculate the change in angle for each city
    dphi = math.pi * loops / float(NUMBER_OF_CITIES)

    for i in range(NUMBER_OF_CITIES):
        # get radius of city centre
        r = 0.5*REGION_SIZE*float(i+1)/float(NUMBER_OF_CITIES)
        phi += dphi
        xcity = 0.5*REGION_SIZE + r*math.cos(phi);
        ycity = 0.5*REGION_SIZE + r*math.sin(phi);
        city_name = chr(i+65)
        # add this city to the dictionary
        cities[city_name] = (xcity, ycity)
        
    #plot_cities()
       
    # create a population of chromosomes
    # each chromosome will get a random ordering of cities to visit
    
    chromosomes = []
    
    random.seed(RANDOM_SEED)
    
    for i in range(NUMBER_OF_CHROMOSOMES):
        city_list = list(cities.keys())
        random.shuffle(city_list)
        chromosomes.append(Chromosome(city_list))

    
    # we define a function which computes the path length for a given order of cities
    def path_length(city_list, cities):
        sum = 0.0
        for i in range(1,len(city_list)):
            (x1,y1) = cities[city_list[i-1]]
            (x2,y2) = cities[city_list[i]]
            sum += math.sqrt((x1-x2)**2+(y1-y2)**2)
        return sum
    
    epoch = 1
    
    while True:
        
        # find the path length for each chromosome
        path_lengths = {}
        for c in chromosomes:
            path_lengths[c] = path_length(c.chromosome, cities) 

        sorted_chromosomes = sorted(path_lengths, key=path_lengths.get, reverse=False)
        
        print 'Epoch',epoch,'Best chromosome',sorted_chromosomes[0].chromosome_string(), \
            path_lengths[sorted_chromosomes[0]]
            
        epoch += 1
        
        if epoch > NUMBER_OF_EPOCHS:
            break
        
        # select the mating population
        mating_population = sorted_chromosomes[:NUMBER_OF_CHROMOSOMES/2]
        
        # have the population mate in pairs, to produce offspring
        
        offspring_population = []
        
        while len(offspring_population) < NUMBER_OF_CHROMOSOMES/2:
            mother = random.choice(mating_population)
            father = random.choice(mating_population)
            (offspring1, offspring2) = mother.mate_no_duplicates(father)
            # mutate the offspring with some probability
            if random.random() < MUTATION_PROBABILITY:
                offspring1.mutate_swap()
            if random.random() < MUTATION_PROBABILITY:
                offspring2.mutate_swap()
            offspring_population.append(offspring1)
            offspring_population.append(offspring2)
        
        # the new population is the mating population plus the offspring
        
        chromosomes = mating_population + offspring_population
        

 
    # we plot the solution at the stopping condition    
        
    plot_cities(chromosomes[0].chromosome, str(epoch-1) + ' Best ' + chromosomes[0].chromosome_string())

    
    



if __name__ == '__main__':
    main()