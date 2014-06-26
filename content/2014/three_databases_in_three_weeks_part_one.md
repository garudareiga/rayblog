Title: Three Databases in Three Weeks Part I - PostgreSQL
Date: 2014-06-25 23:30
Author: Ray Chen
Category: Database 

PostgreSQL is a relational database management system. It's implemented as two-dimensional tables with data rows and strictly enforced column types. Unlike some other datastores, you needn't know how you plan to use the data. If a relational schema is normalized, queries are flexible.

## Day 1: Installation

We install PostgreSQL with contributed packages on Ubuntu 12.04. A list of contrib modules will be under the directory _/usr/share/postgresql/9.1/extension_.
```bash
$ sudo apt-get install postgresql postgresql-contrib
$ sudo /etc/init.d/postgresql start
```

Once we have Postgres installed, create a schema called _book_, and ensure our contrib packages have been installed correctly. We will use the _book_ schema for the rest of this post.
```bash
$ createdb book
$ psql book -c "CREATE EXTENSION tablefunc"
$ psql book -c "CREATE EXTENSION fuzzystrmatch"
$ psql book -c "CREATE EXTENSION pg_trgm"
$ psql book -c "CREATE EXTENSION cube"
$ psql book -c "CREATE EXTENSION dict_xsyn"
$ psql book -c "SELECT '1'::cube;"
 cube 
------
 (1)
(1 row)
```

## Day 2: Relations, CRUD, and Joins

Relational databases contain _relations (i.e., tables), which are sets of _tuples_ (i.e., rows), which map _attributes_ to atomic values. Creating a table consists of giving it a name and a list of columns with types and optional constraints. Postgres has a rich set of datatypes such as _text_ (a string of any length), _varchar(10)_ (a string of variable length up to 10 characters), and _char(2)_ (a string of exactly two characters). The __primary key__ disallow duplicate rows, and the __references__ keyword constrains field to another table's primary key, in order to maintain __referential integrity__.
```sql
ray=# create table countries (country_code char(2) primary key, country_name text unique);
ray=# create table cities (name text not null, postal_code varchar(10) check (postal_code <> ''),
ray(# country_code char(2) references countries, primary key (country_code, postal_code));
ray=# \dt
         List of relations
 Schema |   Name    | Type  | Owner 
--------+-----------+-------+-------
 public | cities    | table | ray
 public | countries | table | ray
(2 rows)

```

```sql
ray=# insert into countries (country_code, country_name)
ray-# values ('us', 'United States'), ('mx', 'Mexico'), ('au', 'Australia');
```