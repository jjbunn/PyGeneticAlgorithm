'''
Created on May 4, 2015

@author: Julian
'''

import random

class Chromosome:
    '''
    A chromosome object that has a list of values, and a length used for 
    swapping values when mating
    '''

    def __init__(self, values, swap_length=None):
        '''
        Constructor
        '''
        assert isinstance(values, list)
        
        self.length = len(values)
        self.chromosome = values 
   
        # the length of the chromosome part that will be swapped between parents
        if swap_length:
            self.swap_length = swap_length
        else:
            # a default swap length if not specified - one third of the total length
            self.swap_length = max(self.length / 3, 1) 

    def mate(self, father):
        '''
        Mates this mother chromosome with a father and produces a pair of offspring
        '''
        #swap a segment between the mother and the father
        swap_start_position = random.randrange(self.length-self.swap_length)
        swap_end_position = swap_start_position + self.swap_length
        #obtain the list of cut alleles in the father's and mother's chromosomes
        father_cut = father.chromosome[swap_start_position:swap_end_position]
        mother_cut = self.chromosome[swap_start_position:swap_end_position]

        #create a new chromosome with the alleles for the first child
        offspring1 = Chromosome(self.chromosome[:swap_start_position] + \
                               father_cut + \
                               self.chromosome[swap_end_position:])

        # create a new chromosome with the alleles for the second child
        offspring2 = Chromosome(father.chromosome[:swap_start_position] + \
                               mother_cut + \
                               father.chromosome[swap_end_position:])
       
        return (offspring1, offspring2)
    
    def enforce_all_entries(self, target):
        '''
        Ensures that the target list contains all items in the chromosome
        '''  
        missing = set(self.chromosome) - set(target)
        while len(missing) > 0:
            duplicates = set([x for x in target if target.count(x) > 1])
            if len(duplicates) == 0:
                break
            target[target.index(duplicates.pop())] = missing.pop()
            
        return target
    
    def mate_no_duplicates(self, father):
        '''
        Mates this mother chromosome with a father and produces a pair of offspring
        This mating scheme (as opposed to "mate" ensures that the chromosome alleles are not duplicated.
        It is used for e.g. the Travelling Salesman problem which requires that all the cities
        appear in the chromosome
        '''
        #swap a segment between the mother and the father
        swap_start_position = random.randrange(self.length-self.swap_length)
        swap_end_position = swap_start_position + self.swap_length
        #obtain the list of cut alleles in the father's and mother's chromosomes
        father_cut = father.chromosome[swap_start_position:swap_end_position]
        mother_cut = self.chromosome[swap_start_position:swap_end_position]
        
        offspring1_chromosome = self.chromosome[:swap_start_position] + \
                               father_cut + \
                               self.chromosome[swap_end_position:]
        # ensure that we are not missing alleles

        offspring1_chromosome = self.enforce_all_entries(offspring1_chromosome)
            
        offspring1 = Chromosome(offspring1_chromosome)
            
        # create a new chromosome with the alleles for the second child
        offspring2_chromosome = father.chromosome[:swap_start_position] + \
                               mother_cut + \
                               father.chromosome[swap_end_position:]
        offspring2_chromosome = self.enforce_all_entries(offspring2_chromosome)
            
        offspring2 = Chromosome(offspring2_chromosome)
       
        return (offspring1, offspring2)
    
    def mutate(self, list_of_alleles):
        '''
        Mutates a random allele in this chromosome by replacing it with a new value 
        randomly chosen from the supplied list of alleles
        '''
        self.chromosome[random.randrange(self.length)] = random.choice(list_of_alleles)
        
    def mutate_swap(self):
        '''
        Mutates a pair of random alleles in this chromosome by swapping 
        '''
        location1 = random.randrange(self.length)
        location2 = random.randrange(self.length)

        (self.chromosome[location2], self.chromosome[location1]) = (self.chromosome[location1], self.chromosome[location2])
        
    def mutate_rotate(self):
        '''
        Mutates this chromosome by rotating it from a random position 
        '''
        location = random.randrange(self.length)
        
        self.chromosome = self.chromosome[location:] + self.chromosome[:location]
        
    def chromosome_string(self):
        '''
        Returns a string representation of the chromosome
        '''
        return str(self.chromosome)
    
    def value(self, function):
        '''
        Returns the value of the chromosome when the given function is applied to the
        chromosome's alleles
        '''
        return function(self.chromosome)
        
if __name__ == '__main__':
    
    # create a population of 5 chromosomes, each of length 8 genes
    c = []
    length = 8
    for i in range(5):
        alleles = [random.randrange(8) for _ in range(length)]
        cc = Chromosome(alleles)
        print cc.chromosome_string()
        c.append(cc)
      
    # pick two chromosomes from the population  
    one = random.choice(c)
    two = random.choice(c)
    
    # mate the two chromosomes, to produce two new chromosomes
    print 'Mate\t', one.chromosome_string(), 'with', two.chromosome_string()
    (child1, child2) = one.mate(two)
    print 'gives\t', child1.chromosome_string(), child2.chromosome_string()
    
    # mutate one of the children's chromosome alleles
    print 'Mutate\t', child1.chromosome_string()
    child1.mutate([200, 300, 400])
    print 'gives\t', child1.chromosome_string()
    
    # define some fitness functions that will be applied to the chromosomes
    def summation(args):
        return sum(args)
    
    def all_non_zero(args):
        for a in args:
            if a == 0:
                return False
        return True
        
    # test the fitness functions
    print 'child summation value',child1.value(summation)
    print 'child all non zero value',child1.value(all_non_zero)
    

        
    
        
         
        
        