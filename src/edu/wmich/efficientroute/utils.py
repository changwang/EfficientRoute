#! /usr/bin/env python
# coding: utf-8

'''
Created on Dec 1, 2009

@author: changwang
'''
import math

from edu.wmich.efficientroute.datastructure import Node

def create_matrix(num):
    ''' Create a matrix based on the input number;
        num is the number of input nodes. '''
    # the final matrix, use list to store the number inside.
    matrix = []
    # This is a tricky part here, if num can not be represented by K*(K-1) + 1,
    # we'll introduce "dash" to fill the empty cell in matrix,
    # and record the index in dash_indexes for further usage.
    dash_indexes = []
    
    K = int(math.ceil(math.sqrt(num)))
    L = K * (K-1) + 1
    if (L < num):
        K = K + 1
    
    row = []
    flag = False
    element_count = (K-1) * (K-1)
    for i in range(1, element_count+1):
        if (i + K) > num:
            # if num is less than L, insert "dash".
            row.append('_')
            
            # calculate indexes of the dash.
            fir_index = 0
            sec_index = 0
            if (i % (K-1)) == 0:
                fir_index = i / (K - 1) - 1
                sec_index = K - 2
            else:
                fir_index = i / (K - 1)
                sec_index = (i % (K -1)) - 1
            dash_indexes.append((fir_index, sec_index))
            flag = True
        else:
            # otherwise insert current value into matrix
            row.append((i+K))
        
        if (i % (K-1)) == 0:
            matrix.append(row)
            # empty the row for next loop
            row = []
    
    # return a tuple containing dash indicator, matrix and dash_indexes.
    return (flag, matrix, dash_indexes)

def set_factory(matrix):
    ''' One core method, to produce the communication sets from input matrix. '''
    K = len(matrix[0])
    row, column, diagonal = [], [], []
    rows, columns, diagonals = [], [], []
    
    # Insert first K numbers into communication sets.
    for i in range(1, K+2):
        row.append(i)
    rows.append(row)
    
    # Create communication sets based on rows.
    for i in range(K):
        row = []
        row.append(1)
        row.extend(matrix[i])
        rows.append(row)
    
    # Create communication sets based on columns.
    for i in range(K):
        column = []
        column.append(2)
        for j in range(K):            
            column.append(matrix[j][i])
        columns.append(column)
        
    # Create communication sets based on diagonals.
    for jump in range(1, K):
        for i in range(K):        
            diagonal = []
            diagonal.append(jump+2)    
            for j in range(K):
                diagonal.append(matrix[j][(i+j*jump) % K])
            diagonals.append(diagonal)
    
    del row, column, diagonal
    return (rows, columns, diagonals)

def compute_links(sets):
    ''' Core method, compute the set links. '''
    K = len(sets[0]) - 1
    # use map to store the result, and the format is: 
    # NodeValue : [connected Nodes]
    # i.e. 2 : [1, 4, 5] means site 2 connects to site 1, site 4 and site 5. 
    link_map = {}
    
    node_1 = sets[0][0][0]
    tmp = sets[0][0][:]
    tmp.remove(node_1)
    link_map[node_1] = unique_list(tmp)
    del node_1
    
    # compute the rows
    for i in sets[0][1:]:
        n = i[1]
        if n in link_map or n == '_':
            # if n already exists in link_map or n is a dash,
            # ignore it, because it doesn'value contribute links.
            continue
        tmp = i[:]
        tmp.remove(n)
        link_map[n] = unique_list(tmp)
        
    # compute the columns
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
        
    # compute the diagonals
    jump = 0
    loop = 0
    for i in sets[2]:
        loop += 1
        n = i[jump + 2]
        if n == '_':
            continue
        if n in link_map:
            for value in i:
                if value not in link_map:
                    # check whether any node in current set is not in the link_map,
                    # if it is, use it.
                    n = value
                    tmp = i[:]
                    tmp.remove(n)
                    link_map[n] = unique_list(tmp)
                    break
            else:
                # otherwise use the default one, and update its communication set.
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
            # finishing one round, jump increases 1.
            jump += 1
    
    count_pool = []
    for key in link_map:
        # calculate how many links does each site have.
        if key == '_':
            continue
        if '_' in link_map[key]:
            # dash doesn't contribute links, remove it from list.
            link_map[key].remove('_')
        
        # for convenience, represent each item like this: [number of links, site number]
        # because I need to sort it by number of links, and fetch the minimum one.
        for value in link_map[key]:
            tmp = [key, value]
            tmp.sort()
            if tmp not in count_pool:
                count_pool.append(tmp)
            
