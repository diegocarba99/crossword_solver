#!/usr/bin/python



# Function: function_name
# ------------------------------------------------------------------------------
# Function that reads a file containing a crossword and stores it in a matrix
#   
#   returns:
#       crossword = the matrix representation of the crossword
#       i = vertical size of the crossword
#       j = horizontal size of the crossword
#
def readCrossword():
    file = open("crossword_CB_v2.txt", "r") # Open the file
    i = 0
    j = 0
    crossword = []
    for line in file: # For every line in the file
        temp_line = []
        j = 0
        for word in line.split(): # For every caracter in the file
            if word == '#': # If position is blank or filled
                temp_line.append(int(-1))
            else:
                temp_line.append(int(0))
            j +=1
        crossword.append(temp_line) # Add calculated line to crossword
        i +=1
    return crossword, i, j

# Function: readDictionary
# ------------------------------------------------------------------------------
# Stores the list of words of a file onto a dictionary indexed by the size of
# the word
#
#   returns: a list of the words in the file indexed by size
#
def readDictionary():
    file = open("diccionari_CB_v2.txt", "r") # Open the file
    word_list = [] # List with all the words from the dictionary
    max_len = 1

    for line in file:
        word_list.append(line[:-1]) # Add word without the '\n'
        if len(line) > max_len: # Calculate the longest words length
            max_len = len(line)

    dictionary = [None] * (max_len-2) # Create empy dictionary

    for word in word_list:
        if dictionary[len(word)-2] == None: # If position is empty
            dictionary[len(word)-2] = [word] # Add new list with first word
        else:
            dictionary[len(word)-2].append(word) # Append word to list
    return dictionary


# Function: horizontalBeginning
# ------------------------------------------------------------------------------
# Calculates if a given position in the crossword is the beginning of a
# horizontal word
#
#   crossword: crossword whose position will be calculated if it's the beginning
#              of a horizontal word
#   i: vertical coordinate of the position
#   j: horizontal coordinate of the position
#   m: horizontal size of the crossword
#
#   returns: True if position is the beginning of a horizontal word.
#            False otherwise
#
def horizontalBeginning(crossword, i, j, m):
    # Possible two situations:
    #   ///[ ][ ] --> nothing-blank-blank
    #   [#][ ][ ] --> filled-blank-blank
    if (j == 0 and crossword[i][j+1] == 0) or (j < m-1 and crossword[i][j+1] == 0 and crossword[i][j-1] == -1 ):
        return True
    else:
        return False

# Function: verticalBeginning
# ------------------------------------------------------------------------------
# Calculates if a given position in the crossword is the beginning of a vertical
# word
#   crossword: crossword whose position will be calculated if it's the beginning
#              of a vertical word
#   i: vertical coordinate of the position
#   j: horizontal coordinate of the position
#   n: vertical size of the crossword
#
#   returns: True if position is the beginning of a vertical word.
#            False otherwise
#
def verticalBeginning(crossword, i, j, n):
    # Possible two situations:
    #   ///
    #   [ ] --> nothing-blank-blank
    #   [ ]
    #
    #   [#]
    #   [ ] --> filled-blank-blank
    #   [ ]
    if (i == 0 and crossword[i+1][j] == 0) or (i < n-1 and crossword[i+1][j] == 0 and crossword[i-1][j] == -1 ):
        return True
    else:
        return False

# Function: calculateLengthHorizontal
# ------------------------------------------------------------------------------
# Given a horizontal slot beginnin, calculates it's size
#
#   crossword: crossword whose slots' size will be calculated
#   i: vertical coordinate of the slot
#   j: horizontal coordinate of the slot
#   m: horizontal size of the crossword
#
#   returns: length of the slot
#
def calculateLengthHorizontal(crossword, i, j, m):
    length = 1
    while (j < m-1) and (crossword[i][j+1] != -1):
        length += 1
        j += 1
    return length

# Function: calculateLengthVertical
# ------------------------------------------------------------------------------
# Given a vertical slot beginnin, calculates it's size
#
#   crossword: crossword whose slots' size will be calculated
#   i: vertical coordinate of the slot
#   j: horizontal coordinate of the slot
#   n: vertical size of the crossword
#
#   returns: length of the slot
#
def calculateLengthVertical(crossword, i, j, n):
    length = 1
    while (i < n-1) and (crossword[i+1][j] != -1):
        length += 1
        i += 1

    return length

