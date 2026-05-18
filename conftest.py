import pandas as pd
import pytest
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

@pytest.fixture()
def connect_to_mysql_database():
    logger.info("Mysql databse connection is being established..")
    mysql_engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}").connect()
    logger.info("Mysql databse connection has been successfully established..")
    yield mysql_engine
    mysql_engine.close()
    logger.info("Mysql databse connection has been closed..")


@pytest.fixture()
def connect_to_oracle_database():
    logger.info("Oracle databse connection is being established..")
    oracle_engine = create_engine(
        f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}").connect()
    logger.info("Oracle databse connection has been successfully established..")
    yield oracle_engine
    oracle_engine.close()
    logger.info("Oracle databse connection has been closed..")





