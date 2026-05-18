from io import StringIO
import pytest
import boto3
import pandas as pd
from sqlalchemy import create_engine
import cx_Oracle
import logging
import paramiko

# Logging configuration
from test_configuration.etlconfig import *

from test_configuration.etlconfig import *

logging.basicConfig(
    filename="application_logs/etljob.log",
    filemode='a',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO )
logger = logging.getLogger(__name__)

def verify_expected_as_file_to_actual_as_database(file_path,file_type,db_engine_actual,query_actual,test_case_name):
    try:
        if file_type =='csv':
            df_expected = pd.read_csv(file_path)
        elif file_type =='json':
            df_expected = pd.read_json(file_path)
        elif file_type =='xml':
            df_expected = pd.read_xml(file_path,xpath=".//item")
        else:
            raise ValueError(f"unsupported file type passed {file_type}")
        logger.info(f"Expected data from the file is {df_expected}")

        query_actual = """select * from stag_supplier"""
        df_actual = pd.read_sql(query_actual,db_engine_actual)
        logger.info(f"Actual data from the databse is {df_actual}")

        # Find extra / non matching rows in expected dataframe
        df_extra_in_expected = df_expected[~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))]
        df_extra_in_expected.to_csv(f"Differences/extra_rows_in_expected_{test_case_name}.csv",index=False)
        assert df_extra_in_expected.empty, f"There are extra rows in expected {df_extra_in_expected}"

        # Assigment : Find extra / non matching rows in actual dataframe
        # Assertion for extra rows in actual data

    except Exception as e:
        logger.error(f"there is exception raised while check{e}")
        pytest.fail()









def download_file_from_linux():
    logger.info("product file download from linux server has started...")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(LIUNX_HOSTNAME,username=LIUNX_USERNAME,password=LIUNX_PASSWORD)
    sftp = ssh_client.open_sftp()
    sftp.get(REMOTE_FILE_PATH,LOCAL_FILE_PATH)
    sftp.close()
    logger.info("product file download from linux server has completed...")


# initialize the connection
s3 = boto3.client("s3")
def read_file_from_s3_and_write_to_database(bucket_name,file_key):
    # fetch the csv file from S3
    try:
        response = s3.get_object(Bucket=bucket_name,Key=file_key)
        csv_content = response['Body'].read().decode('utf-8')
        data = StringIO(csv_content)
        df = pd.read_csv(data)
        return df
    except Exception as e:
        logger.error(f"exception raised while reading from S3 {e}", exc_info=True)


