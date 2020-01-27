# Module 5 exercise

#########################  Regex  ####################################
import re
"""
# Given the following data:
str1 = "The answer is 42"
str2 = "What... is the air speed of an unladen swallow?"
str3 = "3.15; 2.383 and 11.039*2.77  1257.11"
str4 = "2020 / 08 / 14"
inList = [str1, str2, str3, str4]

# 1. Write regex to print the string if the string has:
# a. a digit
for s in inList :
    if re.search("\d",s):   # if re.search returns None, it means False
        print(s)
print()

# b. a number that's at least 3 digit long
for s in inList :
    if re.search("\d{3}",s):
        print(s)
print()

# c. no letters
for s in inList :
    if re.search("^[^a-zA-Z]+$",s):  # when you want to say an exact number of something
        print(s)                     # use both anchors, then describe what you want for the string
print()                              # In this case, we want 1 or more non-letters between
                                     # beginning and end of the string

"""
"""
# 2. Write a regex to print 
# a. the 3 numbers of str4
str4 = "2020 / 08 / 14"
print(re.findall("\d+",str4))
print()

# b. the start location of the 3 numbers of str4
for m in re.finditer("\d+",str4) :
    print(m.start())
print()
"""
"""

# 3. Write a regex to print:
# a. the first word of str2
str2 = "What... is the air speed of an unladen swallow?"
m = re.search("(.+)\.{3}", str2)
#m = re.search("(\w+)\.", str2)
#print(m.group(1))
print()

# b. the last word of str2
#str2 = re.search("(\w+)\?$", str2)
#str2 = re.search(".*\w+\W$", str2)
#print(str2.group(0))

# c. both the first and last words of str2
str2 = re.search("(\w+).*?(\w+)\W$", str2)
print(str2.group(1), str2.group(2))

# d. str2 with spaces changed to underscore

print()

# e. str2 with the ellipsis (...) removed

print()


# 4. Use regex to print only floating point numbers with 2 digit
# after the decimal point in str3
str3 = "3.15; 2.383 and 11.039*2.77  1257.11"

##print(re.findall("\d+\.\d{2}\\b",str3))

for m in re.finditer("\d+\.\d{2}\\b",str3):
    print(m.group())

#print(re.findall("\d+(?:\.\d+)?",str3))




# 5. Write a loop that asks the user input for a birth date. 
# Keep asking until you get a valid birth date.


# Validate the user input with the following steps:
# a. check that the format of str4 is valid: yyyy-mm-dd
    
# b. check that the month is 1-12, day is valid for the 
# month (28, 30, or 31), and the year is between 1900 and 2100

# c. then print the date as mm/dd/yyyy
dayLookup = (0,31,28,31,30,31,31)

while True:
    try:
        s = input("Enter your birthdate: ")
        mObj = re.search("(\d{4})-(\d{2})-(\d{2})", s)
        if mObj:
            y,m,d= int(mObj.group(1)),int(mObj.group(2)),int(mObj.group(3))
            if not 1990 <= y <= 2100:
                raise ValueError("year is 1900-2100")
            if not 1 <= m <= 12:
                raise ValueError("month is 1-12")
            if not 1 <= d <= dayLookup[m]:
                raise ValueError("day is 1-12")
            
            print(f"birthdate is {y}-{m}-{d}")
            break
        else:
            print("Format is yyyy-mm-dd")
    except ValueError as e:
        print(str(e))
""" 




#############  Functions as first class objects ##################


def greeting(text1, text2="", text3="How are you?") :
    print(text1, text2)
    print(text3)


def doWork(f, aStr):
    f(aStr)
    
#doWork(greeting, "hello")

"""

    
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

# write a function doAnyWork that accepts a function and a 
# variable argument list. doAnyWork calls the function and 
# passes the argument list. doWnyWork returns the 
# function's return value
"""
def doAnyWork(*args, **kwargs):
    # args is a tuple
    print("These are the positional args:")
    for arg in args: 
        print(arg)
    # kwargs is a dictionary
    print("These are the keyword args: ")
    for k, v in kwargs.items(): 
        print(k,"=",v)    

doAnyWork(1,2,3,4,a=5,b=6)



def doAnyWork(f, *args, **kwargs):
    f(*args,**kwargs)
    
doAnyWork(greeting, "hello", "CIS 41A")


"""

"""

# will this work? 
L = "hello there CIS41A".split()
#doAnyWork(greeting, L)   # if this works, what does it print?  
doAnyWork(greeting, *L[0:])  # if this works, what does it print?  

# will any of the following print statements run successfully?
def add2(n1, n2=0) :
    return n1 + n2

print(doAnyWork(add2, 5))    
print(doAnyWork(add2, 6, 7))  
print(doAnyWork(add2, n2=8, n1=3))  
# print(doAnyWork(add2, 1, 2, 3))   

"""

########################### Generator ##########################


# 8. If you need to write a generator that produces fibonacci 
# numbers, where the current value is the sum of the 2 previous
# values, would you use a generator function or generator expression?  
# Why?

# Write the fibonacciGen generator

def fibonacciGen():
    prev=0
    curr=1
    while True:
        yield   prev
        prev,curr= curr, prev+curr






fgen = fibonacciGen()   # what is fgen?
for i in range(15):
    print(next(fgen))



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

gen = (num    for row in T   for num in row)

# Note: random discovery-but might be in us one day
#generate= ( (boys,girls)  for boys in self.getBoys()[0:limit] for girls in self.getGirls()[0:limit])


"""
answer = 'y'
while answer == 'y' :
    print()             # code to print a value of the table T
    answer = input("Next val? y/n: ")
    
# Write code to print all values of the table T

"""