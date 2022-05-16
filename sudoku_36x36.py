import pycosat
import math
import sys, getopt 
import time

# python sudoku.py -b/-c mt1
# b --> Binomal
# c --> Commander
# mt --> Sudoku maxtrix from 1 to 2

clauses = []
sudoku_size = 36;

def main(argv): 
    argument = '' 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "b:c",["mt1","mt2"])
    except getopt.GetoptError:
        sys.exit()
    
    for opt, arg in opts: 
        if opt in ("-b","--mt1"): 
            solve_problem(mt1, sudoku_size, 0) 
        elif opt in ("-c","--mt1"): 
            solve_problem(mt1, sudoku_size, 1)
        elif opt in ("-b","--mt2"): 
            solve_problem(mt2, sudoku_size, 0)
        elif opt in ("-c","--mt2"): 
            solve_problem(mt2, sudoku_size, 1)
        else:
            sys.exit()
            
def print_sudoku(problemset, size):
    box_size = int(math.sqrt(size))
    for d in range(len(problemset)):
        if d % box_size == 0 and d != 0:
            print("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")
        for c in range(len(problemset[0])):
            if c % box_size == 0 and c != 0:
                print("| ", end ="")
            if c == size-1:
                if(problemset[d][c]<10):
                    print("0"+str(problemset[d][c]))
                else:
                    print(str(problemset[d][c]))
            else:
                if(problemset[d][c]<10):
                    print("0"+str(problemset[d][c]) + " ", end = "")
                else:
                    print(str(problemset[d][c]) + " ", end = "")
                


def solve_problem(problemset, size, bi_co):
    print('Problem:') 
    print_sudoku(problemset,sudoku_size) 
    solve(problemset, size, bi_co) 
    print('Answer:')
    print_sudoku(problemset,sudoku_size)   

# Caculate Index    
def v(i, j, d, size): 
    return size*size * (i - 1) + size * (j - 1) + d

