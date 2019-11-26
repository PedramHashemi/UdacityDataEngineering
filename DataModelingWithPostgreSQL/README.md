# Postgresql ETL

Creates the databases necessary for Analysis in Sparkify with a star shape.

## Datasets available

All the data are can be found in the folder `data`. The `log_data` is used to insert data into tables `user`, `songplay` and `date`.
The table `artists` is filled with data coming from `song_data` folder.


## Program Execution

A step by step series of examples that tell you how to get a development env running

Deleting the database and making new ones

```
python create_tables.py
```

then run the etl.py function to fill the rows.

```
python etl.py
```

## Schema Design
We have star shaped schema design with a fact table which is called `songplay` and 4 dimention tables `user`, `song`, `artist`, `time`. 

## Purpose of this database
This Database is a `OLAP` denormalized data base designed for analyis.

