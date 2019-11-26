import configparser
from datetime import datetime
import os, zipfile
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import TimestampType, DateType


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """ 
    This function gets the song_data and creates analytics tables song_table and artist_table
    
    parameters:
    spark: A spark session
    input_data: direction of raw data.
    output_data: direction where we want to save our new tables.
    
    """
    # get filepath to song data file
    song_data = os.path.join(input_data, "song_data/A/*/*/*.json")
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select("song_id", "title", "artist_id", "year", "duration")
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy('year', 'artist_id').parquet(output_data + "songs")

    # extract columns to create artists table
    artists_table = df.select("artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude")
    
    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(output_data + "artists")


def process_log_data(spark, input_data, output_data):
    """ 
    This function creates the rest of tables, users_table, time_table, songplays_table from the raw log data
    
    parameters:
    spark: spark session
    input_data: the raw log files to get the info
    ouput_data: the direction where we want to save our new tables.
    """
    # get filepath to log data file
    log_data = os.path.join(input_data, "log_data")

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table    
    users_table = df.select("userId", "firstName", "lastName", "gender", "level")
    
    # write users table to parquet files
    users_table.write.mode('overwrite').parquet(output_data + "users")

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda s: int(int(s)/1000.0), TimestampType())
    df = df.withColumn('timestamp', get_timestamp(df.ts))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda s: str(datetime.fromtimestamp(s/1000.0)), TimestampType())
    df = df.withColumn('datetime', get_datetime(df.ts))
    
    # extract columns to create time table
    time_table = df.select(
        df.datetime.alias('start_time'), 
        hour('datetime').alias('hour'),
        dayofmonth('datetime').alias('day'),
        weekofyear('datetime').alias('week'),
        month('datetime').alias('month'),
        year('datetime').alias('year')
        date_format('datetime', 'F').alias('weekday')
    )
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy('year', 'month').parquet(output_data + 'time_table')

    # read in song data to use for songplays table
    song_data = os.path.join(input_data, "song_data/A/*/*/*.json")
    song_df = spark.read.json(song_data)

    # extract columns from joined song and log datasets to create songplays table
    songplays_table = df.join(song_df,
                              (df.song == song_df.title) &
                              (df.artist == song_df.artist_name) &
                              (df.length == song_df.duration),
                              'left_outer').select(
        df.timestamp,
        col("userId").alias('user_id'),
        df.level,
        song_df.song_id,
        song_df.artist_id,
        col("sessionId").alias("session_id"),
        df.location,
        col("useragent").alias("user_agent"),
        year('datetime').alias('year'),
        month('datetime').alias('month')
    )

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode('overwrite').partitionBy('year', 'month').parquet(output_data + 'songplays')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = ""
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
