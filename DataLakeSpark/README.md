# Data Lake

## What is Sparkify?
Sparkify is a music streaming website. It has some users and a database of all the logs and songs.

## Purpose of the Project
The purpose of this project is to use the log files to build an analytics database in this orders:

- save the logfiles in amazon S3
- access the log files with spark
- read the log files, process them into desired chunks and write them into s3 again.

## How to run the project?

add your AWS access and secret keys to dl.cfg file and run the code below:

~~~
python etl.py
~~~