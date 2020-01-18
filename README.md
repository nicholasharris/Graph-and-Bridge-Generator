# Graph-and-Bridge-Generator
Created for University of Nevada, Reno's Evolutionary Computing Systems Lab (ECSL), as part of an automated bridge-inspection project. 

The purpose of this code to generate and visualize graphs of arbitrary size and density, and to generate graphs designed to follow the layout of steel-truss bridges. It can be used to generate an arbitrary large dataset of graphs or bridge-graphs of desired size and density for use in machine learning.

![alt text](https://raw.githubusercontent.com/nicholasharris/Graph-and-Bridge-Generator/master/graph.png)

![alt text](https://raw.githubusercontent.com/nicholasharris/Graph-and-Bridge-Generator/master/graph1.png)


The command line arguments of the graph_generator.py code are explained within the comments of the file. They allow you to generate graphs of arbitrary size and density, make a windy or non-windy graph, decide if the graph should take on the form of a steel-truss bridge, and control the file name the graph will be saved in (.csv format we have used in all arc routing work at ECSL). A visualization of the topology of the generated graph drawn in pyplot will also be saved as a .png 

The dataset_generator.py lets you generate many graphs at once with your chosen set of parameters. Generating large datasets takes a non-trivial amount of time - approximately 1 second per graph - so a very large data set may take a few tens of minutes to be created.