def Cmdexactone(vari, group):
    num_clause = 0
    # Divide elements in vari to groups
    number_of_item_in_group = len(vari) // len(group)
    if len(vari) % len(group):
        number_of_item_in_group += 1

    group_array = [[vari[0]]]

    for i in range(1, len(vari)):
        if i % number_of_item_in_group == 0:
            group_array.append([])
        group_array[i // number_of_item_in_group].append(vari[i])

    # ALO for commander
    clauses.append(group)
    num_clause += 1

    # AMO for commander
    for i in range(len(group) - 1):
        for j in range(i + 1, len(group)):
            clauses.append([-group[i], -group[j]])
            num_clause += 1
    
    if len(group_array) != len(group):
        return False

    # Iterate through each group
    for i in range(len(group_array)):
        # ALO if commander var true
        current_group = list(group_array[i])
        current_group.append(-group[i])
        clauses.append(current_group)
        num_clause += 1

        for j in range(len(group_array[i])):
            if j < len(group_array[i]) - 1:
                for k in range(j + 1, len(group_array[i])):
                    # AMO if commander var true
                    clauses.append([-group[i], -group_array[i][j], -group_array[i][k]])
                    num_clause += 1

            # If commander var false
            clauses.append([group[i], -group_array[i][j]])
            num_clause += 1
    return num_clause


def commander_clauses(size): 
    res = []
    group_quantity = int(math.sqrt(size))
    box_size = int(math.sqrt(size))
    # Commander temporary group variables index
    group_v = int(math.pow(size, 3)) + 1
    num_clause = 0
    # for all cells, ensure that the each cell contains only one number:
    for i in range(size):
        for j in range(size):
            var_list = []
            for k in range(1, size + 1):
                var_list.append(i*int(math.pow(size, 2)) + j*size + k)
            group_list = []
            for k in range(group_quantity):
                group_list.append(group_v + k)
            num_clause += Cmdexactone(var_list, group_list)
            group_v += group_quantity
            #print(group_v)

    # ensure row have distinct values
    for i in range(size):
        for k in range(1, size + 1):
            var_list = []
            for j in range(size):
                var_list.append(i*int(math.pow(size, 2)) + j*size + k)
            group_list = []
            for j in range(group_quantity):
                group_list.append(group_v + j)
            num_clause += Cmdexactone(var_list, group_list)
            group_v += group_quantity

    # ensure columns have distinct values
    for j in range(size):
        for k in range(1, size + 1):
            var_list = []
            for i in range(size):
                var_list.append(i*int(math.pow(size, 2)) + j*size + k)
            group_list = []
            for i in range(group_quantity):
                group_list.append(group_v + i)
            num_clause += Cmdexactone(var_list, group_list)
            group_v += group_quantity

    # ensure sub-grids(3x3,4x4,...) "regions" have distinct values
    for k in range(1, size + 1):
        for a in range(box_size):
            for b in range(box_size):
                var_list = []
                for i in range(box_size):
                    for j in range(box_size):
                        var_list.append((a*box_size+i)*int(math.pow(size, 2)) + (b*box_size+j)*size + k)
                group_list = []
                for i in range(group_quantity):
                    group_list.append(group_v + i)
                num_clause += Cmdexactone(var_list, group_list)
                group_v += group_quantity

    return num_clause

#Reduces Sudoku problem to a SAT clauses 
def binomal_clauses(size): 
    res = []
    box_size = int(math.sqrt(size))

    # for all cells, ensure that the each cell:
    for i in range(1, size+1):
        for j in range(1, size+1):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d, size) for d in range(1, size+1)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, size+1):
                for dp in range(d + 1, size+1):
                    res.append([-v(i, j, d, size), -v(i, j, dp, size)])

    def valid(cells): 
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, size+1):
                        res.append([-v(xi[0], xi[1], d, size), -v(xj[0], xj[1], d, size)])

    # ensure rows and columns have distinct values
    for i in range(1, size+1):
        valid([(i, j) for j in range(1, size+1)])
        valid([(j, i) for j in range(1, size+1)])
        
    # ensure sub-grids(3x3,4x4,...) "regions" have distinct values
    for i in 1, 7, 13, 19, 25, 31:
        for j in 1, 7, 13, 19, 25, 31:
            valid([(i + k % box_size, j + k // box_size) for k in range(size)])
    return res

def solve(grid,size,bi_co):
    #solve a Sudoku problem
    if bi_co == 0:
        sudoku_clauses = binomal_clauses(size)
        numclause = len(sudoku_clauses)
    else:
        sudoku_clauses = clauses
        numclause = commander_clauses(size)
    for i in range(1, size+1):
        for j in range(1, size+1):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal). 
            if d:
                sudoku_clauses.append([v(i, j, d, size)])
    
    # Print number SAT clause  
    print("P CNF " + str(numclause) +"(number of clauses)")
    
    # solve the SAT problem
    start = time.time()
    sol = set(pycosat.solve(sudoku_clauses))
    end = time.time()
    print("Time: "+str(end - start))
    
    def read_cell(i, j):
        # return the digit of cell i, j according to the solution
        for d in range(1, size+1):
            if v(i, j, d, size) in sol:
                return d

    for i in range(1, size+1):
        for j in range(1, size+1):
            grid[i - 1][j - 1] = read_cell(i, j)


if __name__ == '__main__':
    from pprint import pprint

    mt1 =   [[22,8,30,0,2,0,6,23,7,0,0,33,0,0,24,0,0,14,25,13,36,0,19,5,0,16,0,26,0,20,0,1,0,9,31,28],
            [0,0,7,35,0,0,0,27,24,18,29,0,25,13,36,32,0,0,0,16,34,0,15,20,0,0,11,9,31,0,0,0,10,2,21,0],
            [0,0,0,18,29,0,0,0,36,0,19,0,3,16,34,0,0,0,17,0,0,9,0,0,8,0,0,0,0,22,0,0,35,0,33,0],
            [25,13,36,32,19,5,0,16,0,0,15,20,0,1,11,9,0,28,0,30,10,2,0,22,23,7,0,0,33,6,27,24,18,29,14,12],
            [3,0,34,0,0,0,0,1,11,9,0,28,8,30,0,0,21,22,0,0,0,0,0,6,27,24,0,29,14,12,0,36,32,19,5,25],
            [17,1,0,0,31,28,8,30,10,2,21,0,23,0,35,4,0,6,0,24,18,0,0,12,0,36,32,19,0,25,0,34,0,15,0,3],
            [0,30,0,0,0,0,0,0,35,0,33,6,27,24,18,0,0,0,13,0,32,0,0,25,16,34,26,15,20,0,0,11,9,31,28,17],
            [0,7,0,4,33,6,0,24,0,29,0,0,13,0,32,19,5,0,0,0,0,15,20,3,0,0,0,31,0,17,30,10,2,0,0,8],
            [27,0,18,29,0,12,0,36,32,19,5,25,0,0,0,15,20,0,0,11,0,0,28,0,0,0,0,21,22,8,7,0,0,33,0,0],
            [0,36,32,19,5,25,16,34,26,0,20,3,1,0,9,31,0,0,30,10,2,21,0,8,7,0,0,33,0,0,0,18,29,14,12,0],
            [0,0,26,15,20,3,0,11,9,0,28,0,30,10,2,0,22,0,0,0,0,33,6,23,0,0,29,14,0,27,36,32,19,5,0,13],
            [1,0,0,0,0,0,30,0,0,21,0,8,0,35,4,33,0,23,24,18,29,14,0,27,0,32,0,5,0,13,34,0,15,0,0,16],
            [10,2,0,22,8,30,35,0,33,0,0,7,18,29,14,12,27,24,0,19,0,0,0,36,26,15,0,3,16,34,0,31,28,0,1,11],
            [35,4,33,0,0,0,0,0,14,12,0,0,0,0,5,0,13,36,26,0,0,0,16,34,0,31,28,17,1,11,2,0,0,0,30,10],
            [18,29,14,12,27,24,0,19,0,25,13,0,26,0,0,0,0,0,9,31,0,17,0,11,2,0,22,8,30,0,4,0,6,0,7,0],
            [0,19,5,0,13,0,26,15,20,0,0,34,0,0,0,17,1,11,2,21,22,8,0,0,0,0,6,0,0,0,29,0,12,27,24,0],
            [0,15,20,3,0,34,9,0,28,0,1,0,0,21,0,0,0,10,4,0,6,23,7,35,29,0,12,27,24,0,19,5,25,13,0,32],
            [9,0,28,17,1,11,2,21,0,8,30,10,4,33,6,0,0,35,29,14,0,27,24,0,19,0,25,0,0,0,15,0,3,16,34,26],
            [0,6,0,7,0,4,14,0,27,24,0,0,5,25,13,0,32,0,20,3,0,34,26,0,0,0,1,11,9,31,0,8,0,10,2,0],
            [0,25,13,36,0,0,0,3,16,34,0,0,0,17,1,11,9,31,22,8,0,0,2,21,0,23,0,35,0,33,12,0,24,0,0,14],
            [14,12,27,0,18,29,0,0,13,0,32,19,0,3,16,0,26,15,0,17,0,11,0,0,0,8,30,10,0,21,0,23,7,0,4,33],
            [21,0,0,0,0,0,0,6,23,0,35,0,14,12,0,0,18,0,5,25,13,0,32,0,0,3,0,34,0,0,28,17,1,0,9,31],
            [20,0,0,34,26,15,0,17,0,11,9,0,22,8,0,10,0,21,6,23,0,35,0,0,0,0,24,18,29,0,25,0,36,32,0,5],
            [28,17,0,11,0,0,22,0,30,10,2,0,6,23,0,0,0,0,12,27,24,0,0,14,0,0,0,0,19,5,0,16,34,26,0,0],
            [2,0,22,0,0,0,4,0,0,23,7,35,0,14,0,0,0,0,0,5,25,0,36,32,0,20,3,16,0,0,31,0,0,1,11,0],
            [4,0,6,23,7,35,29,0,12,27,0,18,19,0,25,13,0,32,15,20,3,16,0,0,0,0,17,0,11,0,0,22,0,30,0,2],
            [0,0,0,13,36,0,0,20,3,16,0,0,31,28,0,1,0,9,0,22,8,0,10,2,33,0,23,0,35,0,14,12,27,24,18,0],
            [0,14,0,0,24,18,19,0,25,0,36,32,15,20,3,16,34,26,31,28,0,1,11,9,21,0,0,30,0,2,33,6,23,7,35,4],
            [0,20,0,0,34,26,0,28,0,1,0,9,21,22,8,0,0,2,33,6,23,0,35,4,14,0,27,24,18,29,0,0,0,36,0,0],
            [0,28,17,0,0,9,0,0,8,30,10,2,0,6,0,7,35,0,0,0,27,0,0,0,0,0,13,36,32,0,20,3,0,0,26,15],
            [0,10,0,21,22,8,7,0,0,33,0,23,24,18,0,14,12,27,0,0,19,5,0,0,34,26,15,20,3,16,11,9,0,0,17,0],
            [0,0,4,33,0,23,24,18,0,0,12,27,0,0,0,0,25,13,34,26,15,20,3,0,11,9,0,28,0,0,0,2,0,22,8,30],
            [0,18,29,0,12,0,36,32,0,5,25,13,0,0,0,20,3,0,0,9,31,0,17,1,10,0,21,0,0,30,0,0,0,6,0,7],
            [0,0,19,5,25,13,0,26,15,20,3,0,0,9,31,28,0,0,0,0,21,0,8,30,0,0,33,6,23,0,18,0,14,0,27,0],
            [34,26,0,20,3,16,11,0,31,28,17,1,10,0,21,22,8,30,35,0,33,0,23,0,0,29,14,0,27,24,0,19,5,25,0,36],
            [11,0,31,28,0,0,10,2,21,22,8,30,35,0,33,6,23,7,18,0,0,12,27,24,32,0,0,0,13,36,26,0,0,0,16,0]]
        
    mt2 =   [[36,8,24,20,0,12,0,18,4,0,28,25,0,1,0,6,11,14,30,0,19,31,13,0,9,0,5,0,0,16,3,0,0,0,0,23],
            [0,18,4,0,0,0,2,1,17,6,0,14,0,10,0,0,0,21,0,35,5,0,33,16,0,34,27,3,15,23,8,0,0,0,0,36],
            [2,1,0,6,0,0,30,10,19,31,0,21,32,0,0,9,33,16,3,34,0,29,15,0,22,0,0,0,12,36,18,0,7,28,0,26],
            [30,10,19,31,13,0,32,0,0,9,0,16,3,34,27,29,0,0,0,0,20,0,0,36,28,4,7,18,25,0,1,17,6,11,0,0],
            [32,35,0,9,33,16,3,0,27,29,0,0,8,24,20,22,12,0,18,4,0,28,25,26,0,17,0,1,0,0,10,0,31,0,21,0],
            [0,34,0,29,0,23,8,24,0,22,0,36,18,4,0,28,25,0,0,0,6,0,14,0,13,19,0,10,21,30,35,5,9,0,0,0],
            [0,20,0,12,0,8,0,7,0,0,26,0,17,0,11,14,2,1,0,0,0,21,0,10,16,0,0,0,0,0,0,29,15,0,0,0],
            [0,0,28,25,26,18,17,0,0,0,2,0,0,0,13,0,0,0,0,9,33,0,0,35,0,29,15,0,0,34,20,0,0,36,0,24],
            [17,0,0,0,2,1,0,31,0,0,30,0,0,9,33,16,0,0,27,29,0,0,0,0,0,0,12,0,8,24,7,0,0,26,18,4],
            [19,31,13,21,30,10,5,9,0,16,32,35,27,0,0,0,3,0,20,0,12,36,8,24,0,0,0,7,0,0,6,11,0,0,0,17],
            [0,9,33,16,32,0,0,29,0,23,3,34,0,22,0,36,8,24,7,28,25,0,0,4,0,0,14,0,0,0,31,13,21,0,0,19],
            [27,29,0,23,0,34,20,22,12,36,8,0,7,28,25,0,0,4,6,11,14,2,0,17,0,13,0,0,0,19,0,33,16,0,0,0],
            [8,0,0,22,12,36,0,0,0,28,25,26,0,17,0,0,0,2,10,19,31,0,0,30,33,5,9,35,16,32,34,27,29,15,23,3],
            [0,4,0,28,0,0,1,17,6,11,14,0,0,19,0,13,21,0,35,5,0,33,0,32,15,27,29,0,0,0,0,20,22,12,0,8],
            [0,17,6,0,0,0,0,19,0,13,21,30,35,5,9,33,0,32,34,0,0,15,23,0,12,0,22,0,0,8,0,0,28,0,26,0],
            [10,0,0,13,0,30,0,5,9,33,0,32,0,0,29,0,23,3,24,20,0,0,36,8,25,0,0,0,0,18,0,0,0,0,2,0],
            [35,0,9,33,16,0,0,27,29,0,0,3,24,0,22,12,0,0,4,0,0,25,26,0,0,6,0,17,2,1,0,0,13,21,30,10],
            [34,27,29,15,23,3,24,20,22,0,0,8,4,0,28,0,26,0,0,0,11,14,2,0,0,0,13,19,30,0,5,0,0,16,0,35],
            [20,0,12,36,0,0,7,0,0,0,18,0,6,0,0,2,1,0,31,13,21,0,0,0,32,33,16,9,35,5,29,15,23,3,34,27],
            [7,0,25,0,0,4,0,11,0,2,0,17,31,0,21,0,0,19,0,33,16,32,35,5,3,0,23,29,0,0,0,0,36,8,24,0],
            [6,0,0,2,0,17,0,0,21,30,10,0,9,33,0,0,35,5,0,0,23,3,0,27,8,0,36,22,24,0,28,0,26,18,4,7],
            [31,0,21,30,10,0,9,0,16,0,35,0,29,15,23,3,34,27,22,0,36,0,24,20,0,0,0,28,0,7,11,14,2,0,17,6],
            [9,0,16,32,0,5,0,0,0,3,34,27,22,12,0,8,0,0,0,25,0,18,0,0,1,0,2,11,0,6,13,0,0,0,0,31],
            [29,0,23,3,34,27,22,12,0,8,24,20,0,25,26,18,4,0,11,14,2,1,0,6,0,0,30,0,19,31,33,0,0,35,5,0],
            [0,0,36,0,24,0,0,25,26,18,0,0,11,0,0,1,0,6,0,0,30,10,0,31,0,16,32,0,5,9,15,23,3,34,27,0],
            [28,0,0,0,4,7,0,14,2,1,0,6,0,21,30,10,19,31,0,0,32,0,5,9,34,23,0,15,0,0,12,0,8,24,0,22],
            [11,14,0,0,0,0,0,21,0,10,19,0,33,0,32,35,5,0,15,23,3,34,27,0,24,0,0,0,20,0,25,26,0,0,7,0],
            [33,0,32,35,0,0,15,0,0,0,27,29,12,36,0,24,20,0,25,26,18,0,7,28,17,2,1,14,6,0,21,30,10,0,0,13],
            [15,23,3,34,27,0,0,0,0,0,20,0,0,26,18,0,7,0,14,2,0,17,6,0,0,0,0,0,31,0,16,32,35,0,0,33],
            [13,21,30,10,19,31,33,16,0,0,5,9,0,23,3,34,0,0,12,36,8,24,20,0,4,26,18,25,7,28,0,0,1,17,0,0],
            [0,36,0,24,20,0,0,26,0,4,7,28,14,2,1,17,0,0,21,0,10,0,31,13,0,32,0,16,9,33,0,3,0,27,29,15],
            [25,26,0,0,0,0,14,0,0,17,6,11,21,30,0,0,0,13,0,32,0,5,0,33,27,0,34,0,29,0,0,8,24,20,22,0],
            [0,2,1,0,0,11,21,30,10,19,31,0,16,0,35,0,9,0,0,0,34,27,29,0,0,8,0,36,0,12,0,18,4,0,28,0],
            [0,0,10,19,31,13,16,32,0,5,0,0,0,0,34,0,0,0,0,8,0,0,22,12,7,18,4,26,0,25,2,1,17,0,11,0],
            [0,32,35,5,9,0,23,0,34,27,29,15,0,0,24,20,22,0,26,18,0,7,0,0,0,1,17,2,11,0,0,10,19,0,13,21],
            [0,0,0,27,29,0,36,8,24,20,22,12,26,18,0,7,0,25,2,1,0,6,11,14,0,10,19,30,0,21,32,35,5,9,33,16]]
    
    if(len(sys.argv[1:]) == 0):
        print('Argument error, Please try again')
    else:
        main(sys.argv[1:])