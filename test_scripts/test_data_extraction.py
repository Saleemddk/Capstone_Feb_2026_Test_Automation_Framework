import pandas as pd
from sqlalchemy import create_engine
import cx_Oracle
import logging


# Logging configuration
from test_configuration.etlconfig import *

logging.basicConfig(
    filename="logs/extrcation_tests.log",
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO )
logger = logging.getLogger(__name__)


# database connection
oracle_engine = create_engine(f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}")
mysql_engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")


class TestDataExtraction:

    def test_DE_between_source_supplier_file_to_target_as_staging(self):
        df_expected = pd.read_json("test_data/supplier_data.json")
        query_actual = """select * from stag_supplier"""
        df_actual= pd.read_sql(query_actual,mysql_engine)
        assert df_actual.equals(df_expected),"Supplier data did not extract correctly"


    def test_DE_between_source_inventory_file_to_target_as_staging(self):
        df_expected = pd.read_xml("test_data/inventory_data.xml", xpath=".//item")
        query_actual = """select * from stag_inventory"""
        df_actual = pd.read_sql(query_actual, mysql_engine)
        assert df_actual.equals(df_expected), "Inventory data did not extract correctly"



