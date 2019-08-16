##########################
#   UNR Evolutionary Computing Systems Lab 
#   Graph and Bridge generator
#   Created by Nicholas Harris
##########################

'''
Python Program to generate and visualize graphs and
    bridge-graphs of a chosen size and density

Used in conjuction with the bridge inspection project
    at ECSL, Univeristy of Nevada, Reno.
'''

'''
TO RUN: call this program in the command line and pass as arguments:
        NUM_VERTICES (INT), DENSITY (float 0-1), windy (true/false), MAKE_BRIDGE (true/false), output_file_name.csv
'''

import argparse
import random
import sys
import math

import matplotlib.pyplot as plt

#Function to parse a boolean value from a string given in the command line arguments
def str_to_bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

#Function to create a graph with given parameters and save it
def make_general_graph(n_vertices, density, windy, output_file):

    random.seed()

    #initialize NxN (N vertices) matrix to store graph representation
    matrix = []
    for x in range(n_vertices):
        row = []
        for y in range(n_vertices):
            if(x == y):
                row.append(0)
            else:
                #add an empty connection
                row.append(-1)                
        matrix.append(row)

    #For every possible connection (element in the matrix), create a
    #connection with probability given by DENSITY, and assign a
    # random value 1-15. Mirror values in matrix (as connection ij == ji)
    # and transform opposite values if graph is windy
    num_edges = 0
    for x in range(n_vertices):
        for y in range(n_vertices):
            if(y > x):
                if (random.random() < DENSITY):
                    #add a connection
                    matrix[x][y] = (random.randint(1, 15))
                    num_edges += 1
                    if(windy == False):
                        matrix[y][x] = matrix[x][y]
                    else:
                        matrix[y][x] = (random.randint(1, 15))

    #Run through the graph again and make sure every node has at least one connection
    for i in range(2):
        for x in range(n_vertices):
            connection_flag = False
            for y in range(n_vertices):
                if(matrix[x][y] > 0 ):
                    connection_flag = True

            if connection_flag == False:
                index = random.randint(1, n_vertices) - 1
                while index == x:
                    index = random.randint(1, n_vertices) - 1
                matrix[x][index] = (random.randint(1, 15))
                num_edges += 1
                if(windy == False):
                    matrix[index][x] = matrix[x][index]
                else:
                     matrix[index][x] = (random.randint(1, 15))
              


    #Save the produced graph in a .csv file
    with open(output_file, 'w') as o:
        for x in range(n_vertices):
            for y in range(n_vertices):
                if y != n_vertices - 1:
                    o.write(str(matrix[x][y]) + ",")
                else:
                    o.write(str(matrix[x][y]) + "\n")

        o.write("\n")
        for x in range(n_vertices):
            o.write(" , ")
        o.write("NUM_VERTICES: " + str(n_vertices) + ",")
        o.write(" , ")
        o.write("NUM_EDGES: " + str(num_edges) + "\n")

    #Draw visualization of graph and display
    points_x = [] #x, y coordinates of vertices
    points_y = []

    x_count = 0
    y_count = 0
    for x in range(n_vertices):
        points_x.append( (x_count*3) )
        points_y.append( y_count*3 )

        x_count += 1
        if (x_count > 6 ):
            y_count += 1
            x_count = 0

    #print("len points_x: " + str(len(points_x)))
    #print("len points_y: " + str(len(points_x)))
    #print("num_vertices: " + str(n_vertices))

    plot_count = 0
    for x in range(n_vertices):
        for y in range(n_vertices):     
            if ( x < y and matrix[x][y] > - 1):
                #draw the connection if it exists
                plt.plot([points_x[y], points_x[x]], [points_y[y], points_y[x]], color='b', marker = 'o')
                plot_count += 1

    #print("plot count: " + str(plot_count))
    #print("num_edges: " + str(num_edges))

    #plt.show()
    plt.savefig('graph.png')
    

