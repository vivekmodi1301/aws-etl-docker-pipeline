import os
import boto3
import pandas as pd
import psycopg2
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def read_from_s3(bucket_name, file_key):
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        data = pd.read_csv(obj['Body'])
        return data
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {e}")
        return None
    except Exception as e: 
        print(f"Error reading from S3: {e}")
        return None

def push_to_rds(data, rds_config):
    try:
        conn = psycopg2.connect(**rds_config)
        cursor = conn.cursor()
        for index, row in data.iterrows():
            cursor.execute("INSERT INTO your_table (col1, col2) VALUES (%s, %s)", (row['col1'], row['col2']))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to push to RDS: {e}")
        return False
    return True

def push_to_glue(data, glue_database, glue_table, s3_output_bucket):
    try:
        temp_file_path = '/Users/vivekmodi/Desktop/AWS_ETL/data.csv'
        data.to_csv(temp_file_path, index=False)
        
        s3 = boto3.client('s3')
        s3.upload_file(temp_file_path, s3_output_bucket, 'data.csv')

        glue = boto3.client('glue')
        response = glue.start_crawler(Name='your-glue-crawler')

        print(f"Glue Crawler started: {response}")
        
    except Exception as e:
        print(f"Error pushing data to Glue: {e}")

def main():
    bucket_name = os.getenv('S3_BUCKET')
    file_key = os.getenv('FILE_KEY')
    rds_config = {
        'dbname': os.getenv('RDS_DB_NAME'),
        'user': os.getenv('RDS_USERNAME'),
        'password': os.getenv('RDS_PASSWORD'),
        'host': os.getenv('RDS_HOST'),
        'port': int(os.getenv('RDS_PORT', 5432))
    }
    glue_database = os.getenv('GLUE_DB')
    glue_table = os.getenv('GLUE_TABLE')
    s3_output_bucket = os.getenv('S3_OUTPUT_BUCKET')

    data = read_from_s3(bucket_name, file_key)
    if data is not None:
        success = push_to_rds(data, rds_config)
        if not success:
            push_to_glue(data, glue_database, glue_table, s3_output_bucket)

if __name__ == '__main__':
    main()
