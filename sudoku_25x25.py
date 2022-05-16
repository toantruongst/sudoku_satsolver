import pycosat
import math
import sys, getopt 
import time

# python sudoku.py -b/-c mt1
# b --> Binomal
# c --> Commander
# mt --> Sudoku maxtrix from 1 to 2

clauses = []
sudoku_size = 25;

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
            print("-- -- -- -- --   -- -- -- -- --   -- -- -- -- --   -- -- -- -- --   -- -- -- -- --")
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
    for i in 1, 6, 11, 16, 21:
        for j in 1, 6, 11, 16, 21:
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

    mt1 =   [[7, 11, 15, 5, 10, 6, 3, 0, 17, 0, 19, 9, 8, 2, 23, 0, 0, 13, 0, 1, 0, 0, 25, 14, 12], 
            [22, 0,18, 0, 19, 23, 0, 4, 0, 11, 0, 0, 0, 0, 0, 15, 0, 8, 17, 6, 0, 0, 0, 13, 0], 
            [12, 0, 0, 24, 13, 0, 0, 0, 5, 0, 0, 0, 0, 6, 0, 0, 19, 0, 18, 10, 15, 11, 7, 17, 20], 
            [17, 3, 0, 6, 20, 0, 21, 14, 0, 0, 16, 11, 4, 0, 18, 24, 0, 25, 0, 5, 0, 0, 23, 2, 9], 
            [23, 16, 25, 8, 2, 1, 0, 20, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [9, 0, 6, 11, 0, 0, 22, 0, 24, 25, 0, 0, 7, 0, 0, 8, 3, 0, 5, 13, 0, 15, 17, 0, 19], 
            [0, 0, 0, 0, 0, 0, 0, 3, 7, 0, 0, 0, 6, 17, 13, 0, 0, 0, 0, 0, 0, 0, 0, 21, 24], 
            [4, 0, 7, 10, 12, 11, 0, 0, 19, 0, 3, 0, 0, 0, 0, 0, 15, 16, 0, 0, 0, 0, 0, 0, 0], 
            [16, 0, 8, 0, 0, 5, 6, 13, 14, 0, 0, 0, 0, 18, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 11], 
            [0, 0, 0, 0, 0, 2, 12, 15, 9, 16, 0, 0, 23, 11, 19, 18, 0, 6, 0, 17, 0, 0, 8, 10, 0], 
            [8, 0, 11, 0, 7, 3, 15, 17, 0, 0, 0, 5, 0, 0, 0, 21, 0, 1, 12, 18, 20, 6, 0, 24, 0], 
            [1, 0, 16, 0, 18, 0, 9, 0, 2, 7, 13, 6, 11, 0, 0, 0, 23, 20, 0, 22, 8, 0, 0, 12, 15], 
            [10, 24, 0, 0, 0, 0, 0, 6, 0, 0, 17, 0, 18, 20, 0, 13, 25, 2, 0, 0, 5, 4, 0, 19, 22], 
            [13, 9, 0, 2, 22, 14, 11, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 3, 7, 0, 16, 1, 0], 
            [0, 23, 4, 21, 0, 12, 5, 8, 0, 13, 0, 16, 25, 0, 0, 0, 7,0, 0, 0, 0, 0, 0, 0, 0], 
            [25, 0, 23, 0, 0, 10, 0, 12, 0, 5, 0, 17, 0, 4, 0, 0, 8, 0, 2, 9, 14, 18, 0, 0, 0], 
            [0, 6, 0, 13, 0, 18, 4, 0, 11, 20, 0, 0, 9, 0, 0, 0, 17, 0, 0, 12, 23, 0, 0, 0, 0], 
            [14, 0, 9, 4, 0, 25, 13, 0, 1, 0, 18, 19, 0, 3, 5, 22, 6, 0, 0, 0, 11, 0, 2, 15, 0], 
            [0, 20, 0, 0, 8, 0, 19, 24, 6, 0, 21, 0, 22, 10, 0, 5, 18, 0, 25, 23, 17, 0, 0, 0, 4], 
            [21, 0, 0, 0, 0, 0, 14, 0, 0, 17, 11, 23, 24, 25, 0, 1, 0, 10, 13, 4, 9, 5, 0, 7, 0], 
            [0, 0, 0, 16, 9, 21, 25, 11, 0, 12, 8, 0, 0, 14, 0, 0, 13, 24, 0, 0, 0, 0, 18, 22, 7], 
            [18, 0, 0, 0, 25, 22, 24, 19, 16, 0, 9, 4, 0, 0, 0, 7, 0, 0, 0, 2, 0, 20, 0, 8, 3], 
            [6, 0, 22, 19, 0, 17, 0, 0, 15, 3, 0, 2, 1, 13, 0, 25, 0, 0, 8, 0, 0, 10, 0, 0, 0], 
            [0, 0, 14, 0, 0, 0, 0, 1, 10, 6, 25, 7, 16, 0, 17, 3, 0, 11, 0, 20, 19, 0, 0, 5, 2], 
            [20, 0, 5, 3, 4, 9, 0, 0, 0, 0, 0, 0, 0, 24, 22, 17, 10, 0, 0, 21, 13, 1, 0, 11, 25]]




        
    mt2 =   [[2, 0, 0, 12, 3, 8, 11, 0, 13, 17, 0, 22, 23, 0, 25, 18, 0, 21, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 15, 1, 6, 7, 9, 0, 0, 24, 0, 3, 25, 0, 0, 2, 0, 0, 0],
            [0, 18, 0, 19, 0, 0, 0, 0, 7, 6, 13, 16, 0, 17, 0, 11, 15, 22, 23, 12, 0, 0, 25, 0, 0],
            [0, 0, 0, 22, 0, 0, 21, 23, 9, 0, 3, 0, 0, 11, 0, 1, 4, 0, 0, 8, 0, 0, 13, 0, 0],
            [25, 21, 7, 0, 17, 0, 0, 0, 0, 0, 1, 2, 4, 0, 15, 6, 13, 0, 0, 10, 0, 5, 0, 0, 12],
            [0, 6, 0, 9, 19, 24, 0, 0, 25, 0, 23, 0, 0, 0, 11, 0, 0, 0, 4, 22, 8, 13, 0, 20, 15],
            [1, 0, 18, 17, 0, 0, 0, 3, 20, 0, 0, 15, 16, 9, 0, 0, 11, 0, 0, 0, 14, 19, 0, 21, 4],
            [0, 0, 0, 21, 0, 0, 17, 0, 2, 19, 0, 6, 10, 0, 8, 0, 5, 12, 13, 15, 0, 18, 0, 0, 0],
            [12, 14, 0, 0, 0, 5, 0, 0, 8, 23, 0, 0, 0, 0, 18, 16, 6, 0,20, 0, 0, 11, 0, 2, 17],
            [13, 23, 5, 25, 0, 15, 4, 0, 10, 0, 19, 17, 0, 0, 0, 0, 14, 0, 0, 21, 7, 0, 24, 9, 0],
            [0, 0, 14, 15, 5, 0, 2, 0, 16, 9, 17, 0, 6, 0, 10, 0, 0, 0, 12, 3, 0, 4, 11, 8, 0],
            [0, 0, 0, 4, 0, 23, 0, 0, 0, 0, 5, 19, 0, 20, 9, 0, 0, 0, 0, 1, 0, 0, 21, 13, 0],
            [9, 2, 19, 0, 0, 0, 0, 0, 0, 4, 0, 0, 25, 0, 13, 0, 23, 15, 24, 0, 18, 7, 0, 0, 16],
            [3, 0, 0, 24, 0, 0, 0, 0, 0, 0, 2, 0, 1, 15, 4,0, 18, 16, 0, 0, 17, 0, 0, 0, 0],
            [0, 1, 10, 11, 12, 17, 0, 0, 0, 22, 0, 18, 3, 16,24, 0, 9, 0, 5, 7, 2, 0, 0, 23, 25],
            [0, 10, 0, 0, 0, 13, 0, 24, 17, 0, 7, 0, 15, 0, 22, 20, 12, 0, 9, 18, 0, 0, 16, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 16, 0, 8, 18, 0, 13, 0, 23, 0, 0, 25, 0, 0, 0, 20, 0, 3, 0],
            [0, 7, 21, 1, 0, 0, 0, 15, 0, 10, 9, 20, 0, 0, 0, 4, 0, 0, 0, 19, 0, 23, 0, 14, 0],
            [17, 19, 22, 0, 20, 4, 7, 12, 14, 0, 0, 10, 0, 25, 1, 15, 0, 13, 16, 23, 5, 24, 0, 0, 9],
            [0, 25, 0, 3, 23, 0, 0, 9, 5, 20, 0, 0, 0, 8, 0, 0, 22, 11, 0, 2, 0, 10, 15, 12, 0],
            [20, 0, 0, 14, 0, 9, 0, 0, 3, 15, 11, 0, 5, 10, 7, 0, 0, 6, 0, 0, 23, 8, 0, 16, 21],
            [21, 0, 0, 0, 0, 25, 0, 6, 23, 14, 0, 0, 24, 0, 0, 12, 16, 18, 1, 4, 19, 3, 0, 15, 0],
            [22, 15, 25, 0, 6, 0, 0, 0, 0, 16, 0, 0, 0, 14, 19, 23, 21, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 17, 0, 16, 7, 18, 0, 2, 1, 5, 15, 13, 21, 0, 0, 22, 0, 0, 8, 9, 25, 0, 20, 10, 11],
            [0, 24, 13, 0, 9, 11, 0, 0, 0, 21, 16, 1, 0, 23, 3, 25, 10, 7, 0, 20, 0, 0, 0, 0, 0]]
    
    if(len(sys.argv[1:]) == 0):
        print('Argument error, Please try again')
    else:
        main(sys.argv[1:])