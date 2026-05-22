import inspect

import pandas as pd
import pytest
from sqlalchemy import create_engine
import cx_Oracle
import logging


# Logging configuration
from common_utilities.utilities import *
from test_configuration.etlconfig import *

logging.basicConfig(
    filename="logs/extrcation_tests.log",
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO )
logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("connect_to_mysql_database")
class TestDataTransformation:
    validation_utility = ValidationUtility()

    def test_data_transformation_filter_sales(self,connect_to_mysql_database):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            expected_query = """
                              select * from stag_sales where sale_date >= '2025-09-10'
                              """
            actual_query = """
                            select *
                            from filtered_sales
                            """
            self.validation_utility.execute_validation(
                validation_type="DB_TO_DB",
                test_case_name=test_case_name,
                query_expected=expected_query,
                db_expected=connect_to_mysql_database,
                query_actual=actual_query,
                db_actual=connect_to_mysql_database
            )
        except Exception as e:
            logger.error(f"Error while validating filter transfromatio : {e}")

    def test_data_transformation_router_high_sales(self,connect_to_mysql_database):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            expected_query = """select * from filtered_sales where region='High'"""
            actual_query ="""select * from  high_sales"""
            self.validation_utility.execute_validation(
                validation_type="DB_TO_DB",
                test_case_name=test_case_name,
                query_expected=expected_query,
                db_expected=connect_to_mysql_database,
                query_actual=actual_query,
                db_actual=connect_to_mysql_database
            )
        except Exception as e:
            logger.error(f"Error while validating router - High transfromatio : {e}")

    def test_data_transformation_router_low_sales(self,connect_to_mysql_database):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            expected_query = """select * from filtered_sales where region='Low'"""
            actual_query ="""select * from  low_sales"""
            self.validation_utility.execute_validation(
                validation_type="DB_TO_DB",
                test_case_name=test_case_name,
                query_expected=expected_query,
                db_expected=connect_to_mysql_database,
                query_actual=actual_query,
                db_actual=connect_to_mysql_database
            )
        except Exception as e:
            logger.error(f"Error while validating router - Low transfromatio : {e}")


    # Assignments:
    def test_data_transformation_aggregator_sales(self, connect_to_mysql_database):
        pass

    def test_data_transformation_Joiner(self, connect_to_mysql_database):
        pass

    def test_data_transformation_aggregator_inventory(self, connect_to_mysql_database):
        pass