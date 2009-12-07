'''
Created on Dec 1, 2009

@author: changwang
'''
from edu.wmich.efficientroute.utils import *

if __name__ == '__main__':
    m = matrix(9)

    mat = m[1]
    print mat

    indeces = []
    
    if m[0] == True:
        indeces = m[2]
    while indeces:
        tmp = indeces.pop()
        t = substitute_dash(m[1], 9, tmp)
        mat[tmp[0]][tmp[1]] = t
    
    sets = set_factory(mat)
    print compute_links(sets)
    
    print assign_set(sets)
