# MySQL

## What is MySQL?
* MySQL is a __relational database__
* A relational database is a system for storing data that centers on __four key organizing structures__
 * __Rows__ store records or cases
     * Each row should be identified by a __unique key__ (or "primary" key)
 * __Columns__ store attributes or variables
 * A set of rows and columns together define a __table__
     * Within a database, each table should usually record data about distinct entity types (e.g., firms, people)
 * __Databases__ are collections of related tables

## Why should you use MySQL?
* Most people in our field tend to use tools like Stata or Excel for data management
* But Stata and Excel are not designed to be data management tools, and consequently, most researchers stretch them beyond their limits
 * This is increasingly true as projects using "big" data are becoming more common
* MySQL is designed from the ground up for data management, which gives it many advantages over other tools
  * Speed (access and manipulate data quickly)
  * Scale (manage projects with millions or billions of records)
  * Storage (keep one copy of your data, minimize possibility of errors, use only what you need)
* In addition, MySQL is designed to "play nicely" with many other data tools, which greatly extends its scope and power
  * For example, in the third session, we'll work on integrating MySQL and Python.

![alt text](https://github.com/russellfunk/phd_toolbox/blob/master/images/change_my_mind.jpeg "Logo Title Text 1")

## How do you do things with MySQL?
* More than just letting you store your data, MySQL also lets you do things more actively
* In SQL land, you act on your data by running __queries__ (hence the name, __S__tructured __Q__uery __L__anguage)
* Probably 90% of what you do in MySQL will consist of running some combination of the following types of queries
  * `select` queries are for viewing records
  * `update` queries are for updating existing records
  * `insert` queries are for adding new records
* Other common queries include
  * `create database` queries are for creating new databases
  * `create table` queries are for creating new tables
  * `join` queries are for linking across tables
  
Here are a few quick examples that bring together some of these queries (and a few more)

```mysql
-- create database
create schema my_database 
default character set utf8 
collate utf8_bin;```

```mysql
-- create a table for firms
create table my_database.firms
(firm_id int(11) not null,
year int(11) not null,
state varchar(2) null,
profits double null,
treated int(11) null,
primary key (firm_id, year));```

```mysql
-- insert query
insert into my_database.firms (firm_id, year, state) values (1, 1999, 'MN', 2),
                                                            (1, 2000, 'MN', -2),
                                                            (1, 2001, 'MN', 10),
                                                            (1, 2002, 'MN', 2),
                                                            
                                                            (2, 1999, 'VA', 3.6),
                                                            (2, 2000, 'VA', 40),
                                                            (2, 2001, 'VA', 8),
                                                            (2, 2002, 'VA', 3),
                                                            
                                                            (3, 1999, 'MN', -0.2),
                                                            (3, 2000, 'MN', -20),
                                                            (3, 2001, 'MN', -8),
                                                            (3, 2002, 'MN', -100),
 
                                                            (4, 1999, 'OH', 0),
                                                            (4, 2000, 'OH', null),
                                                            (4, 2001, 'OH', null),
                                                            (4, 2002, 'OH', null);```

```mysql
-- select query
select *
from my_database.firms;```
 
```mysql
-- update query
update my_database.firms
set treated = 1
where year > 2000
and state in ('MN') ;```


```mysql
-- create a table for states
create table my_database.states
(state varchar(2) not null,
population double null,
primary key (state));```

```mysql
-- insert query
insert into my_database.states (state, population) values ('MN', 5.577),
                                                          ('VA' 8.47),
                                                          ('OH', 11.66);```


## Exercises