#Function to create a bridge-graph with given parameters and save it
def make_bridge_graph(n_vertices, density, windy, output_file):

    if(n_vertices < 18):
        #print("ERROR, Minimum 18 vertices needed to construct graph.")
        return
    random.seed()

    #initialize NxN (N vertices) matrix to store graph representation
    matrix = []
    for x in range(n_vertices):
        row = []
        for y in range(n_vertices):
            if(x == y):
                row.append(0)
            else:
                #add an empty connection
                row.append(-1)                
        matrix.append(row)


    #Build the bridge layer by layer
    half_size = math.floor(n_vertices/2) #nodes in one half of bridge (all bridges created here are symmetric)

    num_layers = random.randint(3, 4) #number of layers in bridge half

    #print("num layers: " + str(num_layers))

    num_extra_nodes = half_size % num_layers

    layer_sizes = []
    #define size of layers
    for x in range(num_layers):
        layer_sizes.append(math.floor(half_size/num_layers))

    while num_extra_nodes > 0:
        layer_sizes[random.randint(0, num_layers - 1)] += 1
        num_extra_nodes -= 1

    layer_separations = []
    for x in range(num_layers - 1):
        layer_separations.append(random.randint(2, 5))



    num_layers_full = num_layers*2

    #print("num layers full: " + str(num_layers_full))
    layer_sizes_full = []
    for x in range(num_layers):
        layer_sizes_full.append(layer_sizes[x])
    for x in range(num_layers):
        layer_sizes_full.append(layer_sizes[num_layers - 1 - x])


    layer_separations_full = []
    for x in range(num_layers - 1):
        layer_separations_full.append(layer_separations[x])
    layer_separations_full.append(random.randint(2, 5))
    for x in range(num_layers - 1):
        layer_separations_full.append(layer_separations[len(layer_separations) - 1 - x])

    #print("num layer separations full: " + str(len(layer_separations_full)))


    max_layer_size = max(layer_sizes_full)

    #print("max layer size: " + str(max_layer_size))

    #duplicate layers to form full bridge
    full_vertices = []
    full_xs = []
    full_ys = []

    x_count = 0
    y_count = 0
    layer_count = 0
    for x in range(math.floor(n_vertices/2) * 2):
        full_vertices.append(x)

        if layer_sizes_full[layer_count] < max_layer_size:
            full_xs.append((x_count + 1)*2)
        else:
            full_xs.append((x_count)*2)

        full_ys.append(y_count)

        x_count += 1
        if x_count >= (layer_sizes_full[layer_count]):
            x_count = 0
            y_count += layer_separations_full[layer_count]
            layer_count += 1
            layer_count = layer_count % len(layer_separations_full)


    #Add the correct connections to the matrix
    num_edges = 0
    layer_count = 0
    x_count = 0
    for x in range(len(full_vertices)):
        #add all connections for each vertex

        #connection on this layer if it exists
        if(x_count < layer_sizes_full[layer_count] - 1 and x + 1 < len(full_vertices)):
            matrix[x][x + 1] = 2
            matrix[x + 1][x] = 2

            num_edges += 1

        #connections on upper layer if it exists
        if layer_count < num_layers_full - 1:
            #select all vertices I should connect to
            for y in range(len(full_vertices)):
                if y > x and full_ys[y] == full_ys[x] + layer_separations_full[layer_count] and abs(full_xs[y] - full_xs[x]) <= 2: # if I should connect
                    if( full_xs[y] == full_xs[x] ):
                        matrix[x][y] = layer_separations_full[layer_count]
                        num_edges += 1
                    elif layer_count != num_layers_full/2 - 1:
                        matrix[x][y] = layer_separations_full[layer_count] * math.sqrt(2)
                        num_edges += 1
                    if windy == False:
                        matrix[y][x] = matrix[x][y]
                    else:
                        if(layer_count < num_layers_full/2 - 1 and matrix[x][y] > 0):
                            matrix[x][y] *= 2
                            matrix[y][x] = matrix[x][y]/2.0
                        elif (layer_count > num_layers_full/2 - 1 and matrix[x][y] > 0):
                            matrix[y][x] = matrix[x][y]*2

                    

        x_count += 1
        if x_count >= (layer_sizes_full[layer_count]):
            x_count = 0
            layer_count += 1
            layer_count = layer_count % len(layer_sizes_full)

    #Save the produced graph in a .csv file
    with open(output_file, 'w') as o:
        for x in range(n_vertices):
            for y in range(n_vertices):
                if y != n_vertices - 1:
                    o.write(str(matrix[x][y]) + ",")
                else:
                    o.write(str(matrix[x][y]) + "\n")

        o.write("\n")
        for x in range(n_vertices):
            o.write(" , ")
        o.write("NUM_VERTICES: " + str(n_vertices) + ",")
        o.write(" , ")
        o.write("NUM_EDGES: " + str(num_edges) + "\n")

    #Draw visualization of graph and display
    points_x = full_xs #x, y coordinates of vertices
    points_y = full_ys

    #print("len points_x: " + str(len(points_x)))
    #print("len points_y: " + str(len(points_x)))
    #print("num_vertices: " + str(n_vertices))

    plot_count = 0
    for x in range(n_vertices):
        for y in range(n_vertices):     
            if ( x < y and matrix[x][y] > - 1):
                #draw the connection if it exists
                plt.plot([points_x[y], points_x[x]], [points_y[y], points_y[x]], color='b', marker = 'o')
                plot_count += 1

    #print("plot count: " + str(plot_count))
    #print("num_edges: " + str(num_edges))

    #plt.show()
    plt.savefig('graph.png')
    

#read arguments passed from command line
NUM_VERTICES = int(sys.argv[1])
DENSITY = float(sys.argv[2])
WINDY = str_to_bool(sys.argv[3])
MAKE_BRIDGE = str_to_bool(sys.argv[4])
OUTPUT_FILE = sys.argv[5]

#Handle bridge-graph and general graph cases separately
if(MAKE_BRIDGE == False):
    #create a general graph, without bridge constraints
    make_general_graph(NUM_VERTICES, DENSITY, WINDY, OUTPUT_FILE)

else:
    #creat a graph with bridge constraints
    make_bridge_graph(NUM_VERTICES, DENSITY, WINDY, OUTPUT_FILE)


