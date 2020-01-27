# Module 5 exercise
import re
#########################  Regex  ####################################

"""
# Given the following data:
str1 = "The answer is 42"
str2 = "What... is the air speed of an unladen swallow?"
str3 = "3.15; 2.383 and 11.039*2.77  1257.11"
str4 = "2020 / 08 / 14"
inList = [str1, str2, str3, str4]

# 1. Write regex to print the string if the string has:
# a. a digit

print()

# b. a number that's at least 3 digit long

print()

# c. no letters

print()

"""

# 2. Write a regex to print 
# a. the 3 numbers of str4
str4 = "2020 / 08 / 14"
l = re.findall("\d+",str4)
print(f"Year: {l[0]}\tMonth: {l[1]}\tDay: {l[2]}")

# b. the start location of the 3 numbers of str4

#print()



# 3. Write a regex to print:
# a. the first word of str2
str2 = "What... is the air speed of an unladen swallow?"

match= re.search("\w*", str2).group()
print(match)



"""
# b. the last word of str2

print()

# c. both the first and last words of str2

print()

# d. str2 with spaces changed to underscore

print()

# e. str2 with the ellipsis (...) removed

print()


# 4. Use regex to print only floating point numbers with 2 digit
# after the decimal point in str3
str3 = "3.15; 2.383 and 11.039*2.77  1257.11"

print()

"""
"""

# 5. Write a loop that asks the user input for a birth date. 
# Keep asking until you get a valid birth date.

# Validate the user input with the following steps:
# a. check that the format of str4 is valid: yyyy-mm-dd
    
# b. check that the month is 1-12, day is valid for the 
# month (28, 30, or 31), and the year is between 1900 and 2100

# c. then print the date as mm/dd/yyyy

"""
#############  Functions as first class objects ##################

"""
def greeting(text1, text2="", text3="How are you?") :
    print(text1, text2)
    print(text3)
    
greeting("hello")     # what will be printed?

# 6. explain why each of the following lines will work or not work
fctA = greeting("hola")
fctA("ciao")

fctB = greeting
fctB("ciao")
"""

"""
# 7. Write a function called doWork that accepts a function
# and a text string. doWork calls the function and passes the
# text string to the string

    
# call doWork and pass the function greeing and the string "aloha"


"""
"""
# write a function doAnyWork that accepts a function and a 
# variable argument list. doAnyWork calls the function and 
# passes the argument list. doWnyWork returns the 
# function's return value

    

doAnyWork(greeting, "hello", "CIS 41A") 

# will this work? 
#L = "hello there CIS41A".split()
doAnyWork(greeting, L)   # if this works, what does it print?  
doAnyWork(greeting, *L)  # if this works, what does it print?  

# will any of the following print statements run successfully?
def add2(n1, n2=0) :
    return n1 + n2

print(doAnyWork(add2, 5))    
print(doAnyWork(add2, 6, 7))  
print(doAnyWork(add2, n2=8, n1=3))  
# print(doAnyWork(add2, 1, 2, 3))   

"""

########################### Generator ##########################

"""
# 8. If you need to write a generator that produces fibonacci 
# numbers, where the current value is the sum of the 2 previous
# values, would you use a generator function or generator expression?  
# Why?

# Write the fibonacciGen generator

    
fgen = fibonacciGen()   # what is fgen?
for i in range(6):
    print(next(fgen))

"""
"""
# Given the following table:
T = [[1,2,3,4], 
     [11,12,13,14], 
     [21,22,23,24], 
     [31,32,33,34], 
     [41,42,43,44],
     [51,52,53,54],
     [61,62,63,64]]

# Fill in the code to print each data value in the table,
# row by row starting from the first row, and going by 
# col within each row, until the user chooses 'n'


answer = 'y'
while answer == 'y' :
    print()             # code to print a value of the table T
    answer = input("Next val? y/n: ")
    
# Write code to print all values of the table T

"""