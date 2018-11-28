# Workflow

## What is workflow?


## Why does workflow matter?


## How can we link MySQL and Python?

## Example: Patent attorneys

As an illustration of workflow, we will load some data on patent attorneys, and then code their gender. We need to do a few things before we get started.

```mysql
create database `phd_patentsview` default character set utf8mb4 collate utf8mb4_bin;
```

Next, create a table to hold the data.

```mysql
drop table if exists phd_patentsview.rawlawyer;
create table phd_patentsview.rawlawyer (
uuid varchar(45) not null,
lawyer_id varchar(45) null,
patent_id varchar(20) null,
name_first varchar(100) null,
name_last varchar(100) null,
organization varchar(100) null,
country varchar(10) null,
sequence int(11) null,
primary key (uuid));
```

Now download the data, here: (http://www.patentsview.org/data/20171226/rawinventor.tsv.zip)

Next, load the data.

```mysql
load data local infile '~/Desktop/rawlawyer.tsv' 
  into table phd_patentsview.rawlawyer 
  fields 
     terminated by '\t' 
  lines terminated by '\n' 
  ignore 1 lines
  (@uuid,
   @lawyer_id,
   @patent_id,
   @name_first,
   @name_last,
   @organization,
   @country,
   @sequence)
   set uuid=if(@uuid='' or @uuid='NULL', null, @uuid),
       lawyer_id=if(@lawyer_id='' or @lawyer_id='NULL', null, @lawyer_id),
       patent_id=if(@patent_id='' or @patent_id='NULL', null, @patent_id),
       name_first=if(@name_first='' or @name_first='NULL', null, @name_first),
       name_last=if(@name_last='' or @name_last='NULL', null, @name_last),
       organization=if(@organization='' or @organization='NULL', null, @organization),
       country=if(@country='' or @country='NULL', null, @country),
       sequence=if(@sequence='' or @sequence='NULL', null, @sequence);
```

Finally, let's add an index to help speed things up.

```mysql
alter table phd_patentsview.rawlawyer add index name_first_idx (name_first);
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
from phd_patentsview.rawlawyer
where name_first is not null
group by name_first;
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

Once again, the code is too long to show in this note, but you can see it in a separate file, [here]().

## Part #3: Data processing

## How can we link R to MySQL?

## How can we link Stata to MySQL?


## Exercises for during the workshop

