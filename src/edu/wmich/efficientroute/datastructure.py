'''
Created on Dec 1, 2009

@author: changwang
'''
class Node:
    ''' 
        Represents the node in network.
        Each node may contains a communication set,
        which includes the nodes that are all in the same communication set.
     '''
    def __init__(self, value):
        self.communication_set = []
        self.value = value # actual value node contains

    def __eq__(self, other):
        ''' This method is used to handle whether two nodes are equal,
        like node1 == node2.
        Actually, if the value in node is the same, two nodes are the same. '''
        return self.value == other.value
    
    def __ne__(self, other):
        ''' This method is used to handle wheter two nodes are not equal,
        like node1 != node2 or node1 <> node2.
        Acutally, if the value in node is not the same, two nodes are different. '''
        return self.value != other.value
    
    def __repr__(self):
        ''' This method is used to help debug, 
        which give the console a readable information. '''
        return 'Node: ' + str(self.value)