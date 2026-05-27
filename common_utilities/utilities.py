from io import StringIO
import pytest
import boto3
import pandas as pd
from sqlalchemy import create_engine
import cx_Oracle
import logging
import paramiko
from test_configuration.etlconfig import *
import os


logging.basicConfig(
    filename="application_logs/etljob.log",
    filemode='a',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO )
logger = logging.getLogger(__name__)

# Base Utility class

class BaseUtility:
    # usage of encapsulation
    def __read_file(self,file_path,file_type):
        if file_type =='csv':
            df = pd.read_csv(file_path)
        elif file_type =='json':
            df = pd.read_json(file_path)
        elif file_type == 'xml':
            df= pd.read_xml(file_path,xpath=".//item")
        else:
            raise ValueError(f"unsupported file type passed {file_type}")
        return df

    # Abstraction
    def read_file(self,file_path,file_type):
        return self.__read_file(file_path,file_type)

    def log_info(self,message):
        logger.info(message)

    def log_error(self,message):
        logger.error(message)

# Inheritance
class ValidationUtility(BaseUtility):

    # Polymorphism
    def execute_validation(self,validation_type,test_case_name,query_actual=None,db_actual=None,file_path=None,file_type=None,query_expected=None,db_expected=None,bucket_name=None,file_key=None):
        if validation_type=="FILE_TO_DB":
            self.validate_file_to_db(test_case_name,file_path,file_type,query_actual,db_actual)
        elif validation_type=='DB_TO_DB':
            self.validate_db_to_db(test_case_name,query_expected,db_expected,query_actual,db_actual)
        elif validation_type=='S3_TO_DB':
            self.validate_s3_to_db(test_case_name,bucket_name,file_key,query_actual,db_actual)


    # File to database validation
    def validate_file_to_db(self,test_case_name,file_path,file_type,query_actual,db_actual):
        try:
            df_expected = self.read_file(file_path,file_type).astype(str)
            logger.info(f"expected data {df_expected}")

            df_actual = pd.read_sql(query_actual,db_actual).astype(str)
            logger.info(f"actual data {df_actual}")

            # expected minus actual
            df_extra_expected = df_expected[~df_expected.apply(tuple,axis=1).isin(df_actual.apply(tuple,axis=1))]
            df_extra_expected.to_csv(f"differences/extra_row_expected_{test_case_name}.csv",index=False)

            # actual minus expected
            df_extra_actual = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]
            df_extra_actual.to_csv(f"differences/extra_row_actual_{test_case_name}.csv", index=False)

            # assertion
            assert df_actual.equals(df_expected),f"{test_case_name} failed"
            logger.info(f"{test_case_name} passed")

        except Exception as e:
            logger.error(f"{test_case_name} validation failed : {e}")
            pytest.fail()

# File to database validation
    def validate_file_to_db(self, test_case_name, file_path, file_type, query_actual, db_actual):
            try:
                df_expected = self.read_file(file_path, file_type).astype(str)
                logger.info(f"expected data {df_expected}")

                df_actual = pd.read_sql(query_actual, db_actual).astype(str)
                logger.info(f"actual data {df_actual}")

                # expected minus actual
                df_extra_expected = df_expected[~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))]
                df_extra_expected.to_csv(f"differences/extra_row_expected_{test_case_name}.csv", index=False)

                # actual minus expected
                df_extra_actual = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]
                df_extra_actual.to_csv(f"differences/extra_row_actual_{test_case_name}.csv", index=False)

                # assertion
                assert df_actual.equals(df_expected), f"{test_case_name} failed"
                logger.info(f"{test_case_name} passed")

            except Exception as e:
                logger.error(f"{test_case_name} validation failed : {e}")
                pytest.fail()


    # Database to database validation
    def validate_db_to_db(self, test_case_name, query_expected, db_expected, query_actual, db_actual):
            try:

                df_expected = pd.read_sql(query_expected, db_expected).astype(str)
                logger.info(f"actual data {df_expected}")


                df_actual = pd.read_sql(query_actual, db_actual).astype(str)
                logger.info(f"actual data {df_actual}")

                # expected minus actual
                df_extra_expected = df_expected[
                    ~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))]
                df_extra_expected.to_csv(f"differences/extra_row_expected_{test_case_name}.csv", index=False)

                # actual minus expected
                df_extra_actual = df_actual[
                    ~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]
                df_extra_actual.to_csv(f"differences/extra_row_actual_{test_case_name}.csv", index=False)

                # assertion
                assert df_actual.equals(df_expected), f"{test_case_name} failed"
                logger.info(f"{test_case_name} passed")

            except Exception as e:
                logger.error(f"{test_case_name} validation failed : {e}")
                pytest.fail()

