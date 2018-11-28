# Workflow

## What is workflow?
As you work more with tools like MySQL and Python, you'll start to see that they become most valuable in combination with one another. I use the term workflow to refer to the process of working across different tools to do things like collect, clean, process, and analyze data.

## How can we link MySQL and Python?

## Example: Patent attorneys

As an illustration of workflow, we will load some data on patent attorneys, and then code their gender. We need to do a few things before we get started. First, let's create a database.

```mysql
create database `phd_patentsview` default character set utf8mb4 collate utf8mb4_bin;
```

Next, create a table to hold the data.

```mysql
drop table if exists phd_patentsview.lawyer;
create table phd_patentsview.lawyer (
id varchar(45) not null,
name_first varchar(100) null,
name_last varchar(100) null,
organization varchar(100) null,
country varchar(10) null,
primary key (id));
```

Now download the data [here](http://www.patentsview.org/data/20171226/lawyer.tsv.zip).

Next, load the data.

```mysql
load data local infile '~/Desktop/lawyer.tsv' 
  into table phd_patentsview.lawyer 
  fields 
     terminated by '\t' 
  lines terminated by '\n' 
  ignore 1 lines
  (@id,
   @name_first,
   @name_last,
   @organization,
   @country)
   set id=if(@id='' or @id='NULL', null, @id),
       name_first=if(@name_first='' or @name_first='NULL', null, @name_first),
       name_last=if(@name_last='' or @name_last='NULL', null, @name_last),
       organization=if(@organization='' or @organization='NULL', null, @organization),
       country=if(@country='' or @country='NULL', null, @country);
```

Let's add a column to store lawyer gender.

```mysql
alter table phd_patentsview.lawyer add column inventor_gender_gg varchar(45) null;
```

Finally, let's add a few indexes to help speed things up.

```mysql
alter table phd_patentsview.lawyer add index name_first_idx (name_first),
                                   add index id_idx (id);
```


## Part #1: Data cleaning

Our goal is to code lawyer gender based on first names. To help facilitate that, let's first create a new table that lets us focus on first names and set aside some of the other data in the table. We can define a table with the following structure.

```mysql
drop table if exists phd_patentsview.lawyer_gender_coding;
create table phd_patentsview.lawyer_gender_coding (
name_first_id int(11) not null auto_increment,
name_first varchar(100) not null,
name_first_frequency int(11) null,
name_first_clean varchar(100) null,
inventor_gender_gg varchar(45) null,
primary key (name_first_id));
```

Now let's add the data to the table.

```mysql
insert into phd_patentsview.lawyer_gender_coding (name_first, name_first_frequency)
select name_first, count(*)
from phd_patentsview.lawyer
where name_first is not null
group by name_first;
```

And we'll add an index on first name to help speed things up later.

```mysql
alter table phd_patentsview.lawyer_gender_coding add index name_first_idx (name_first);
```

If we look at the resulting list of names, we'll notice that they're quite messy. See the table below for a few examples. 

| name_first_id | name_first                     | 
| ------------- | ------------------------------ |
| 20            | "Henry L. (""Bud"")"           | 
| 9326          | Hsiang-ning &#8220;Sean&#8221; |
| 18860         | Robert M?                      |

Before we try to run the gender coding, we'll want to clean up the names a bit. I've written a simple Python script that will pull data from MySQL and do just that. It's too long to paste here, but you can view the whole script [here](https://github.com/russellfunk/phd_toolbox/blob/master/workflow/clean_lawyer_name.py).

## Part #2: Data collection

Now that we've cleaned our big list of first names, we'll want to collect some data on the gender most commonly associated with each name. Typically, researchers do this by using publicly available data from [Social Security Administration records](https://www.ssa.gov/oact/babynames/index.html). Thankfully, several Python packages have been written that make this whole process much easier. We'll be using a package called [gender_guesser](https://pypi.org/project/gender-guesser/), which you can install by running the following command:

```
pip install gender-guesser
```

Once again, the code is too long to show in this note, but you can see it in a separate file, [here](https://github.com/russellfunk/phd_toolbox/blob/master/workflow/code_lawyer_gender_gg.py).

After we have run the script to assign each name a probably gender, we'll want to add that data back to the original lawyer data table so we can run some analyses (which we'll do next). You can do that by running the short query below.

```mysql
update phd_patentsview.lawyer t1,
       phd_patentsview.lawyer_gender_coding t2
set t1.inventor_gender_gg = t2.inventor_gender_gg
where t1.name_first = t2.name_first;
```

## How can we link R to MySQL?

Python is just the beginning. You can also link MySQL to many other tools, including R, a popular, open source statistical environment. Probably the easiest way to link R to MySQL is through the RMySQL library, which you can install using the following code.

```R
install.packages("RMySQL")
```

Once you have that installed, you can easily pull data from MySQL to analyze in R.

```R
# load the library
library(RMySQL)

# establish a database connection
conn <- dbConnect(MySQL(),
                  user = "root", 
                  password = "",
                  dbname="phd_patentsview", 
                  host = "localhost")

# pull some data
data <- dbGetQuery(conn, "select *
                          from phd_patentsview.lawyer
                          limit 1000;")

# check it out
head(data)

# close the database connection
dbDisconnect(conn)

```

## How can we link Stata to MySQL?

You can also connect to MySQL using Stata, which has a nice built in command called odbc designed exactly for this purpose. Before using the odbc command, though, you'll need to install [MySQL Connector/ODBC](https://dev.mysql.com/downloads/connector/odbc/).

Once you have that installed, you can pull data directly into Stata from MySQL using the code below.

```
set odbcdriver ansi
#delimit ;
local sql_query 

select *
from phd_patentsview.lawyer;

#delimit cr
display in smcl as text "`sql_query'"
odbc load, exec("`sql_query'") conn("DRIVER={MySQL ODBC 5.3 Unicode Driver};SERVER=localhost;DATABASE=phd_patentsview;UID=root;PWD=;PORT=3306;")
```
