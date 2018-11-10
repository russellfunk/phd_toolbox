# Python

## What is Python?
* General purpose programming language
* Interpreted, not compiled
* Object oriented
* Named after Monty Python

![](https://github.com/russellfunk/phd_toolbox/blob/master/images/monty_python.png)

## Why should you use Python?
* General purpose programming language
* Helpful for nearly all aspects of the research process
  * Data collection (e.g., web scraping, web interfaces)
  * Data cleaning
  * Data processing (e.g., constructing variables) 
  * Data modeling (e.g., networks, machine learning)
  * Data visualization
* De facto language of the data science community
* __Massive__ user base means people are always writing awesome libraries and it's easy to get help
* It's also really easy to interface with other tools

## How do you do things with Python?

When it comes to writing and running programs in Python, you have a few different options.

* Write code in a text editor and run using `Terminal` (macOS) or `Command Prompt` (Windows) (this is the best general purpose approach).
* Write code directly in the python interpreter (this is most useful for quickly testing something or ver short programs)
* Write code in [http://jupyter.org/](Jupyter Notebook) (this is a great approach for data analysis, but can be clunky for other things).

Overall, there's no right or best way; just whatever is most comfortable and suits your needs.

Here are a few quick __examples__ that bring together some of these queries (and a few more)

## How do I get started?

No programming tutorial would be complete without a hello world program. Here's all you need in python. 

```python
print("Hello, World!")
```

## Data types
One of the things that makes python so useful right out of the box are its native data types, so we're going to spend a while going through them. A few things to note. First, python uses ___dynamic typing__, meaning that variable types are not specifically declared and are instead inferred from the objects they represent.

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
...in which the compiler get angry. 

# Strings, numbers

```python
"""numbers are pretty straightforward"""
foo = 3
bar = 4
baz = foo/bar # be careful if you run this in python 2
foo = 3.0
bar = 4.0
baz = foo/bar # gives you the result you expect

"""strings are awesome"""

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

""

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

There is a lot more that you can do with lists, most of which is a bit outside our scope today. But if you're curious, do some digging on `list` `comprehensions`.

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

One of the most powerful data types in python is the dictionary. It's literally a mini database. The key thing to remember about dictionaries is that they create a 1 to 1 mapping of keys to values. That means that you cannot repeat the same key more than once.

```python

```

# Sets

Sets are also useful, and can be extremely fast for some kinds of tasks. 

```python

```

## Loops

If you have any experience with other programming languages, you've almost certainly encountered loops. Not too many surprises in python.

```python

# create a list to loop over
companies = ["Company A", "Company B", "Company Q", "Company Z"]

# for loop
for company in companies:
  print(company)
  
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


## Bonus—cool package demonstration (geopy)

```python
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="phd_workshop")
location = geolocator.geocode("321 19th Ave S Minneapolis")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)
```

## Digging deeper

* For python questions, [http://stackoverflow.com/](Stack Overflow) is your friend
* [https://www.amazon.com/Python-Nutshell-Desktop-Quick-Reference/dp/144939292X/](Python in a Nutshell) and the [https://www.amazon.com/Python-Cookbook-Third-David-Beazley/dp/1449340377/](Python Cookbook) are both good general references.
* [https://www.amazon.com/Natural-Language-Processing-Python-Analyzing/dp/0596516495/](Natural Langauge Processing with Python) is getting a bit dated but is still an outstanding introduction to the practical sides of NLP.
* [https://www.amazon.com/Mining-Social-Web-Facebook-Instagram/dp/1491985046/](Mining the Social Web) is a nice overview of interacting with APIs using python, especially for social media sites.