"""
Square class: Represents a square in the Stackdoku grid
    i,j: The Square knows it's position in the grid
    num: The number of the square, if it is known.  Will be "?" if it is not yet known.  '/' for blank
    possibilitites: an array of answers that are still possible for this square
    dim: The dimension of the board (5 for 1-3 stackoku, 6 for 1-4 stackoku)
    b: A link back to the board that contains this square
"""
class Square:
    
    #__init__
    #
    # initializes the square
    #
    # i, j: the position in the board
    # dim: the dimension of the board
    # num: the starting number of the board (usually "?")
    # b: Link back to the board
    def __init__(self, i, j, dim, num, b):
        self.i = i
        self.j = j
        self.num = num
        self.dim = dim
        if (self.num == "?"):
            self.possibilities = ['/'] + list(range(1, self.dim-1))
        else:
            self.possibilities = [num]
        self.b = b
    
    #remove_possibility
    #
    # Removes an answer from the list of possibilities
    #
    # num: the answer to remove
    def remove_possibility(self, num):
        if (num in self.possibilities):
            b.changed=True
            self.possibilities.remove(num)
        if len(self.possibilities)==1:
            b.changed=True
            self.num = self.possibilities[0]
   
    # remove_possbilities_by_row
    #
    # Looks at the squares on the row and removes a possibility for this square if there 
    # is a square of that number in this row, or 2 spaces
    def remove_possbilities_by_row (self):
        if (self.num != "?"): return
        space_count = 0
        for k in list(range (0, self.j)) + list(range(self.j+1,self.dim)):
            num_found = self.b.a[self.i][k].num
            if num_found=='/': 
                space_count+=1
                if space_count==2:
                    self.remove_possibility('/')
            elif (num_found in self.possibilities):
                self.remove_possibility(num_found)

    # remove_possbilities_by_column
    #
    # Looks at the squares on the column and removes a possibility for this square if there 
    # is a square of that number in this column, or 2 spaces   
    def remove_possbilities_by_column (self):
        if (self.num != "?"): return
        space_count = 0
        for k in list(range (0, self.i)) + list(range(self.i+1,self.dim)):
           num_found = self.b.a[k][self.j].num
           if num_found=='/': 
                space_count+=1
                if space_count==2:
                    self.remove_possibility('/')
           elif (num_found in self.possibilities):
               self.remove_possibility(num_found)

    # check_above
    #
    # Looks at the square above and removes any possibilities greater than that number
    def check_above(self):
        if self.i > 0: 
            num_above = self.b.a[self.i-1][self.j].num
            possbilities = self.possibilities.copy()
            for p in possbilities:
                if isinstance(p, int) and isinstance(num_above, int):
                    if p >= num_above:
                        self.remove_possibility(p)
                        
    # check_below
    #
    # Looks at the square below and removes any possibilities less than that number
    def check_below(self):
        if self.i < self.dim-1: 
            num_above = self.b.a[self.i+1][self.j].num
            possbilities = self.possibilities.copy()
            for p in possbilities:
                if isinstance(p, int) and isinstance(num_above, int):
                    if p <= num_above:
                        self.remove_possibility(p)


    # check unique_row
    #
    # Look at all the possibilties and if it is the only number in this row, then it must be the answer for this square
    def check_unique_row(self):
        for p in self.possibilities:
            found = False
            for k in list(range (0, self.j)) + list(range(self.j+1,self.dim)):
                if p in self.b.a[self.i][k].possibilities:
                    found = True
            if (not found):
                self.set_me(p)
                
    # check unique_row
    #
    # Look at all the possibilties and if it is the only number in this column, then it must be the answer for this square
    def check_unique_column(self):
        for p in self.possibilities:
            found = False
            for k in list(range (0, self.i)) + list(range(self.i+1,self.dim)):
                if p in self.b.a[k][self.j].possibilities:
                    found = True
            if (not found):
                self.set_me(p)
    
    # am_i_a_probem
    #
    # Return True if either the square below is greater than me or the square above is less than me
    def am_i_a_problem(self):
        if (self.num=="?" or self.num=='/'): return False
        if (self.i > 0):
            num_above = self.b.a[self.i-1][self.j].num
            if (isinstance(num_above, int) and num_above <= self.num): return True
        if (self.i < self.dim-1):
            num_below = self.b.a[self.i+1][self.j].num
            if (isinstance(num_below, int) and num_below >= self.num): return True        
        return False
       
    # set_me
    #
    # sets the square to a number.  Also, removes other possibilities and sets the board to changed          
    def set_me(self, num):
        if (self.num != "?"): return
        if (self.num != num):
            b.changed=True
        self.num = num
        self.possibilities = [num]
 
    
