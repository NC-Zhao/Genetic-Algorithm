# hw3: Genetic Algorithms

Neal Zhao

3/8/2022

## Assumptions:

- All chromosomes will not last to the next generation, they only survive one generation. 
- All fringe operations are single point. 
- After top 50% chromosomes are culled, they pair up, producing one mutation for each chromosome, and then produce two chromosomes through pairwise cross over. 

## Define the problem

1. A chromosome is defined as a list of length 12 of 1 or 0. Each slot corresponds to an item, 1 if it is in the bag, 0 otherwise. 
2. The initial population is generated randomly. Each item has 40% chance to be in the bag. The size of the initial population is specified by the user. 
3. The fitness function is the sum of value of the items in the bag. If the total weight is 250, then the fitness function will evaluate to 0. 
4. For each generation, 50% of the highest value chromosomes will be able to reproduce. 
5. The chromosomes will pair up into couples. Each chromosomes will mutate a single gene. Each couple will perform a single-point-cross-over, reproduce two children. 
6. The algorithm ends at some number of iterations specified by the user. 