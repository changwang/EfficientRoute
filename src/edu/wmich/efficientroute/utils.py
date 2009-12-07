'''
Created on Dec 1, 2009

@author: changwang
'''
import math

from edu.wmich.efficientroute.datastructure import Node

def matrix(num):
    ''' num is the number of input nodes. '''
    matrix = []
    dash_indece = []
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
            fir_index = 0
            sec_index = 0
            if (i % (K-1)) == 0:
                fir_index = i / (K - 1) - 1
                sec_index = K - 2
            else:
                fir_index = i / (K - 1)
                sec_index = (i % (K -1)) - 1
            dash_indece.append((fir_index, sec_index))
            flag = True
        else:
            sub.append((i+K))
        if (i % (K-1)) == 0:
            matrix.append(sub)
            sub = []
    
    return (flag, matrix, dash_indece)

def set_factory(matrix):
    K = len(matrix[0])
    row, column, diagonal = [], [], []
    rows, columns, diagonals = [], [], []
    
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

def compute_links(sets):
    K = len(sets[0]) - 1
    link_map = {}
    
    node_1 = sets[0][0][0]
    tmp = sets[0][0][:]
    tmp.remove(node_1)
    link_map[node_1] = unique_list(tmp)
    
    # assign the rows
    for i in sets[0][1:]:
        n = i[1]
        if n in link_map or n == '_':
            continue
        tmp = i[:]
        tmp.remove(n)
        link_map[n] = unique_list(tmp)
        
    # assign the columns
    node_2 = sets[1][0][0]
    tmp = sets[1][0][:]
    tmp.remove(node_2)
    link_map[node_2] = unique_list(tmp)
    
    for i in sets[1][1:]:
        n = i[1]
        if n in link_map or n == '_':
            continue
        tmp = i[:]
        tmp.remove(n)
        link_map[n] = unique_list(tmp)
        
    # assign the diagonals
    count = 0
    loop = 0
    for i in sets[2]:
        loop += 1
        n = i[count + 2]
        if n == '_':
            continue
        if n in link_map:
            #n = i[0]
            for t in i:
                if t not in link_map:
                    n = t
                    tmp = i[:]
                    tmp.remove(n)
                    link_map[n] = unique_list(tmp)
                    break
            else:
                tmp = i[:]
                tmp.remove(n)
                link_map[n].extend(tmp)
                tmp = link_map[n]
                link_map[n] = unique_list(tmp)
        else:
            tmp = i[:]
            tmp.remove(n)
            link_map[n] = unique_list(tmp)
        
        if (loop % K) == 0:
            count += 1
    
    count_pool = []
    for key in link_map:
        if key == '_':
            continue
        if '_' in link_map[key]:
            link_map[key].remove('_')
        #count = count + len(link_map[key])
        for value in link_map[key]:
            tmp = [key, value]
            tmp.sort()
            if tmp not in count_pool:
                count_pool.append(tmp)
            
    print link_map
    print count_pool
    print len(count_pool)
    return len(count_pool)

def substitute_dash(matrix, N, indeces):
    map = {}
    
    for i in range(1, N + 1):
        matrix[indeces[0]][indeces[1]] = i
        s = set_factory(matrix)
        map[i] = compute_links(s)
    print map
    
    tmp = [[v[1], v[0]] for v in map.items()]
    tmp.sort()
    print tmp
    return tmp[0][1]

def assign_set(sets):
    K = len(sets[0]) - 1
    nodes = []
    
    node_1 = Node(sets[0][0][0])
    tmp = sets[0][0][:]
    tmp.remove(sets[0][0][0])
    node_1.communication_set = unique_list(tmp)
    nodes.append(node_1)
    
    # assign the rows
    for i in sets[0][1:]:
        n = Node(i[1])
        tmp = i[:]
        tmp.remove(i[1])
        n.communication_set = unique_list(tmp)
        if n in nodes:
            continue
        nodes.append(n)
        
    # assign the columns
    node_2 = Node(sets[1][0][0])
    tmp = sets[1][0][:]
    tmp.remove(sets[1][0][0])
    node_2.communication_set = unique_list(tmp)
    nodes.append(node_2)
    
    for i in sets[1][1:]:
        n = Node(i[1])
        tmp = i[:]
        tmp.remove(i[1])
        n.communication_set = unique_list(tmp)
        if n in nodes:
            continue
        nodes.append(n)
        
    # assign the diagonals
    count = 0
    loop = 0
    for i in sets[2]:
        loop += 1
        n = Node(i[count + 2])
        tmp = i[:]
        tmp.remove(i[count + 2])
        n.communication_set = unique_list(tmp)
        if n in nodes:
            for t in i:
                no = Node(t)
                tmp = i[:]
                tmp.remove(t)
                no.communication_set = unique_list(tmp)
                if no not in nodes:
                    nodes.append(no)
                    break
            else:
                o_index = nodes.index(n)
                origin = nodes[o_index]
                origin.communication_set = unique_list(origin.communication_set + n.communication_set)
        else:
            nodes.append(n)
        if (loop % K) == 0:
            count += 1
        
    return nodes

def unique_list(li):
    s = set(li)
    return list(s)


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