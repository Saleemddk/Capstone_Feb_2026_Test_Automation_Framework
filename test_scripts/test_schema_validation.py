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
class TestSchemaValidation:
    validation_utility = ValidationUtility()
    schema_validation = SchemaValidationUtility()

    def test_fact_sales_table_schema_column_names(self,connect_to_mysql_database):
        try:
            expected_columns = ['sales_id', 'product_id', 'store_id', 'quantity', 'total_sales', 'sale_date']
            schema_validation.validate_column_names(
                engine = connect_to_mysql_database,
                table_name = "fact_sales",
                expected_columns = expected_columns
            )
            logger.info("Schema validation check for column_names completed successfully")
        except Exception as e:
            logger.error(f"Schema validation check for column_names {e}")

    def test_fact_sales_table_schema_data_types(self, connect_to_mysql_database):
            try:
                expected_datatypes = {
                    'sales_id':["int64"],
                    'product_id' :["int64"],
                    'store_id' :["int64"],
                    'quantity':["int64"] ,
                    'total_sales':["float64"],
                    'sale_date':["object"]
                }

                schema_validation.validate_column_datatypes(
                    engine=connect_to_mysql_database,
                        table_name = "fact_sales",
                                     expected_datatypes = expected_datatypes
                )
                logger.info("Schema data types check for column_names completed successfully")
            except Exception as e:
                logger.error(f"Schema data types check for fact_sales {e}")


    # Assignment : Columns names validation

    def test_fact_inventory_table_schema_column_names(self, connect_to_mysql_database):
        pass

    def test_monthly_sales_summary_table_schema_column_names(self, connect_to_mysql_database):
        pass

    def test_inventory_level_by_stores_table_schema_column_names(self, connect_to_mysql_database):
        pass

    # Assignment : Columns data types validation
    def test_fact_inventory_table_schema_data_types(self, connect_to_mysql_database):
        pass

    def test_monthly_sales_summary_table_schema_data_types(self, connect_to_mysql_database):
        pass

    def test_inventory_level_by_stores__table_schema_data_types(self, connect_to_mysql_database):
        pass


    def test_data_quality_referential_check_for_product_id_between_child_fact_sales_and_parent_stag_product(self,connect_to_mysql_database):
        try:
            foreign_query = """select *from fact_sales"""
            primary_query = """select *from stag_product"""
            df_not_matched = (self.schema_validation.check_referential_integrity(
                    source_db_conn=connect_to_mysql_database,
                    target_db_conn=connect_to_mysql_database,
                    foreign_query=foreign_query,
                    primary_query=primary_query,
                    key_column="product_id",
                    csv_path=("differences/foreign_key_not_matching.csv")))
            assert df_not_matched.empty is True, \
                "Foreign key validation failed"
        except Exception as e:
            logger.error(f"Error while performing referential integrity check : {e}")
            pytest.fail( "Error while performing referential integrity check")


    # Complete the assignmnet : Implement other referential integrity tests but not limited to below
    def test_data_quality_referential_check_for_sales_id_between_child_fact_sales_and_parent_stag_sales(self,connect_to_mysql_database):
        pass

    def test_data_quality_referential_check_for_store_id_between_child_fact_sales_and_parent_stag_stores(self,                                                                                            connect_to_mysql_database):
        pass