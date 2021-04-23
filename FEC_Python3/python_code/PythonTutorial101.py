# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=2>

# Python cares for space. \ is the continuation character
# Python is a case sensitive language
# Python has a sentinel value - None

# <codecell>

a = 0 + 45 +  \
    5 + 6
a= None

# <headingcell level=2>

# Everything in python is an object. Even functions, modules, everything

# <headingcell level=2>

# Python works on convention rather than forcing than it on the programmer.

# <headingcell level=2>

# Python does not have static checked data types.

# <codecell>

int(a)

# <codecell>

# Defining a variable
a = 2

# <headingcell level=3>

# Python is dynamically strongly typed language. In weakly typed languages you can change the datatype of a variable after initialization

# <codecell>

# You cannot reference unbound variables
b

# <codecell>

#b = {}
b = dict()
b['3'] = "Ravikant"

# <headingcell level=1>

# In Perl
# 
# my $b->{'2'} = "Ravikant";
# use Data::Dumper;
# > print Dumper $b;
# > '
# $VAR1 = {
#           '2' => 'Ravikant'
#         };
# rkg@rkg-Vostro-2520:~$ ^C
# rkg@rkg-Vostro-2520:~$ 

# <codecell>

# Cannot intermatch types
b = 2
a = "Atr"
c = str(b) + a

# <codecell>

1 or 5
a += 1

# <headingcell level=1>

# Logical operators (|| && do not work in python). There is no ++ operator
# Logical operators
#    'and', 'or', 'not' == != >= <= 
# Exponential operator 
# **

# <codecell>

2 ** 8

# <codecell>

# Python conditional expressions do not yeild boolean or 1 or 0 
[] and 5
a = False
b = True

# <codecell>

# Boolean in python is False and True
# These are all False [] () {} 0 None

# <codecell>

24 | 1 & 5 ^3 ~23

# <codecell>

~2

# <codecell>

 # == vs is
a = "question"
b = "question"
a == b
a is b

# <codecell>

a = None

# <codecell>

a is None

# <codecell>

# Functions
def a():
    return 1, 2, 3

# <codecell>

a, b, c = a()

# <codecell>

c

# <codecell>

print str(c)

# <codecell>

a = {}
a = dict()
a[5] = 4
a[5] = 3
a[2] = 4
del a[2]
print a

# <codecell>

# Allowed values for keys are any values which are immutable
a["valid key"] = "Ravi"

# <codecell>

a

# <codecell>

a= [1,2,3]
a = tuple(a)
print a

# <codecell>

# Mix and match types is allowed
a[4.2] = 1

# <codecell>

a[{2,3}] = 1

# <codecell>

a.keys()

# <codecell>

a.values()

# <codecell>

a.items()

# <codecell>

# Do not do this
for key in a.keys():
    print a[key]
# Use items instead
for key, value in a.items():
    print key
    print value

# <codecell>

# Arrays are zero index based
a = [1,2,3]

# <codecell>

# Python has brillianto negative indices
a[-2]

# <codecell>

a[2]

# <codecell>

# Array slicing
a[0:2]

# <codecell>

a[0:len(a)+1]

# <codecell>

a[0:]

# <codecell>

a[1:-1]

# <codecell>

a[:5]

# <codecell>

a.append(2)

# <codecell>

a

# <codecell>

a.index(3)

# <codecell>

a.reverse()

# <codecell>

a

# <codecell>

a.pop()

# <codecell>

a = [1,2,3,4,5,6]

# <codecell>

a.insert(9,10)

# <codecell>

a

# <codecell>


# <codecell>

a.insert(10, 5)

# <codecell>

a

# <codecell>

a.extend([1,2,3])

# <codecell>

a

# <codecell>

a.remove(4)

# <codecell>

a

# <codecell>

a.remove??

# <codecell>

#  All 

# <codecell>

a = "Malvika"
b = "Malvika"
a is b

# <headingcell level=2>

# # They are all false
# {} () 0 "" 

# <codecell>

a = a + [1,2]

# <codecell>

a

# <codecell>

a = [1,2] * 3

# <codecell>

a

# <codecell>

a = [0] * 10

# <codecell>

a

# <codecell>

len(a)

# <codecell>

a = (1, 2, 3)

# <codecell>

b = {}
b[a]  = 1

# <codecell>

b

# <codecell>

a = (1, [2,3], 1)

# <codecell>

a[1].append(2)

# <codecell>

a

# <codecell>


# <codecell>

b[a] = 1

# <codecell>

list(a)

# <codecell>

tuple([1,2])

# <codecell>

# Functions pass is equivalent to ; or {}
def a(v, b, c=2):
    pass

# <codecell>

x, y, z = a(1,2)

# <codecell>

x

# <codecell>

y

# <codecell>

z

# <codecell>

x,y,z = (1,2,3)

# <codecell>

# for (i=0; i<n; i++)
n = 10
a = [0] * n
for i in range(0,8,2):
    print i

# <codecell>

for index, value in enumerate(a):
    print index
    print value

# <codecell>

a = "sdf" + "csdf" 

# <codecell>

a

# <codecell>

c = "sf%s" % (a)

# <codecell>

c

# <codecell>

c.lower()

# <codecell>

c.upper()

# <codecell>

z = [charac + "abba"  for charac in c if charac !='s']

# <codecell>

z

# <codecell>

a = getattr({}, "clear")

# <codecell>

a()

# <codecell>

lambda x : x ** 2

# <codecell>


# <codecell>


