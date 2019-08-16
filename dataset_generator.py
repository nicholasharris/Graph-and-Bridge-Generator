'''
Program to generate an arbitrarily large dataset of graphs
of desired size and type.

Evolutionary Computing Systems Lab, University of Nevada, Reno.
Created by Nicholas Harris
'''

import math
import random
import os
import subprocess

import time

#Parameters
NUM_GRAPHS = 100

#measure the time needed to generate dataset
start = time.time()

print("Starting data generation...")
#Run Program a set number of times
for y in range(NUM_GRAPHS):
       
        graph_size = random.randint(20, 70)
        #Call the program via cmd string
        # The graph paramerts may be set to anything.
        subprocess.call( ["python", "graph_generator.py", str(graph_size), "0.1", "true", "true", "bridge" + str(y) + ".csv"])
        
        
end = time.time()

print("time elapsed: " + str(end-start))
