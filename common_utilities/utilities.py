from io import StringIO
import pytest
import boto3
import pandas as pd
from sqlalchemy import create_engine
import cx_Oracle
import logging
import paramiko
from test_configuration.etlconfig import *


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
