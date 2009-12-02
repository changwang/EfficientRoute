'''
Created on Dec 1, 2009

@author: changwang
'''
import unittest
from edu.wmich.efficientroute.utils import matrix, set_factory

class Test(unittest.TestCase):


    def testMatrix(self):
        self.assertEqual(matrix(7), (False, [[4, 5], [6, 7]]))
        self.assertEqual(matrix(8), (True, [[5, 6, 7], [8, '_', '_'], ['_', '_', '_']]))
        self.assertEqual(matrix(13), (False, [[5, 6, 7], [8, 9, 10], [11, 12, 13]]))

    def testSetFactory(self):
        #self.assertEqual(set_factory(matrix(7)[1]), 
        #                 ([[1, 2, 3], [1, 4, 5], [1, 6, 7]], [[2, 4, 6], [2, 5, 7]], [[3, 4, 7], [3, 5, 6]]))
        self.assertEqual(set_factory(matrix(13)[1]), 
                         ([[1, 2, 3, 4], [1, 5, 6, 7], [1, 8, 9, 10], [1, 11, 12, 13]], 
                          [[2, 5, 8, 11], [2, 6, 9, 12], [2, 7, 10, 13]], 
                          [[3, 5, 9, 13], [3, 6, 10, 11], [3, 7, 8, 12]],
                          [[4, 5, 10, 12], [4, 7, 9, 11], [4, 6, 8, 13]]))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMatrix']
    unittest.main()