"""
Board class: Represents a grid of squares

    a: The Array of Squares
    dim: The dimension of the board (5 for 1-3 stackoku, 6 for 1-4 stackoku)
    changed: The state of the board.  It knows if it's been changed on the last run through
"""    
class Board:

    # __init__
    #
    # initialize a grid
    # dim: the dimension of the board
    # boardstr: optional string to fill in the board for initial input
    def __init__(self, dim, boardstr=""):
        self.a = []
        self.dim = dim
        self.changed=False
        
        for i in range (0, self.dim):
            self.a.append([])
            for j in range (0, self.dim):
                self.a[i].append(Square(i, j, self.dim, "?", self))
        for i,s in enumerate(boardstr):
            if (s != "?"):
                self.a[i//self.dim][i % self.dim].set_me(int(s))  

    # print_board
    #
    # used to print the board
    def print_board(self, indent):
        mystr = indent
        for i in range (0, self.dim):
            for j in range (0, self.dim):
                mystr += "|" + str(self.a[i][j].num) + "|"
            mystr += "\n" + indent
        print (mystr)   
    
    # __eq__
    #
    # returns true if all nums and possibilities are the same for both boards
    #
    # other: the board to compare to
    def __eq__(self, other):
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                os = other.a[i][j]
                ss = self.a[i][j]
                if os.num != ss.num or os.possibilities != ss.possibilities:
                    print ("false yo")
                    return False
        return True
    
    # copy
    #
    # copies the other board onto me
    #
    # other: the copy of the board
    def copy (self, other):
        self.a = []
        self.dim = other.dim
        self.changed=True
        for i in range (0, self.dim):
            self.a.append([])
            for j in range (0, self.dim):
                self.a[i].append(Square(i, j, self.dim, other.a[i][j].num, self))

    # print_possibilities
    #
    # prints possibilties for debugging
    def print_possibilities(self):
        mystr = ""
        for i in range (0, self.dim):
            for j in range (0, self.dim):
                mystr += str(self.a[i][j].possibilities) + "|"
            mystr += "\n"
        print (mystr) 
    
    #set_square
    def set_square(self, i, j, v):
        self.a[i][j].set_me (v)
    
    # simple_check
    #
    # does the simple check of looking at each square, then checking it's row and column and the value above and below
    # does nothing hypothetical
    def simple_check(self):
        self.changed=False
        for i in range (0, self.dim):
            for j in range (0, self.dim):
                self.a[i][j].remove_possbilities_by_row()
                self.a[i][j].remove_possbilities_by_column()
                self.a[i][j].check_above()
                self.a[i][j].check_below()
                self.a[i][j].check_unique_row()
                self.a[i][j].check_unique_column()
#                self.print_possibilities()
 
    
    def check_file_for_problem (self, is_row=True):
        for i in range (0, self.dim):
             cdict = {k:0 for k in range(1, self.dim)}
             cdict ['?'] = 0
             cdict ['/'] = 0
             for j in range (0, self.dim):
                 if (is_row):
                     cdict[self.a[i][j].num] +=1
                 else:
                      cdict[self.a[j][i].num] +=1                  
             if cdict['/']>2:
                 return True
             for k in range (1, self.dim):
                 if cdict[k] > 1:
                    return True
        return False
    
    # do_i_have_a_contradiction
    #
    # returns true if there's a problem with the current grid
    def do_i_have_a_contradiction(self):
        # check above/below requirement
        for i in range (0, self.dim):
            for j in range (0, self.dim):
                if self.a[i][j].am_i_a_problem():
                    return True
                
        #check rows for problems
        if self.check_file_for_problem(True): return True

        #check columns for problems
        if self.check_file_for_problem(False): return True
            
        
    # is_solved
    #
    # returns true if the puzzle is solved (all squares are set)
    def is_solved(self):
         for i in range (0, self.dim):
            for j in range (0, self.dim):
                if (self.a[i][j].num=="?"):
                    return False
         return True 
     
    # simple_solve
    def simple_solve(self):
        self.changed = True
#       while self.changed:
        for i in range(20):
            self.simple_check()
        self.simple_check()
    
    # get_possibility_list
    # 
    # Finds the first square with only two possibilities and then returns
    # a list of tuples with (i, j, p) where i,j is the square coordinates
    # and p is the possibility
    def get_possibility_list(self):
        pos_list = []
        for i in range (0, self.dim):
            for j in range (0, self.dim):
                if len(self.a[i][j].possibilities)==2:
                    for p in self.a[i][j].possibilities:
                        pos_list.append((i, j, p))
                    return pos_list
                
    
           
    def try_hypothetical(self, indent):
        pos_list = self.get_possibility_list()
        for p_tuple in pos_list:
            print (indent + "Trying: {} at ({}, {})".format(p_tuple[2], p_tuple[0], p_tuple[1]))
            bcopy = Board(self.dim)
            bcopy.copy(self)
            bcopy.set_square(p_tuple[0], p_tuple[1], p_tuple[2])
            bcopy.print_board(indent)
            bcopy.simple_solve()
            bcopy.print_board(indent)
            input()
            is_ok = not bcopy.do_i_have_a_contradiction()
            if (not is_ok):
                print (indent + "Board is not valid.")
                continue
            else:
                print (indent + "Board is valid.")
            if (bcopy.is_solved()): 
                print (indent + "Board is solved!\n")
                return bcopy
            recurb = bcopy.try_hypothetical(indent + "   ")
            if (recurb):
                return recurb
        print (indent + "Dead end: Exit hypothetical\n")
        return None

            
b = Board(6, 
          """??3???"""
          """?3????"""
          """???4??"""
          """?????1"""
          """4?????"""
          """????2?"""
          )

print ("Initial Board:")
b.print_board("")
b.simple_solve()

print ("Initial Board after rules followed:")
b.print_board("")
if (not b.is_solved()):
    solution  = b.try_hypothetical("")
    print ("Solution:")
    solution.print_board("")





