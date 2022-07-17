
# psycopg2
# sqlalchemy
################################################################################################
import random
import string
import pandas as pd
################################################################################################
from sqlalchemy import create_engine,Table,insert
import sqlalchemy as db
from tqdm import tqdm
################################################################################################
metadata_obj = db.MetaData()
################################################################################################
db_string = "postgresql://cuirpjup:WYeHTkTcEejgms44zAJqKFl25nSMCvbE@tyke.db.elephantsql.com/cuirpjup"
ENGINE  = create_engine(db_string)
TABLE_NAME = "bikes"
DB_NAME = "cuirpjup"
################################################################################################
def add_bike(serial_number,maintenance_state,status):


    # SQL Query that allows to insert a record into the table
    query = f"""INSERT INTO {TABLE_NAME} (serial_number,maintenance_state,status) VALUES ('{serial_number}',{maintenance_state},{status});"""


    ENGINE.execute(query)


    return None



def delete_bike(serial_number):

    # SQL Query that allows to insert a record into the table
    query = f"""DELETE FROM {TABLE_NAME} WHERE serial_number = '{serial_number}';"""
    ENGINE.execute(query)

    return None


def update_bike(serial_number,maintenance_state,status):
    '''
    We assume serial_number can not be modified. Only the bike maintenance state and status.
    '''
    # SQL Query that allows to insert a record into the table
    query = f"""UPDATE {TABLE_NAME} SET maintenance_state = {maintenance_state},status={status} WHERE serial_number = '{serial_number}'"""
    ENGINE.execute(query)

    return None


def is_bike_in_db(serial_number):
    ''''
    Will return True or False to check whether the bike is in db or not
    '''

    # If the dictionary is not empty, it means the bike is in DB. Otherwise, it is not.
    return len(get_bike(serial_number)) > 0

def get_bike(serial_number):
    '''
    Given a serial number, return a dictionary with the relevant information.
    '''

    df = pd.read_sql_query(f"""select * from "{TABLE_NAME}" where "serial_number" = '{serial_number}'""",con=ENGINE)
    number_of_rows, _ = df.shape

    # We return empty dic if no bike matches this serial number
    dic_info = {key:df[key][0] for key in df.columns} if number_of_rows else {}

    return dic_info

def get_number_of_bikes():
    '''
    Returns number of bikes that are in the DB
    '''

    df = pd.read_sql_query(f'select count(*) from "{TABLE_NAME}"',con=ENGINE)

    count = df["count"][0]

    return count

def get_all_bikes():
    '''
    Returns a dataframe of the database table
    '''

    df = get_df_from_db(TABLE_NAME)


    return df

def get_df_from_db(table_name):
    df = pd.read_sql_query(f'select * from "{table_name}"',con=ENGINE)
    return df




    
################################################################################################



