from ex1 import *

crossword, n, m = readCrossword()
slots = calculateSlots(crossword, n, m)
dictionary = readDictionary()

solution = crossword_solution(slots, m, n, dictionary, crossword)



#print("A solution for this crossword is : {0}".format(slots))