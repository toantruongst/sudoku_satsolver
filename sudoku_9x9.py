import pycosat
import math
import sys, getopt 
import time

# python sudoku.py -b/-c mt1
# b --> Binomal
# c --> Commander
# mt --> Sudoku maxtrix from 1 to 10

clauses = []
sudoku_size = 9;

def main(argv): 
    argument = '' 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "b:c",["mt1","mt2","mt3","mt4","mt5","mt6","mt7","mt8","mt9","mt10"])
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
        elif opt in ("-b","--mt3"):
            solve_problem(mt3, sudoku_size, 0) 
        elif opt in ("-c","--mt3"):
            solve_problem(mt3, sudoku_size, 1) 
        elif opt in ("-b","--mt4"):
            solve_problem(mt4, sudoku_size, 0)
        elif opt in ("-c","--mt4"):
            solve_problem(mt4, sudoku_size, 1)
        elif opt in ("-b","--mt5"):
            solve_problem(mt5, sudoku_size, 0) 
        elif opt in ("-c","--mt5"):
            solve_problem(mt5, sudoku_size, 1)
        elif opt in ("-b","--mt6"): 
            solve_problem(mt6, sudoku_size, 0)  
        elif opt in ("-c","--mt6"): 
            solve_problem(mt6, sudoku_size, 1)
        elif opt in ("-b","--mt7"): 
            solve_problem(mt7, sudoku_size, 0) 
        elif opt in ("-c","--mt7"): 
            solve_problem(mt7, sudoku_size, 1)
        elif opt in ("-b","--mt8"):
            solve_problem(mt8, sudoku_size, 0) 
        elif opt in ("-c","--mt8"):
            solve_problem(mt8, sudoku_size, 1)
        elif opt in ("-b","--mt9"):
            solve_problem(mt9, sudoku_size, 0) 
        elif opt in ("-c","--mt9"):
            solve_problem(mt9, sudoku_size, 1) 
        elif opt in ("-b","--mt10"):
            solve_problem(mt10, sudoku_size, 0)
        elif opt in ("-c","--mt10"):
            solve_problem(mt10, sudoku_size, 1)
        else:
            sys.exit()

