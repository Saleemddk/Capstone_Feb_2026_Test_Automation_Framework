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
    data_quality_utility = DataQualityUtility()
    file_utility = FileUtility()

    @pytest.mark.regression
    def test_data_quality_duplicate_check_for_product_data_csv_file(self,connect_to_mysql_database):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"test case : {test_case_name} started ...")
            duplicate_status = self.data_quality_utility.check_duplicate_in_file("test_data/product_data_from_linux.csv","csv")
            logger.info(f"Duplicate status is : {duplicate_status}")
            assert duplicate_status is True,"There are duplicate in the product file"
            logger.info(f"test case : {test_case_name} completed ...")
        except Exception as e:
            logger.error(f"error while performing duplicate check {e}")
            pytest.fail()

     # File existence check
    @pytest.mark.regression
    def test_data_quality_file_existence_of_product_data_csv_file(self):
                test_case_name = inspect.currentframe().f_code.co_name
                logger.info(f"test case : {test_case_name} started ...")
                try:
                    file_status = (self.file_utility.check_file_existence("test_data/product_data_from_linux.csv"))
                    assert file_status is True,"product_data.json file does not exist"
                    logger.info(f"test case : {test_case_name} completed ...")
                except Exception as e:
                    logger.error(f"error while performing file existence check {e}")
                    pytest.fail()


# Assignmnet : Implement below test cases
    def test_data_quality_file_existence_of_inventory_data_xml_file(self):
        pass

    def test_data_quality_file_existence_of_sales_data_file(self):
        pass

    def test_data_quality_file_existence_of_supplier_data_file(self):
        pass


    def test_data_quality_file_existence_of_product_data_csv_file(self):
        pass

    # File size check
    @pytest.mark.regression
    @pytest.mark.DataQuality
    @pytest.mark.smoke
    def test_data_quality_file_size_of_product_data_csv_file(self):
        try:
            file_size_status = (self.file_utility. check_file_size( "test_data/product_data_from_linux.csv") )
            assert file_size_status is True, \
                "sales_data.csv is empty"
        except Exception as e:
            logger.error(f"Error while checking file size : {e}")
            pytest.fail( "Error while checking file size")

    # Assignmnet : Implement below test cases
    @pytest.mark.DataQuality
    def test_data_quality_file_size_of_invenorty_data_xml_file(self):
        pass

    @pytest.mark.DataQuality
    def test_data_quality_file_size_of_supplier_data_json_file(self):
        assert 1==2,"failed"

    @pytest.mark.DataQuality
    def test_data_quality_file_size_of_sales_data_csv_file(self):
        pass