# S3 to database validation
    def validate_s3_to_db(self, test_case_name,bucket_name,file_key, query_actual, db_actual):
            try:
                df_expected = self.read_file_from_s3(bucket_name,file_key).astype(str)
                logger.info(f"expected data {df_expected}")

                df_actual = pd.read_sql(query_actual, db_actual).astype(str)
                logger.info(f"actual data {df_actual}")

                # expected minus actual
                df_extra_expected = df_expected[
                    ~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))]
                df_extra_expected.to_csv(f"differences/extra_row_expected_{test_case_name}.csv", index=False)

                # actual minus expected
                df_extra_actual = df_actual[
                    ~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]
                df_extra_actual.to_csv(f"differences/extra_row_actual_{test_case_name}.csv", index=False)

                # assertion
                assert df_actual.equals(df_expected), f"{test_case_name} failed"
                logger.info(f"{test_case_name} passed")

            except Exception as e:
                logger.error(f"{test_case_name} validation failed : {e}")
                pytest.fail()


    def read_file_from_s3(self,bucket_name,file_key):
        try:
            logger.info("Reading file from S3")
            s3 = boto3.client("s3")
            response = s3.get_object(Bucket = bucket_name, Key = file_key)
            csv_content = response["Body"].read().decode("utf-8")
            file_data = StringIO(csv_content)
            df = pd.read_csv(file_data)
            return df
        except Exception as e:
            logger.error(f"S3 file read failed {e}")

# LINUX SERVER UTILITY CLASS
class LinuxServerUtility(BaseUtility):

    def download_file_from_linux_server(self):
        try:
            logger.info(
                "Linux file download started"
            )
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )
            ssh_client.connect(LIUNX_HOSTNAME,username=LIUNX_USERNAME,password=LIUNX_PASSWORD)
            sftp = ssh_client.open_sftp()
            sftp.get(REMOTE_FILE_PATH,LOCAL_FILE_PATH)
            sftp.close()
            logger.info( "Linux file download completed")
        except Exception as e:
            logger.error(f"Linux file download failed : {e}")
        finally:
            logger.info( "Finally block executed" )

class DataQualityUtility(BaseUtility):

    # Duplicate checks
    def check_duplicate_in_file(self,file_path,file_type):
        try:
            df = self.read_file(file_path,file_type)
            if df.duplicated().any():
                return False
            return True
        except Exception as e:
            logger.error(f"Duplicate check failed : {e}")

    # Assignment:
    def check_duplicate_in_database(self,db_name,query):
        pass

    def check_duplicate_for_specific_column_in_file(self, file_path, file_type,column_name):
        try:
            df = self.read_file(file_path, file_type)
            if df[column_name].duplicated().any():
                return False
            return True
        except Exception as e:
            logger.error(f"Column Duplicate check failed : {e}")

    # Assignment:
    def check_duplicate_for_specific_column_in_database(self,db_name,query,column_name):
        pass



     # Null value checks
    def check_null_values_in_file(self, file_path, file_type):
        try:
            df = self.read_file(file_path, file_type)
            if df.isnull().values().any():
                return False
            return True
        except Exception as e:
            logger.error(f"Null value check failed : {e}")

    def check_null_values_for_specific_column(self, file_path, file_type,column_name):
        try:
            df = self.read_file(file_path, file_type)
            if df[column_name].isnull().values().any():
                return False
            return True
        except Exception as e:
            logger.error(f"Column - Null value check failed : {e}")


        # Assignment:
    def check_null_in_database(self, db_name, query):
        pass

    def check_null_for_specific_column_in_database(self, db_name, query, column_name):
        pass


# FILE UTILITY CHECKS

class FileUtility(BaseUtility):
    def check_file_existence(self,file_path):
        try:
            return os.path.isfile(file_path)
        except Exception as e:
            logger.error(f"File existence check fails {e}")

    def check_file_size(self, file_path):
        try:
            return os.path.getsize(file_path)>0
        except Exception as e:
            logger.error(f"File size check fails {e}")


class SchemaValidationUtility(BaseUtility):
    def validate_column_names(self,engine,table_name,expected_columns):
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query,engine)
        actual_columns = list(df.columns)
        assert actual_columns == expected_columns,(
            f"\nColumn mismatch in table {table_name}"
            f"\expected cplumns: {expected_columns}"
            f"\actual cplumns: {actual_columns}"
        )

    def validate_column_datatypes(self,engine,table_name,expected_datatypes):
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query,engine)
            for column_name,allowed_datatypes in expected_datatypes.item():
                actual_data_type = df[column_name].dtype
                assert actual_data_type in allowed_datatypes,(
                    f"\ndataype mismatch in table {table_name}"
                    f"\Column: {column_name}"
                    f"\actual datatype: {actual_data_type}"
                    f"\expected datatype: {allowed_datatypes}"
                )
   
    def check_referential_integrity(
                self,
                source_db_conn,
                target_db_conn,
                foreign_query,
                primary_query,
                key_column,
                csv_path):
            try:
                foreign_df = pd.read_sql(foreign_query, source_db_conn)
                primary_df = pd.read_sql(primary_query,target_db_conn)
                df_not_matched = foreign_df[~foreign_df[key_column].isin(primary_df[key_column])]
                df_not_matched.to_csv(csv_path,index=False)
                return df_not_matched
            except Exception as e:
                logger.error(f"Referential Integerity check fails {e}")
