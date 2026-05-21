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






