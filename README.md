# Log Analysis

## Description
Log Analysis project for the Udacity Full Stack Nanodegree. The project consists of answering three questions given a database and data.

## Prerequisites
- Python 2
- PostgreSQL

## Installing
To create an environment to run the project, install Vagrant and Virtual Box following the instructions from Udacity.

Start the Virtual Machine(VM) by running `vagrant up` in the directory that contains the "Vagrantfile" and then SSH into the VM using `vagrant ssh`. Navigate to `/vagrant` to access the files shared between the VM and your computer.

Create the schema and load the data by running `psql -d news -i newsdata.sql`. The "newsdata.sql" file
contains the SQL commands to create the schema and load data into the tables.

Note: When done with the VM, type exit and then `vagrant suspend` to pause the VM.

## Running the Program
To run the program, first create the views. These views are created in the `analyze_logs.py` file. For completeness, below are the VIEW statements.

- Create View of Popular Articles
```
CREATE OR REPLACE VIEW favorite_articles as \
    SELECT distinct(count(log.path)) as page_views, log.path \
    FROM log \
    WHERE log.status = '200 OK' \
    and log.path like '/article/%' \
    GROUP BY log.path \
    ORDER BY page_views desc
```

- Create a view of total calls per day.
```
CREATE OR REPLACE VIEW total_calls_per_day as
    SELECT COUNT(*) as all_calls, date_trunc('day', log.time) as date
    FROM log
    GROUP BY date;
```

- Create a view of failed calls per day.
```
CREATE OR REPLACE VIEW failed_calls_per_day as
    SELECT COUNT(*) as failed_calls, date_trunc('day', log.time) as date
    FROM log
    WHERE status != '200 OK'
    GROUP BY date;
```

- Create a view of the percentage of failed calls per day.
```
CREATE OR REPLACE VIEW percent_failed_calls as
    SELECT round((f.failed_calls/t.all_calls*1.0)*100, 1)
    as per_failed_calls, f.date
    FROM failed_calls_per_day as f, total_calls_per_day as t
    WHERE f.date=t.date;
```


Then execute the program as `python analyze_logs.py`. The output is written to the Terminal.

## Example Output
```
Top three favorite articles:
"Candidate is jerk, alleges rival" --- 338647
"Bears love berries, alleges bear" --- 253801
"Bad things gone, say good people" --- 170098
```