# Function: calculateSlots
# ------------------------------------------------------------------------------
# Given a crossword, calculates all the beginning of words, their orientation,
# position and length
#
#   crossword: matrix representation of a crossword whose slots will be calculated
#   n: vertical size of the crossword
#   m: horizontal size of the crossword
#
#   returns: list with the slots' information
#
def calculateSlots(crossword, n, m):
    slots = []
    for i in range(n):
        for j in range(m):
            if crossword[i][j] != -1:
                if horizontalBeginning(crossword, i, j, m):
                    slots.append(['H', i, j, calculateLengthHorizontal(crossword, i, j, m)])
                if verticalBeginning(crossword, i, j, n):
                    slots.append(['V', i, j, calculateLengthVertical(crossword, i, j, n)])
    return slots

# Function: main
# ------------------------------------------------------------------------------
# Executes the main program
#
#def main():
#    crossword, n, m = readCrossword()
#    slots = calculateSlots(crossword, n, m)
#    dictionary = readDictionary()

#if __name__ == "__main__":
#    main()



# Function: max_word
# ------------------------------------------------------------------------------
# Find the first word with maximal length in the crossword
#
#   slots: list with the slots' information
#   m: vertical size of the crossword
#   n: horizontal size of the crossword
#
#   returns: word with maximal length (if there is many, returns the first of the slots' list)
#       => ['V'/'H' , row, column, length]
#
def max_word(slots, m, n):
    i=0     # i : row index in the slots' list
    max=0   # maximum word length founded in the crossword
    while i < len(slots):
        if(slots[i][3]>max):    # slots[i][3] = length
            max=slots[i][3]
            position=slots[i]     
    return position



# Function: find_constraint
# ------------------------------------------------------------------------------
# Finds if there is any constraint for a word
# (a constraint is letter already founded whiwh has to be in this word)
#
#   word : given word in the slots' list
#   solution : partial solution of the crossword
#
#   constraint_list : list with all constraints of letters for one slot
#       => [position, letter]
#
def find_constraint(word,solution):
    i=word[1]
    j=word[2]
    length=word[3]
    constraint_list = []  
    if word[0]=='V':
        while i <= word[1]+length:
            if solution[i][j] != '0':
                letter = solution[i][j]
                constraint_list = constraint_list + [i,letter]
                i+=1
            else:
                i+=1
    else :      # if word[0]=='H'       
        while j <= word[2]+length:
            if solution[i][j] != '0':
                letter = solution[i][j]
                constraint_list = constraint_list + [j,letter]
                j+=1
            else:
                j+=1   
    return constraint_list



# Function: find_word
# ------------------------------------------------------------------------------
# Searchs in the dictionary if there is a word with a length and constraints
#
#   length: length of the searched word
#   constraint_list: letter constraint in the searched word
#   dictionary: result of the function 'readDictionary'
#
#   returns 0 if there isn't such a word in the dictionary
#   returns a solution for the searched word if it exists
#
def find_word(length, constraint_list, dictionary):
    word=' '
    for word in dictionary :
        if len(word)==length:
            i=0
            while i<=len(constraint_list):
                letter = constraint_list[i][1]
                position = constraint_list[i][0]
                if word[position] != letter:
                    break
                else:
                    i+=1
    if word==' ':
        return 0
    else :
        return word



# Function: crossword_solution
# ------------------------------------------------------------------------------
# Gives a final solution for the given crossword
#
#   slots: list with the slots' information
#   m: vertical size of the crossword
#   n: horizontal size of the crossword
#   dictionary: given dictionary
#   crossword: given crossword
#
#   returns a crossword as final solution
#
def crossword_solution(slots, m, n, dictionary, crossword):
    temp_solution = crossword
    slots_copy = slots
    # we will erase each word of slots_copy when we find its solution in the dictionary
    k=0

    while k <= len(slots):
        word = max_word(slots_copy, m, n)
        constraint_list = find_constraint(word, temp_solution)

        # backtracking (we search another word if this one doesn't work) :
        while find_word(word[3], constraint_list, dictionary) == 0:
            slots_copy_2 = slots_copy
            slots_copy_2.remove(word)
            word = max_word(slots_copy_2, m, n)

        # when a word works, we write it in the solution
        if find_word(word[3], constraint_list, dictionary) != 0:
            word_from_dictionary = find_word(word[3], constraint_list, dictionary)
            slots_copy.remove(word)

            i=word[1]
            j=word[2]
            length=word[3]
                
            if word[0]=='V':
                while i <= word[1]+length:
                    temp_solution[i][j] = word_from_dictionary[i]
                    i+=1
            else :      # if word[0]='H'       
                while j <= word[2]+length:
                    temp_solution[i][j] = word_from_dictionary[j]
                    j+=1   

        # else :
        #   is it possible ?

        k+=1
    
    final_solution = temp_solution
    return final_solution
        

