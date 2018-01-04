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
To run the program, first create the views.

Then execute the program as `python log_analyis.py`. The output is written to the Terminal.

## Example Output
```
Top three favorite articles:
"Candidate is jerk, alleges rival" --- 338647
"Bears love berries, alleges bear" --- 253801
"Bad things gone, say good people" --- 170098
```
