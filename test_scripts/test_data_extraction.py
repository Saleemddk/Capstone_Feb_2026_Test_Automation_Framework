import inspect

import pandas as pd
import pytest
from sqlalchemy import create_engine
import cx_Oracle
import logging


# Logging configuration
from common_utilities.utilities import verify_expected_as_file_to_actual_as_database
from test_configuration.etlconfig import *

logging.basicConfig(
    filename="logs/extrcation_tests.log",
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO )
logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("connect_to_mysql_database")
class TestDataExtraction:

    def test_DE_between_source_supplier_file_to_target_as_staging(self,connect_to_mysql_database):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case name :{test_case_name}")
            logger.info(f"Test case {test_case_name} execution has started..")
            query_actual = """select * from stag_supplier"""
            verify_expected_as_file_to_actual_as_database\
                ("test_data/supplier_data.json","json", connect_to_mysql_database,query_actual,
                                                      test_case_name=test_case_name)
        except Exception as e:
            logger.error(f"Test case {test_case_name} execution has failed..")
            pytest.fail(f"Test case {test_case_name} execution has failed..")


'''    def test_DE_between_source_inventory_file_to_target_as_staging(self,connect_to_mysql_database):
        df_expected = pd.read_xml("test_data/inventory_data.xml", xpath=".//item")
        query_actual = """select * from stag_inventory"""
        df_actual = pd.read_sql(query_actual, connect_to_mysql_database)
        assert df_actual.equals(df_expected), "Inventory data did not extract correctly"


'''

