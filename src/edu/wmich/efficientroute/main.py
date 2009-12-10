#! /usr/bin/env python
# coding: utf-8

'''
Created on Dec 1, 2009

@author: changwang
'''
from edu.wmich.efficientroute.utils import *
from edu.wmich.efficientroute.datastructure import Network

import random

def random_run(num):
    print "The input site number is %d" % num
    print
    network = Network()
    m = create_matrix(num)
    
    mat = m[1]
    
#    print "**********************************"
#    print "Original (K-1) x (K-1) matrix is: "
#    for row in mat:
#        print row
#    print "**********************************"
#    print 
    
    indexes = []
    
    if m[0] == True:
        indexes = m[2]
        mat = substitute_all_dash(mat, num, indexes)
#        print "**********************************"
#        print "Dash substituted (K-1) x (K-1) matrix is: "
#        for row in mat:
#            print row
#        print "**********************************"
#        print
    
    sets = set_factory(mat)
    
#    print "**********************************"
#    print "Constructed Maekawa set is: "
#    formatter(sets)
#    print "**********************************"
#    print 
    
    network.nodes = assign_set(sets)
    
#    print "**********************************"
#    print "The final graph is: "
#    for i in network.nodes:
#        print i
#    print 
#    print "There are: " + str(compute_links(sets)) + " links between " + str(len(network.nodes)) + " communication sets"
#    print "**********************************"
    
    communication_cost = 0
    random.seed()
    for i in range(20):
        source = random.randint(1, num)
        dest = random.randint(1, num)
        while dest == source:
            dest = random.randint(1, num)
        print 'From source site %s to destination site %s' % (str(source), str(dest))
        print 'selected route is: '
        route = route_selector(network.getNode(source), network.getNode(dest))
        communication_cost = communication_cost + len(route)
        route_printer(route)
        print 
    print 'Total communication cost is: %d' % communication_cost
    

if __name__ == '__main__':
    random_run(9)
    #random_run(13)
