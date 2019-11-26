# Data Warehouse

### Purpose of the project:
- Save the log files in S3 bucket
- Make databases of the **events** and **songs** in amazon **redshift**
- Import the data from S3 logs and adding them to **events** and **songs** in parallel using **copy** command.
- Make A star shaped databse for analytics from **Events** and **Songs** tables to make.

### How to run the project

- make a cluster in redshift and make an IAM role, Add the IAM role to dwh.cfg file.
- run **create_tables.py** on shell
- run **etl.py** on the shell