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
class TestDataExtraction:
    validation_utility = ValidationUtility()
    linux_utility = LinuxServerUtility()

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.order(5)
    def test_data_extraction_from_supplier_to_stage(self,connect_to_mysql_database):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            actual_query = """select * from stag_supplier"""
            self.validation_utility.execute_validation(
                validation_type="FILE_TO_DB",
                test_case_name = test_case_name,
                file_path="test_data/supplier_data.json",
                file_type="json",
                query_actual=actual_query,
                db_actual=connect_to_mysql_database)
        except Exception as e:
            logger.error(f"supplier data extrcation valodation failed {e}")

    @pytest.mark.order(3)
    def test_data_extraction_from_product_data_to_stage(self,connect_to_mysql_database):
            try:
                test_case_name = inspect.currentframe().f_code.co_name

                self.linux_utility.download_file_from_linux_server()
                # ABSTRACTION
                # download_file_from_linux_server()
                # Internal SSH/SFTP implementation
                # is hidden from test case

                actual_query = """
                                select *
                                from stag_product
                                """
                self.validation_utility.execute_validation(

                    validation_type="FILE_TO_DB",

                    test_case_name=test_case_name,

                    file_path="test_data/product_data_from_linux.csv",

                    file_type="csv",

                    query_actual=actual_query,

                    db_actual=connect_to_mysql_database
                )

            except Exception as e:

                logger.error(
                    f"Product data extraction validation failed : {e}"
                )

    @pytest.mark.smoke
    @pytest.mark.order(2)
    def test_data_extraction_from_store_table_data_to_stage(self,connect_to_oracle_database,connect_to_mysql_database):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            expected_query = """
                              select *
                              from stores
                              """
            actual_query = """
                            select *
                            from stag_stores
                            """
            self.validation_utility.execute_validation(
                validation_type="DB_TO_DB",
                test_case_name=test_case_name,
                query_expected=expected_query,
                db_expected=connect_to_oracle_database,
                query_actual=actual_query,
                db_actual=connect_to_mysql_database
            )
        except Exception as e:
            logger.error(f"Store data extraction validation failed : {e}")


  # Assignments
    @pytest.mark.order(4)
    def test_data_extraction_from_inventory_data_to_stage(self, connect_to_mysql_database):
        pass

    @pytest.mark.order(1)
    def test_data_extraction_from_sales_data_to_stage(self, connect_to_mysql_database):
        pass