#    print link_map
#    print count_pool
#    print len(count_pool)
    return len(count_pool)

def best_site(matrix, N, indexes):
    ''' Substitute one dash by each site once a time,
        calculate the communication links,
        return the site number with the minimum links between communication sets.
    '''
    map = {}
    
    for i in range(1, N + 1):
        # substitute dash by site
        matrix[indexes[0]][indexes[1]] = i
        # assign the set on the fly
        s = set_factory(matrix)
        # compute links by the generated sets
        map[i] = compute_links(s)
#    print map
    
    tmp = [[v[1], v[0]] for v in map.items()]
    tmp.sort()
    #print tmp
    return tmp[0][1]

def substitute_all_dash(matrix, N, indexes_list):
    while indexes_list:
        indexes = indexes_list.pop()
        bs = best_site(matrix, N, indexes)
        matrix[indexes[0]][indexes[1]] = bs
    return matrix

def assign_set(sets):
    ''' Core method, assign the communication set to the appropriate site.
        refer to report for detail. '''
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
        if n in nodes:
            continue
        # Lazy attachment, in order to save the memory,
        # if site is not in the list, attaching the neighbour sites.
        tmp = i[:]
        tmp.remove(i[1])
        n.communication_set = unique_list(tmp)
        nodes.append(n)
        
    # assign the columns
    node_2 = Node(sets[1][0][0])
    tmp = sets[1][0][:]
    tmp.remove(sets[1][0][0])
    node_2.communication_set = unique_list(tmp)
    nodes.append(node_2)
    
    for i in sets[1][1:]:
        n = Node(i[1])
        if n in nodes:
            continue
        tmp = i[:]
        tmp.remove(i[1])
        n.communication_set = unique_list(tmp)
        nodes.append(n)
        
    # assign the diagonals
    jump = 0
    loop = 0
    for i in sets[2]:
        loop += 1
        n = Node(i[jump + 2])
        if n in nodes:
            for t in i:
                no = Node(t)
                if no not in nodes:
                    tmp = i[:]
                    tmp.remove(t)
                    no.communication_set = unique_list(tmp)
                    nodes.append(no)
                    break
            else:
                o_index = nodes.index(n)
                origin = nodes[o_index]
                tmp = i[:]
                tmp.remove(n.value)
                origin.communication_set = unique_list(origin.communication_set + tmp)
        else:
            tmp = i[:]
            tmp.remove(i[jump + 2])
            n.communication_set = unique_list(tmp)
            nodes.append(n)
        if (loop % K) == 0:
            jump += 1
        
    return nodes

def unique_list(li):
    ''' Use set to remove duplicated items in list.'''
    s = set(li)
    return list(s)

def route_selector(source, dest):
    ''' Route strategy is very simple due to the properties of communication sets.
        1) Check the communication set belongs to source site, 
            whether the dest site is in the communication set,
            if it is, directly establish connection between source and dest sites; otherwise
        2) Check the communication set belongs to dest site,
            whether the source site is in this communication set,
            if it is, directly establish connection between source and dest sites; otherwise
        3) Get the intersectional site from communication set belongs to source site 
            and communication set belongs to dest site. '''
    route = []
    route.append(source.value)
    if source == dest:
        return route
    # check communication set belongs to source site.
    s_comm = source.communication_set
    d_comm = dest.communication_set
    if dest.value in s_comm or source.value in d_comm:
        route.append(dest.value)
    else:
        # a speedy way to find the intersect
        # simply, I just need first one.
        route.append([x for x in s_comm if x in d_comm][0])
        route.append(dest.value)
    
    return route

def formatter(sets):
    ''' print out the in put sets with a readable format. '''
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
        
def route_printer(route):
    ''' print out the selected route. '''
    print " ➙ ".join(str(v) for v in route)