# Python

## What is Python?
* General purpose __programming language__
* Interpreted, not compiled
* Object oriented
* Named after __Monty Python__

![](https://github.com/russellfunk/phd_toolbox/blob/master/images/monty_python.jpg)

[This](https://www.youtube.com/watch?v=ycKNt0MhTkk) is why you'll often see __spam__ (the food) references in Python code.

## Why should you use Python?
* Helpful for nearly all aspects of the research process
  * Data __collection__ (e.g., web scraping, web interfaces)
  * Data __cleaning__
  * Data __processing__ (e.g., constructing variables) 
  * Data __modeling__ (e.g., networks, machine learning)
  * Data __visualization__
* De facto language of the data science community
* __Massive__ user base means people are always writing awesome libraries and it's easy to get help
* It's also really easy to interface with other tools

## How do you do things with Python?

When it comes to __writing and running programs__ in Python, you have a few different options.

* Write code in a text editor and run using `Terminal` (macOS) or `Command Prompt` (Windows) (this is the best general purpose approach).
* Write code directly in the Python __interpreter__ (this is most useful for quickly testing something or ver short programs)
* Write code in [Jupyter Notebook](http://jupyter.org/) (this is a great approach for data analysis, but can be clunky for other things).

Overall, there's no right or best way; just __whatever is most comfortable__ and suits your needs.

Here are a few quick __examples__ that bring together some of these queries (and a few more)

## How do I get started?

No programming tutorial would be complete without a __hello world__ program. Here's all you need in Python. 

```python
print("Hello, World!")
```

## Data types
One of the things that makes Python so useful right out of the box are its __native data types,__ so we're going to spend a while going through them. A few things to note. First, Python uses ___dynamic typing__, meaning that variable types are not specifically declared and are instead inferred from the objects they represent.

```python
foo = 0
foo = "bar"
```

Compare that to the equivalent program in `C`, which uses ___static typing__:

```c
#include <stdio.h>
int main()
{
   int foo = 0;
   foo = "bar";
   return 0;
}
```
...in which the compiler gets angry. 

# Strings, numbers

```python
# numbers are pretty straightforward

# initialize
foo = 3
bar = 4
baz = foo/bar # be careful if you run this in Python 2
foo = 3.0
bar = 4.0

# operations
baz = foo/bar # gives you the result you expect

# strings are more interesting (and fun!)

# initialize
foo = "bar"

# multiline
foo = """this is my
multiline
string"""

# string to list
foo.splitlines()

# save as new single line string
foo_clean = " ".join(foo.splitlines())

# clean up strings
foo = "  I hate leading and trailing spaces    ".strip()
"People say I use too many exclamation points!!!".strip("!")
"133".zfill(5) # great for zipcodes
"55455".zfill(5) # great for zipcodes

# also great for cleaning and standardization
"hello world".upper()
"HeLlO wOrLd".lower()
```

# Lists

A `list` is an ordered set of elements, sometimes called, in other languages, an `array`. Note that lists are __ordered__, the significance of which will become clearer when we look at other data types.

```python
# initialize some lists
a = []
b = list()
a == b # prints True

# add some elements
a.append("foo")
a.append("bar")

# we can also add lists to list
[1,2,3].append([4,5,6])
[1,2,3].extend([4,5,6])

# we can access list elements using slice notation, which is very cool/useful
foo = "turning and turning in the widening gyre".split()
foo[0]
foo[1]
foo[-1]
foo[3:4]

# counting
foo.count("turning")

# sorting
foo.sort()
foo.sort(reverse=True)

# deleting
del foo[0]
```

There's a lot __more you can do with lists,__ most of which is a bit outside our scope today. But if you're curious, do some digging on `list` `comprehensions`.

```python
foo = "1, 2 buckle my shoe. 3, 4 shut the door."

# what if we want to remove all the numbers?
"".join([t for t in foo if not t.isdigit()])

```

# Tuples

Tuples are a lot like lists, but the are __immutable__, meaning that once you define one, it cannot be changed (unless you convert it to another data type).

```python
# initialize some tuples
a = tuple(range(0,100))
b = (1, 2, 'a', 'b')
```

# Dictionaries

One of the most powerful data types in Python is the __dictionary.__ It's literally a mini database. The important thing to remember about dictionaries is that they create a 1 to 1 mapping of keys to values. That means that you cannot repeat the same key more than once.

```python

d = {}
d["foo"] = 1
d["spam"] = 2
d[7] = "baz"
```
In the dictionary above, we have the following key-value pairs:

| Key           | Value         | 
| ------------- | ------------- |
| foo           | 1             | 
| spam          | 2             |
| 7             | baz           |

Notice that our keys and values can be different data types.

Moving on, sometimes it's also useful to make __dictionaries of dictionaries.__

```python
universities = {}
universities[0] = {"name": "University of Minnesota", "city": "Minneapolis", "students": 51147}
universities[1] = {"name": "University of Michigan", "city": "Ann Arbor", "students": 44718}

# iterate over
for id, data in universities.items():
  print(id, data["name"], data["city"], data["students"])

# we can access keys and values separately
universities.keys()
universities.values()
```

Python has a built in package that can let us __print out our dictionary__ in a nice, human readable format. 

```python
>>> from pprint import pprint
>>> pprint(universities)
{0: {'city': 'Minneapolis',
     'name': 'University of Minnesota',
     'students': 51147},
 1: {'city': 'Ann Arbor', 
     'name': 'University of Michigan', 
     'students': 44718}}
```

The following is a really simple illustration of how dictionaries can be useful for some aspects of __data cleaning__.

```python
# create a dictionary of corporate abbreviations
ABBREVIATIONS = {"corporation": "Corp.",
                 "incorporated": "Inc."}

# now standardize some company names
company_names = ("Microsoft Corporation", "Yahoo Incorporated", "New York Times, Inc.")

for company_name in company_names:
  clean_name = []
  for token in company_name.split():
    if token.lower() in ABBREVIATIONS:
      clean_name.append(ABBREVIATIONS[token.lower()])
    else:
      clean_name.append(token)
  print(" ".join(clean_name))
```

# Sets

Sets are also useful, and can be __extremely__ fast for some kinds of tasks. 

```python
# initialize
foo = {1,2,3,4,3,2}
bar = set([4,3,2])

# do some stuff
foo.intersection(bar)
bar.add(7)
foo.intersection(bar)
foo.discard(1)
foo.intersection(bar)

# sets are really useful for counting the number of unique items in a list
foo = [1,3,4,5,6,5,4,3,2,2,4,6,3]
print(len(foo))
print(len(set(foo)))
```

## Loops

If you have any experience with other programming languages, you've almost certainly encountered __loops.__ Not too many surprises in Python.

```python

# create a list to loop over
companies = ["Company A", "Company B", "Company Q", "Company Z"]

# for loop
for company in companies:
  print(company)

# note that "company" is just a variable we create to unpack "companies", we can name it anything
for element in companies:
  print(element)

# we can also use slice notation
for i in range(0,len(companies)):
  print(i, companies[i])

# enumerate can be useful for giving things ids
for company_id, company in enumerate(companies):
  print(company_id, company)

# while loop
i = 0
while i < 100:
  print(i)
  i += 1
```

## Functions

Details on __functions__ are also a bit beyond the scope of this tutorial, but the basics are pretty straightforward.

Here is a function that computes a __Jaccard coefficient,__ which measures the overlap between two sets, using some features of Python's built in `set` data type:

```python
def jaccard(a, b):
  """Given two lists, a and b, return the jaccard coefficient."""
  s1 = set(a)
  s2 = set(b)
  intersection = s1.intersection(s2)
  union = s1.union(s2)
  return float(len(intersection)) / len(union)
```

```python
innovative_firms = ["C10","C24","C45","C12","C09","C12"]
profitable_firms = ["C34","C09","C45","C25","C45","C19","C04","C12"]
print(jaccard(innovative_firms, profitable_firms))

```


## Installing and loading packages
Although the Python programming language comes with a lot of useful built in tools and functions, what really makes the language so useful are the many thousands of __third party packages__ that you can download and use freely. Installation is done via the `pip` command (like `ssc` in Stata).

* `pip install numpy` (Numeric Python, matrix algebra and many other mathematical functions)
* `pip install scipy` (Scientific Python, even more mathematical functions)

Loading is easy:

```python
import numpy as np
np.mean([1,2,3])
```

## Bonus—connecting to MySQL
We will discuss connecting MySQL and Python to __other tools__ in the next session, but as a quick preview, here is a simple example of how you cann connect Python and MySQL. First, you'll need to install a third party package:

```python
# python 2.x
pip install mysql-python

# python 3.x
pip install mysqlclient
```

Then, run the following code:

```python
# load the library
import MySQLdb

# connect to MySQL (on local machine, change parameters as necessary)
conn = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "",
                        charset = "utf8",
                        use_unicode = True)

# now establish a cursor (for running queries)
cursor = conn.cursor()

# now run a select query
cursor.execute(""" select firm_id, year
                   from my_database.firms;")
                   
# now print the rows
for row in cursor.fetchall():
  firm_id = row[0]
  year = row[1]
  print(firm_id,year)

# don't forget to shut things down when done
cursor.close()
conn.close()
```

## Bonus—`geopy` package demonstration

As a quick illustration of how useful third party packages can be, let's go through a quick example. Install the package from the __Python Package Index__ (pypi):
* `pip install geopy`

```python
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="phd_workshop")
location = geolocator.geocode("321 19th Ave S Minneapolis")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)
```

## Digging deeper

* For Python questions, [Stack Overflow](http://stackoverflow.com/) is your friend
* [Python in a Nutshell](https://www.amazon.com/Python-Nutshell-Desktop-Quick-Reference/dp/144939292X/) and the [Python Cookbook](https://www.amazon.com/Python-Cookbook-Third-David-Beazley/dp/1449340377/) are both good general references.
* [Natural Langauge Processing with Python](https://www.amazon.com/Natural-Language-Processing-Python-Analyzing/dp/0596516495/) is getting a bit dated but is still an outstanding introduction to the practical sides of NLP.
* [Mining the Social Web](https://www.amazon.com/Mining-Social-Web-Facebook-Instagram/dp/1491985046/) is a nice overview of interacting with APIs using Python, especially for social media sites.