def print_sudoku(problemset, size):
    box_size = int(math.sqrt(size))
    for d in range(len(problemset)):
        if d % box_size == 0 and d != 0:
            print("- - - - - - - - - - -")
        for c in range(len(problemset[0])):
            if c % box_size == 0 and c != 0:
                print("| ", end ="")
            if c == size-1:
                print(str(problemset[d][c]))
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
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
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

    mt1 =  [[2, 0, 0, 0, 5, 6, 1, 0, 9],
           [0, 6, 0, 8, 0, 1, 4, 0, 3],
           [3, 0, 8, 2, 0, 0, 0, 6, 7],
           [0, 4, 2, 5, 0, 7, 3, 9, 0],
           [1, 5, 9, 6, 2, 0, 0, 0, 0],
           [7, 0, 0, 0, 9, 8, 2, 0, 0],
           [0, 0, 0, 0, 0, 5, 0, 0, 0],
           [0, 0, 0, 9, 0, 4, 0, 0, 1],
           [0, 0, 3, 0, 0, 2, 0, 5, 0]]

        
    mt2 =  [[7, 1, 9, 0, 0, 3, 4, 0, 0],
           [0, 0, 8, 0, 7, 1, 0, 9, 0],
           [0, 0, 6, 4, 9, 0, 0, 0, 1],
           [1, 3, 0, 9, 0, 4, 2, 0, 0],
           [9, 8, 2, 0, 3, 7, 5, 4, 0],
           [0, 0, 0, 8, 2, 0, 0, 1, 0],
           [5, 0, 0, 3, 4, 6, 7, 0, 0],
           [0, 0, 7, 0, 0, 9, 0, 0, 4],
           [2, 4, 3, 7, 1, 0, 0, 0, 0]]


    mt3 =  [[7, 0, 3, 0, 4, 0, 0, 6, 0],
           [0, 0, 8, 7, 3, 0, 0, 0, 9],
           [0, 2, 0, 0, 0, 0, 3, 0, 0],
           [8, 3, 0, 9, 0, 0, 6, 0, 0],
           [0, 7, 2, 0, 0, 0, 0, 8, 1],
           [6, 0, 0, 5, 0, 8, 4, 3, 0],
           [0, 5, 0, 2, 0, 0, 0, 0, 3],
           [0, 4, 6, 8, 0, 7, 0, 2, 0],
           [2, 0, 0, 4, 0, 0, 0, 9, 0]]


    mt4 =  [[0, 7, 8, 1, 4, 3, 9, 0, 2],
           [0, 9, 3, 0, 0, 8, 0, 0, 1],
           [0, 1, 0, 0, 0, 9, 0, 0, 0],
           [0, 0, 7, 0, 1, 6, 0, 8, 0],
           [0, 0, 2, 9, 7, 5, 0, 0, 6],
           [0, 0, 0, 0, 0, 2, 0, 0, 7],
           [0, 0, 9, 0, 2, 0, 6, 3, 0],
           [1, 3, 6, 8, 0, 4, 0, 2, 5],
           [8, 2, 0, 0, 3, 7, 0, 4, 0]] 
    
    mt5 =  [[4, 0, 0, 7, 5, 8, 9, 2, 0],
           [0, 6, 0, 0, 0, 2, 7, 3, 0],
           [2, 7, 8, 6, 0, 9, 5, 1, 0],
           [0, 0, 3, 0, 6, 0, 4, 0, 2],
           [0, 0, 4, 0, 2, 0, 0, 0, 0],
           [8, 2, 6, 0, 9, 0, 1, 0, 0],
           [0, 4, 0, 3, 8, 1, 0, 0, 7],
           [0, 1, 0, 0, 0, 5, 3, 8, 9],
           [0, 0, 5, 9, 0, 6, 2, 0, 0]]

    mt6 =  [[8, 0, 0, 0, 4, 6, 0, 9, 0],
           [7, 0, 0, 0, 9, 0, 6, 0, 0],
           [0, 9, 0, 7, 1, 5, 0, 8, 0],
           [0, 0, 7, 0, 5, 0, 8, 6, 0],
           [5, 8, 4, 6, 3, 7, 2, 1, 9],
           [6, 0, 0, 9, 8, 2, 4, 7, 5],
           [0, 6, 0, 5, 7, 0, 9, 0, 0],
           [1, 7, 0, 8, 2, 3, 0, 0, 6],
           [3, 5, 8, 0, 0, 0, 1, 0, 0]]

        
    mt7 =  [[7, 0, 0, 8, 3, 5, 9, 6, 0],
           [3, 0, 1, 7, 0, 9, 5, 0, 0],
           [0, 0, 5, 4, 6, 0, 7, 0, 0],
           [6, 0, 2, 9, 0, 7, 0, 3, 8],
           [4, 0, 8, 0, 1, 0, 2, 0, 0],
           [0, 9, 0, 2, 4, 8, 6, 0, 7],
           [0, 0, 0, 1, 9, 6, 0, 0, 2],
           [0, 0, 0, 5, 0, 2, 8, 4, 6],
           [0, 0, 0, 0, 0, 0, 0, 7, 9]]


    mt8 =  [[4, 0, 1, 0, 0, 5, 0, 0, 0],
           [3, 0, 0, 0, 0, 4, 6, 0, 8],
           [0, 0, 8, 1, 3, 2, 4, 5, 7],
           [1, 2, 0, 0, 5, 8, 7, 9, 6],
           [9, 0, 0, 0, 0, 7, 0, 4, 0],
           [8, 0, 0, 0, 0, 0, 0, 0, 0],
           [5, 1, 0, 0, 0, 0, 0, 8, 4],
           [7, 4, 0, 0, 0, 0, 2, 0, 3],
           [2, 0, 3, 4, 0, 0, 5, 7, 0]]


    mt9 =  [[0, 8, 0, 3, 9, 0, 2, 5, 0],
           [4, 0, 0, 0, 0, 0, 1, 9, 0],
           [6, 0, 5, 0, 0, 4, 3, 0, 7],
           [0, 0, 8, 0, 0, 0, 0, 0, 1],
           [9, 1, 4, 0, 0, 3, 7, 0, 5],
           [0, 3, 6, 0, 0, 9, 8, 4, 2],
           [3, 6, 7, 0, 4, 0, 5, 2, 8],
           [0, 0, 0, 0, 0, 2, 4, 1, 3],
           [0, 0, 2, 0, 3, 0, 6, 0, 0]] 
    
    mt10 = [[0, 0, 3, 2, 0, 6, 5, 0, 0],
           [0, 8, 2, 5, 7, 3, 4, 1, 6],
           [0, 0, 1, 0, 8, 4, 7, 2, 3],
           [0, 1, 5, 0, 4, 0, 0, 8, 0],
           [0, 0, 0, 0, 6, 1, 0, 0, 0],
           [8, 0, 0, 0, 2, 0, 0, 4, 0],
           [2, 9, 8, 6, 5, 7, 0, 0, 4],
           [1, 5, 0, 4, 0, 0, 2, 0, 9],
           [0, 3, 6, 1, 0, 0, 8, 0, 0]]
    
    if(len(sys.argv[1:]) == 0):
        print('Argument error, Please try again')
    else:
        main(sys.argv[1:])