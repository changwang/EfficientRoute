'''
Created on Dec 1, 2009

@author: changwang
'''
import math

def matrix(num):
    ''' num is the number of input nodes. '''
    matrix = []
    K = int(math.ceil(math.sqrt(num)))
    L = K * (K-1) + 1
    
    if (L < num):
        K = K + 1
    
    sub = []
    flag = False
    element_count = (K-1) * (K-1)
    for i in range(1, element_count+1):
        if (i + K) > num:
            sub.append('_')
            flag = True
        else:
            sub.append((i+K))
        if (i % (K-1)) == 0:
            matrix.append(sub)
            sub = []
    
    return (flag, matrix)

def set_factory(matrix):
    K = len(matrix[0])
    rows = []
    columns = []
    diagonals = []
    
    row = []
    column = []
    diagonal = []
    
    for i in range(1, K+2):
        row.append(i)
    rows.append(row)
    
    for i in range(K):
        row = []
        row.append(1)
        row.extend(matrix[i])
        rows.append(row)
    
    for i in range(K):
        column = []
        column.append(2)
        for j in range(K):            
            column.append(matrix[j][i])
        columns.append(column)
        
    for l in range(K-1):
        for i in range(K):        
            diagonal = []
            diagonal.append(l+3)    
            for j in range(K):
                diagonal.append(matrix[j][(i+j+2 * l) % K])
            diagonals.append(diagonal)
        
    return (rows, columns, diagonals)
