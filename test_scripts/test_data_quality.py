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
class TestDataQuality:
    validation_utility = ValidationUtility()
    data_quality_utility = DataQualityUtility

    def test_data_quality_duplicate_check_for_product_data_csv_file(self,connect_to_mysql_database):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            duplicate_status = self.data_quality_utility.check_duplicate_in_file("test_data/product_data_from_linux.csv","csv")
            print(duplicate_status)
            assert duplicate_status is True,"There are duplicate in the product file"
        except Exception as e:
            logger.error(f"error while performing duplicate check {e}")
