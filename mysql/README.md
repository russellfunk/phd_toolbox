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
* Most people in our field tend to use tools like __Stata__ or __Excel__ for data management
* But Stata and Excel are not designed to be data management tools, and consequently, most researchers __stretch them beyond their limits__
 * This is increasingly true as projects using __"big" data__ are becoming more common
* MySQL is designed __from the ground up__ for data management, which gives it many advantages over other tools
  * __Speed__ (access and manipulate data quickly)
  * __Scale__ (manage projects with millions or billions of records)
  * __Storage__ (keep one copy of your data, minimize possibility of errors, use only what you need)
  * __Integrity__ (identify errors in your data quickly, and prevent them from occurring in the first place)
* In addition, MySQL is designed to "play nicely" with __many other data tools,__ which greatly extends its scope and power
  * For example, in the third session, we'll work on integrating __MySQL__ and __Python.__

![](https://github.com/russellfunk/phd_toolbox/blob/master/images/change_my_mind.jpeg)

## How do you do things with MySQL?
* More than just letting you __store your data,__ MySQL also lets you __do things__ more actively
* In SQL land, you act on your data by running __queries__ (hence the name, __S__ tructured __Q__ uery __L__ anguage)
* Probably __90%__ of what you do in MySQL will consist of running some combination of the following types of __queries__
  * `select` queries are for viewing records
  * `update` queries are for updating existing records
  * `insert` queries are for adding new records
* Other common queries include
  * `create database` queries are for creating new databases
  * `create table` queries are for creating new tables
  * `join` queries are for linking across tables
  
Here are a few quick __examples__ that bring together some of these queries (and a few more)

```mysql
-- create database
create schema my_database 
default character set utf8 
collate utf8_bin;
```

```mysql
-- create a table for firms
drop table if exists my_database.firms;
create table my_database.firms
(firm_id int(11) not null,
year int(11) not null,
state varchar(2) null,
profits double null,
treated int(11) null,
primary key (firm_id, year));
```

```mysql
-- insert query
insert into my_database.firms (firm_id, year, state, profits) values (1, 1999, 'MN', 2),
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
                                                            (4, 2002, 'OH', null);
```

```mysql
-- select query
select *
from my_database.firms;
```
 
```mysql
-- update query
update my_database.firms
set treated = 1
where year > 2000
and state in ('MN','OH');
```


```mysql
-- create a table for states
create table my_database.states
(state varchar(2) not null,
population double null,
primary key (state));
```

```mysql
-- insert query
insert into my_database.states (state, population) values ('MN', 5.577),
                                                          ('VA', 8.47),
                                                          ('OH', 11.66);
```

```mysql
-- join query
select *
from my_database.firms,
     my_database.states
where firms.state = states.state;
```

## On to real data!
We're moving very quickly---don't worry if you feel a bit lost. In my experience, the best way to learn any kind of programming language or tool is to simply get your hands dirty and start working with real data. You'll feel more motivated and get a better sense for how the tool may be useful in the real world.

We're going to focus on fiddling with some data on granted patents from the U.S. Patent & Trademark Office (USPTO), available here: (http://www.patentsview.org/download/). Make sure to check out the codebook (see the link on the left side of the page), which, helpfully, tells you which data fields you should use to define your tables when loading the data into MySQL.

Download the following files and extract them to a directory
* patent (http://s3.amazonaws.com/data-patentsview-org/20180528/download/patent.tsv.zip)
* rawassignee (http://s3.amazonaws.com/data-patentsview-org/20180528/download/rawassignee.tsv.zip)

Run the following queries to get the data loaded


```mysql
-- create database
create schema patentsview 
default character set utf8 
collate utf8_bin;
```

```mysql
-- create a table to hold the patent data
drop table if exists patentsview.patent;
create table patentsview.patent (
id varchar(20) not null,
type varchar(100) null default null,
number varchar(100) not null,
country varchar(20) null default null,
date date null default null,
abstract text null default null,
title text null default null,
kind varchar(10) null default null,
num_claims int(11) null default null,
filename varchar(120) null default null,
primary key (id));
```

```mysql
-- load the patent data
load data local infile 'patent.tsv' 
  into table patentsview.patent 
  fields 
     terminated by '\t' 
  lines terminated by '\n' 
  ignore 1 lines
  (@id,
   @type,
   @number,
   @country,
   @date,
   @abstract,
   @title,
   @kind,
   @num_claims,
   @filename)
   set id=if(@id='' or @id='NULL', null, @id),
       type=if(@type='' or @type='NULL', null, @type),
       number=if(@number='' or @number='NULL', null, @number),
       country=if(@country='' or @country='NULL', null, @country),
       date=if(@date='' or @date='NULL', null, @date),
       abstract=if(@abstract='' or @abstract='NULL', null, @abstract),
       title=if(@title='' or @title='NULL', null, @title),
       kind=if(@kind='' or @kind='NULL', null, @kind),
       num_claims=if(@num_claims='' or @num_claims='NULL', null, @num_claims),
       filename=if(@filename='' or @filename='NULL', null, @filename);
```

```mysql
-- add indexes
alter table patentsview.patent add index `number_idx` (`number` asc),
                               add index `date_idx` (`date` asc);
```

```mysql
-- create a table to hold the assignee data
drop table if exists patentsview.rawassignee;
create table patentsview.rawassignee (
uuid varchar(45) not null,
patent_id varchar(20) not null,
assignee_id varchar(45) null default null,
rawlocation_id varchar(150) null default null,
type int(11) null default null,
name_first varchar(100) null default null,
name_last varchar(100) null default null,
organization varchar(300) null default null,
sequence int(11) not null,
primary key (uuid),
unique key (patent_id, sequence));
```

```mysql
-- load the rawassignee data
load data local infile 'rawassignee.tsv' 
  into table patentsview.rawassignee 
  fields 
     terminated by '\t' 
  lines terminated by '\n' 
  ignore 1 lines
  (@uuid, 
   @patent_id, 
   @assignee_id, 
   @rawlocation_id, 
   @type,
   @name_first, 
   @name_last,
   @organization, 
   @sequence)
   set uuid=if(@uuid='' or @uuid='NULL', null, @uuid),
       patent_id=if(@patent_id='' or @patent_id='NULL', null, @patent_id),
       assignee_id=if(@assignee_id='' or @assignee_id='NULL', null, @assignee_id),
       rawlocation_id=if(@rawlocation_id='' or @rawlocation_id='NULL', null, @rawlocation_id),
       type=if(@type='' or @type='NULL', null, @type),
       name_first=if(@name_first='' or @name_first='NULL', null, @name_first),
       name_last=if(@name_last='' or @name_last='NULL', null, @name_last),
       organization=if(@organization='' or @organization='NULL', null, @organization),
       sequence=if(@sequence='' or @sequence='NULL', null, @sequence);
```

```mysql
-- add indexes
alter table patentsview.rawassignee add index `patent_id_idx` (`patent_id` asc);
```



## Exercises for during the workshop

* Determine how many patents were __granted__ in the year 1980 (easy)
* How many __unique countries__ are represented in the `country` column of the `patent` table? (moderate)
* Find the most __prolific assignee__ (by name) in the year 1980 (hard)
* On average, how many __claims__ do issued patents make by year? (hard)
  * Is there any __trend__ in this average?

## Bonus notes---Loading data into MySQL

* Loading data into MySQL can be a pain because (as you can see from the code above) you need to declare the data types for each field in advance
* Getting the data types right is important to ensure data integrity; MySQL will also complain relentlessly (for good reason) if you try to import data (e.g., string) into a column defined by an incompatible data type (e.g., double)
* It's fairly easy to eyeball the data types in a fairly small file, but for bigger tables, you may run into trouble if the file is too big to load in some kind of text editor, or if there are many columns
* Luckily, there are some tools that can "sniff" the columns in your file and (attempt to) detect the data types
* The best place to start is with MySQL Workbench's Data Import wizard (go to `Server -> Data Import`)
* Another tool that can do this is `csvkit` (see the `csvsql` command) (https://csvkit.readthedocs.io/) 

## Bonus notes---Digging deeper

In my view, the best way to learn about MySQL is to use it for your research. But it's also good to have a reference lying around for when you get stuck. See below for some resources that I've found (and continue to find) useful.

* [MySQL (5th Edition) (Developer's Library)](https://www.amazon.com/MySQL-Developers-Library-Paul-DuBois/dp/0321833872/ref=sr_1_4?ie=UTF8&qid=1540413243&sr=8-4&keywords=mysql); save money by getting an older edition (4th edition should be fine)
* [Stack Exchange site for databases](https://dba.stackexchange.com/)
