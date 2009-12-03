'''
Created on Dec 1, 2009

@author: changwang
'''
import math

from edu.wmich.efficientroute.datastructure import Node

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
        
    for l in range(1, K):
        for i in range(K):        
            diagonal = []
            diagonal.append(l+2)    
            for j in range(K):
                diagonal.append(matrix[j][(i+j*l) % K])
            diagonals.append(diagonal)
    
    del row, column, diagonal
    return (rows, columns, diagonals)

def assign_set(sets):
    K = len(sets[0]) - 1
    nodes = []
    
    node_1 = Node(sets[0][0][0])
    node_1.communication_set = sets[0][0]
    nodes.append(node_1)
    
    # assign the rows
    for i in sets[0][1:]:
        n = Node(i[1])
        n.communication_set = i
        if n in nodes:
            continue
        nodes.append(n)
        
    # assign the columns
    node_2 = Node(sets[1][0][0])
    node_2.communication_set = sets[1][0]
    nodes.append(node_2)
    
    for i in sets[1][1:]:
        n = Node(i[1])
        n.communication_set = i
        if n in nodes:
            continue
        nodes.append(n)
        
    # assign the diagonals
    count = 0
    loop = 0
    for i in sets[2]:
        loop += 1
        n = Node(i[count + 2])
        n.communication_set = i
        if n in nodes:
            n = Node(i[0])
            n.communication_set = i
        nodes.append(n)
        if (loop % K) == 0:
            count += 1
        
    return nodes

def formatter(sets):
    # print row first
    rows = sets[0]
    for row in rows:
        print row
        
    # print column then
    columns = sets[1]
    for column in columns:
        print column
        
    # print diagonals finally
    diagonals = sets[2]
    for diagonal in diagonals:
        print diagonal