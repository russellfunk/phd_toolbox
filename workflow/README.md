# Workflow

In this session, you'll learn how to __link MySQL to other tools,__ like Python, R, and Stata.

## What is workflow?
As you work more with tools like MySQL and Python, you'll start to see that they become most valuable __in combination__ with one another. I use the term __workflow__ to refer to the process of working across different tools to do things like __collect, clean, process, and analyze__ data.

## How can we link MySQL and Python?

## Example: Patent attorneys

As an illustration of workflow, we'll load some data on __patent attorneys__ and then code their __gender__. We need to do a few things before we get started. First, let's __create a database__.

```mysql
create database `phd_patentsview` default character set utf8mb4 collate utf8mb4_bin;
```

Next, __create a table__ to hold the data.

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

Now __download__ the data [here](http://www.patentsview.org/data/20171226/lawyer.tsv.zip). You can then use the code below to __load the data__ into MySQL. Note that you'll need to change the __file path__ to reflect where you downloaded the data.

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

Let's __add a column__ to store lawyer gender.

```mysql
alter table phd_patentsview.lawyer add column inventor_gender_gg varchar(45) null;
```

Finally, let's add a few __indexes__ to help speed things up.

```mysql
alter table phd_patentsview.lawyer add index name_first_idx (name_first),
                                   add index id_idx (id);
```


## Part #1: Data cleaning

Our goal is to code lawyer gender based on __first names__. To help facilitate that, let's first __create a new table__ that lets us focus on first names and set aside some of the other data in the table. We can __define a table__ with the following structure.

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

Now let's __add the data__ to the table.

```mysql
insert into phd_patentsview.lawyer_gender_coding (name_first, name_first_frequency)
select name_first, count(*)
from phd_patentsview.lawyer
where name_first is not null
group by name_first;
```

And we'll __add an index__ on first name to help speed things up later.

```mysql
alter table phd_patentsview.lawyer_gender_coding add index name_first_idx (name_first);
```

If we look at the resulting list of names, we'll notice that they're __quite messy__. See the table below for a few examples. 

| name_first_id | name_first                     | 
| ------------- | ------------------------------ |
| 20            | "Henry L. (""Bud"")"           | 
| 9326          | Hsiang-ning &#8220;Sean&#8221; |
| 18860         | Robert M?                      |

Before we try to run the gender coding, we'll want to __clean up the names__ a bit. I've written a simple Python script that will pull data from MySQL and do just that. It's too long to paste here, but you can view the whole script [here](https://github.com/russellfunk/phd_toolbox/blob/master/workflow/clean_lawyer_name.py).

## Part #2: Data collection

Now that we've cleaned our big list of first names, we'll want to collect some data on the __gender most commonly associated__ with each name. Typically, researchers do this by using publicly available data from [Social Security Administration records](https://www.ssa.gov/oact/babynames/index.html). Thankfully, several Python packages have been written that make this whole process much easier. We'll be using a package called [gender_guesser](https://pypi.org/project/gender-guesser/), which you can install by running the following command:

```
pip install gender-guesser
```

Once again, the code is __too long to show in this note,__ but you can see it in a separate file, [here](https://github.com/russellfunk/phd_toolbox/blob/master/workflow/code_lawyer_gender_gg.py).

After we have run the script to assign each name a probably gender, we'll want to __add that data back to the original lawyer data table__ so we can run some analyses (which we'll do next). You can do that by running the short query below.

```mysql
update phd_patentsview.lawyer t1,
       phd_patentsview.lawyer_gender_coding t2
set t1.inventor_gender_gg = t2.inventor_gender_gg
where t1.name_first = t2.name_first;
```

## How can we link R to MySQL?

Python is __just the beginning.__ You can also link MySQL to many other tools, including [R](https://www.r-project.org/), a popular, open source statistical environment. Probably the easiest way to link R to MySQL is through the __RMySQL library,__ which you can install using the following code.

```R
install.packages("RMySQL")
```

Once you have that installed, you can easily __pull data from MySQL__ to analyze in R.

```r
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

If you are running MySQL 8.0, and you have __trouble connecting to R,__ you can try running the following queries (updated to match your login information).

```mysql
alter user 'root'@'localhost' identified with mysql_native_password by '';
flush privileges;
```

## How can we link Stata to MySQL?

You can also __connect to MySQL using Stata,__ which has a nice [built in command](https://www.stata.com/manuals13/dodbc.pdf) called `odbc` designed exactly for this purpose. Before using the `odbc` command, though, you'll need to install [MySQL Connector/ODBC](https://dev.mysql.com/downloads/connector/odbc/).

Once you have that installed, you can __pull data directly into Stata__ from MySQL using the code below.

```stata
set odbcdriver ansi
#delimit ;
local sql_query 

select *
from phd_patentsview.lawyer;

#delimit cr
display in smcl as text "`sql_query'"
odbc load, exec("`sql_query'") conn("DRIVER={MySQL ODBC 5.3 Unicode Driver};SERVER=localhost;DATABASE=phd_patentsview;UID=root;PWD=;PORT=3306;")
```

You'll never use .csv or .dta files again!

![](https://github.com/russellfunk/phd_toolbox/blob/master/images/kool_aid.png)

# Further instructions on setting up ODBC on macOS

If you have trouble connecting to Stata on macOS, you may need to install [ODBC Administrator](https://support.apple.com/kb/DL895?locale=en_US).

You should see something like the configuration below.

![](https://github.com/russellfunk/phd_toolbox/blob/master/images/MACOS_ODBC_ADMIN_1.png)


# Further instructions on setting up ODBC on Windows

*Thanks to [Dennie Kim](http://denniekim.org/) for putting these instructions together!*

Once the MySQL Connector/ODBC plug-in is installed, you have to set up the specific MySQL server that you want to use. The instructions apply to the case where you are hosting data on your own local server/machine (i.e., localhost) but can be easily applied to remote servers.

In Windows, first use Windows search to find the ODBC Data Source Administrator:

![](https://github.com/russellfunk/phd_toolbox/blob/master/images/ODBC_SEARCH.png)

Once in the ODBC Administrator, click "Add..." to add a new data source connection.

![](https://github.com/russellfunk/phd_toolbox/blob/master/images/ODBC_ADMIN_1.png)

You should see a window like this:

![](https://github.com/russellfunk/phd_toolbox/blob/master/images/ODBC_ADMIN_2.png)

Be sure to select the MySQL ODBC option. If you have multiple versions of the ODBC connector installed (e.g., 5.3 and 8.0) be sure to select the one that matches the version of your MySQL server. For new users, the most likely case is MySQL 8.0. Hit "Finish" to proceed to the final step, where you'll see this window:

![](https://github.com/russellfunk/phd_toolbox/blob/master/images/ODBC_ADMIN_2.png)

In the "Data Source Name" field, give your ODBC connection a name that is easy to remember and descriptive. This is what you will use to call a specific connection in your Stata code. For example, if you want to set up a specific connection to the lawyer data we have been using, maybe you will name the connection "lawyer". The description can be whatever you want it to be to describe the data source--I usually just default to the Data Source Name if it's descriptive enough.

Next, in the TCP/IP Server field you have to specify the location of the server you want to access. In the case of your local server, it's easy--just type localhost. In the case of remote servers, you'll need the specific IP address or computer name. For example, if you want to connect to your UMN computer from a remote location, you'll need the IP address of your UMN computer. You can find this by going to the "System" item in the Control Panel and finding the "Full computer name." It should be xxx.ad.umn.edu

In most cases, unless you set up specific user accounts for your MySQL server, you can just type root in the "User" field. If you set up a password, enter that, as well. You can leave the Database blank if you will define the database in your Stata code (or if you will be working across multiple Databases). 

Finally, "Test" your connection to make sure that you can access it. A successful connection should test positively in just a few seconds. If your computer hangs up, there's something wrong. The most likely errors are that you have either incorrectly inputted the server/user/password fields, or your MySQL server is not running. 

![](https://github.com/russellfunk/phd_toolbox/blob/master/images/ODBC_ADMIN_3.png)
