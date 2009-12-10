#! /usr/bin/env python
# coding: utf-8

'''
Created on Dec 1, 2009

@author: changwang
'''

import unittest
from edu.wmich.efficientroute.utils import create_matrix, set_factory, assign_set, compute_links, best_site, route_selector
from edu.wmich.efficientroute.datastructure import Node, Network

class Test(unittest.TestCase):

    def setUp(self):
        self.matrix_7 = create_matrix(7)
        self.matrix_13 = create_matrix(13)
        self.matrix_9 = create_matrix(9)
        
        self.sets_7 = set_factory(self.matrix_7[1])
        self.sets_13 = set_factory(self.matrix_13[1])
        self.sets_9 = set_factory(self.matrix_9[1])
        
        self.network_7 = Network()
        self.network_7.nodes = assign_set(self.sets_7)
        
        self.network_13 = Network()
        self.network_13.nodes = assign_set(self.sets_13)
        
        self.network_9 = Network()
        self.network_9.nodes = assign_set(self.sets_9)

    def testMatrix(self):
        self.assertEqual(self.matrix_7, (False, [[4, 5], [6, 7]], []))
        self.assertEqual(create_matrix(8), (True, [[5, 6, 7], [8, '_', '_'], ['_', '_', '_']], [(1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]))
        self.assertEqual(self.matrix_13, (False, [[5, 6, 7], [8, 9, 10], [11, 12, 13]], []))
        
    def testReversedMatrix(self):
        #self.assertEqual(reversed(self.matrix_7[1]), [[6, 7], [4, 5]])
        it = reversed(self.matrix_7[1])
        self.assertEqual(it.next(), [6, 7])
        self.assertEqual(it.next(), [4, 5])
        #self.assertEqual(it.next(), '')

    def testSetFactory(self):
        self.assertEqual(self.sets_7,
                         ([[1, 2, 3], [1, 4, 5], [1, 6, 7]], 
                          [[2, 4, 6], [2, 5, 7]], 
                          [[3, 4, 7], [3, 5, 6]]))
        
        self.assertEqual(set_factory(create_matrix(6)[1]),
                         ([[1, 2, 3], [1, 4, 5], [1, 6, '_']],
                         [[2, 4, 6], [2, 5, '_']],
                         [[3, 4, '_'], [3, 5, 6]]))
        
        self.assertEqual(self.sets_13, 
                         ([[1, 2, 3, 4], [1, 5, 6, 7], [1, 8, 9, 10], [1, 11, 12, 13]], 
                          [[2, 5, 8, 11], [2, 6, 9, 12], [2, 7, 10, 13]], 
                          [[3, 5, 9, 13], [3, 6, 10, 11], [3, 7, 8, 12],
                          [4, 5, 10, 12], [4, 6, 8, 13], [4, 7, 9, 11]]))
        
        self.assertEqual((set_factory(create_matrix(12)[1])),
                         ([[1, 2, 3, 4], [1, 5, 6, 7], [1, 8, 9, 10], [1, 11, 12, '_']],
                          [[2, 5, 8, 11], [2, 6, 9, 12], [2, 7, 10, '_']],
                          [[3, 5, 9, '_'], [3, 6, 10, 11], [3, 7, 8, 12],
                           [4, 5, 10, 12], [4, 6, 8, '_'], [4, 7, 9, 11]]))
        
        self.assertEqual(set_factory(create_matrix(21)[1]),
                         ([[1, 2, 3, 4, 5], [1, 6, 7, 8, 9], [1, 10, 11, 12, 13], [1, 14, 15, 16, 17], [1, 18, 19, 20, 21]],
                          [[2, 6, 10, 14, 18], [2, 7, 11, 15, 19], [2, 8, 12, 16, 20], [2, 9, 13, 17, 21]],
                          [[3, 6, 11, 16, 21], [3, 7, 12, 17, 18], [3, 8, 13, 14, 19], [3, 9, 10, 15, 20],
                           [4, 6, 12, 14, 20], [4, 7, 13, 15, 21], [4, 8, 10, 16, 18], [4, 9, 11, 17, 19],
                           [5, 6, 13, 16, 19], [5, 7, 10, 17, 20], [5, 8, 11, 14, 21], [5, 9, 12, 15, 18]]))
        
        self.assertEqual(set_factory(create_matrix(19)[1]),
                         ([[1, 2, 3, 4, 5], [1, 6, 7, 8, 9], [1, 10, 11, 12, 13], [1, 14, 15, 16, 17], [1, 18, 19, '_', '_']],
                          [[2, 6, 10, 14, 18], [2, 7, 11, 15, 19], [2, 8, 12, 16, '_'], [2, 9, 13, 17, '_']],
                          [[3, 6, 11, 16, '_'], [3, 7, 12, 17, 18], [3, 8, 13, 14, 19], [3, 9, 10, 15, '_'],
                           [4, 6, 12, 14, '_'], [4, 7, 13, 15, '_'], [4, 8, 10, 16, 18], [4, 9, 11, 17, 19],
                           [5, 6, 13, 16, 19], [5, 7, 10, 17, '_'], [5, 8, 11, 14, '_'], [5, 9, 12, 15, 18]]))
        
    def testAssignSet7(self):
        nodes_7 = []
        node_7_1 = Node(1)
        node_7_1.communication_set = [1, 2, 3]
        nodes_7.append(node_7_1)
        
        node_7_4 = Node(4)
        node_7_4.communication_set = [1, 4, 5]
        nodes_7.append(node_7_4)
        
        node_7_6 = Node(6)
        node_7_6.communication_set = [1, 6, 7]
        nodes_7.append(node_7_6)
        
        node_7_2 = Node(2)
        node_7_2.communication_set = [2, 4, 6]
        nodes_7.append(node_7_2)
        
        node_7_5 = Node(5)
        node_7_5.communication_set = [2, 5, 7]
        nodes_7.append(node_7_5)
        
        node_7_7 = Node(7)
        node_7_7.communication_set = [3, 4, 7]
        nodes_7.append(node_7_7)
        
        node_7_3 = Node(3)
        node_7_3.communication_set = [3, 5, 6]
        nodes_7.append(node_7_3)
        
        self.assertEqual(assign_set(self.sets_7), nodes_7)
        
#    def testAssignSet6(self):
#        nodes_6 = []
#        node_6_1 = Node(1)
#        node_6_1.communication_set = [1, 2, 3]
#        nodes_6.append(node_6_1)
#        
#        node_6_4 = Node(4)
#        node_6_4.communication_set = [1, 4, 5]
#        nodes_6.append(node_6_4)
#        
#        node_6_6 = Node(6)
#        node_6_6.communication_set = [1, 6, 7]
#        nodes_6.append(node_6_6)
#        
#        node_6_2 = Node(2)
#        node_6_2.communication_set = [2, 4, 6]
#        nodes_6.append(node_6_2)
#        
#        node_6_5 = Node(5)
#        node_6_5.communication_set = [2, 5, 7]
#        nodes_6.append(node_6_5)
#        
#        node_6_7 = Node(7)
#        node_6_7.communication_set = [3, 4, 7]
#        nodes_6.append(node_6_7)
#        
#        node_6_3 = Node(3)
#        node_6_3.communication_set = [3, 5, 6]
#        nodes_6.append(node_6_3)
#        
#        self.assertEqual(assign_set(set_factory(matrix(6)[1])), nodes_6)
#        
    def testAssignSet13(self):
        
        nodes_13 = []
        node_13_1 = Node(1)
        node_13_1.communication_set = [1, 2, 3, 4]
        nodes_13.append(node_13_1)
        
        node_13_5 = Node(5)
        node_13_5.communication_set = [1, 5, 6, 7]
        nodes_13.append(node_13_5)
        
        node_13_8 = Node(8)
        node_13_8.communication_set = [1, 8, 9, 10]
        nodes_13.append(node_13_8)
        
        node_13_11 = Node(11)
        node_13_11.communication_set = [1, 11, 12, 13]
        nodes_13.append(node_13_11)
        
        node_13_2 = Node(2)
        node_13_2.communication_set = [2, 5, 8, 11]
        nodes_13.append(node_13_2)
        
        node_13_6 = Node(6)
        node_13_6.communication_set = [2, 6, 9, 12]
        nodes_13.append(node_13_6)
        
        node_13_7 = Node(7)
        node_13_7.communication_set = [2, 7, 10, 13]
        nodes_13.append(node_13_7)
        
        node_13_9 = Node(9)
        node_13_9.communication_set = [3, 5, 9, 13]
        nodes_13.append(node_13_9)
        
        node_13_10 = Node(10)
        node_13_10.communication_set = [3, 6, 10, 11]
        nodes_13.append(node_13_10)
        
        node_13_3 = Node(3)
        node_13_3.communication_set = [3, 6, 10, 11]
        nodes_13.append(node_13_3)
        
        node_13_12 = Node(12)
        node_13_12.communication_set = [4, 5, 10, 12]
        nodes_13.append(node_13_12)
        
        node_13_13 = Node(13)
        node_13_13.communication_set = [4, 6, 8, 13]
        nodes_13.append(node_13_13)
        
        node_13_4 = Node(4)
        node_13_13.communication_set = [4, 7, 9, 11]
        nodes_13.append(node_13_4)
        
        self.assertEqual(assign_set(self.sets_13), nodes_13)
        
    def testSetLength(self):
        self.assertEqual(len(assign_set(self.sets_7)), 7)
        self.assertEqual(len(assign_set(self.sets_13)), 13)
        
    def testComputeLinks(self):
        self.assertEqual(compute_links(set_factory(create_matrix(7)[1])), 14)
        #self.assertEqual(compute_links(set_factory(matrix(6)[1])), 10)
        #self.assertEqual(compute_links(set_factory(matrix(7)[1])), 14)
        #self.assertEqual(compute_links(set_factory(matrix(13)[1])), 39)
    
    def testSubstituteDash(self):
        #self.assertEqual(best_site(matrix(5)[1], 5), '')
        self.assertEqual(best_site(create_matrix(10)[1], 10, (2, 2)), 3)
    
    def testRouteSelector(self):
        self.assertEqual(route_selector(self.network_7.getNode(3), self.network_7.getNode(7)), [3, 7])
        self.assertEqual(route_selector(self.network_7.getNode(4), self.network_7.getNode(6)), [4, 1, 6])
        self.assertEqual(route_selector(self.network_7.getNode(1), self.network_7.getNode(7)), [1, 3, 7])
        self.assertEqual(route_selector(self.network_7.getNode(5), self.network_7.getNode(6)), [5, 7, 6])
        
        self.assertEqual(route_selector(self.network_13.getNode(1), self.network_13.getNode(4)), [1, 4])
        self.assertEqual(route_selector(self.network_13.getNode(11), self.network_13.getNode(13)), [11, 13])
        self.assertEqual(route_selector(self.network_13.getNode(2), self.network_13.getNode(12)), [2, 5, 12])
        self.assertEqual(route_selector(self.network_13.getNode(7), self.network_13.getNode(8)), [7, 10, 8])
        
        self.assertEqual(route_selector(self.network_9.getNode(1), self.network_9.getNode(1)), [1])
    
    def tearDown(self):
        del self.matrix_7
        del self.matrix_13
        del self.matrix_9
        del self.sets_7
        del self.sets_13
        del self.sets_9
        del self.network_13
        del self.network_7
        del self.network_9
    
if __name__ == "__main__":
    unittest.main()