
# psycopg2
# sqlalchemy
################################################################################################
import random
import string
import ast
import pandas as pd
import numpy as np
################################################################################################
from sqlalchemy import create_engine,Table,insert
import sqlalchemy as db
from tqdm import tqdm
################################################################################################
metadata_obj = db.MetaData()
################################################################################################
db_string = "postgresql://cuirpjup:WYeHTkTcEejgms44zAJqKFl25nSMCvbE@tyke.db.elephantsql.com/cuirpjup"
ENGINE  = create_engine(db_string)
TABLE_NAME_BIKE = "bikes"
TABLE_NAME_STATION = "stations"
TABLE_NAME_HISTORY_BIKE = "history_bike"
TABLE_NAME_HISTORY_STATION = "history_station"
DB_NAME = "cuirpjup"
################################################################################################
def add_bike(serial_number,maintenance_state,status):


    # SQL Query that allows to insert a record into the table
    query = f"""INSERT INTO {TABLE_NAME_BIKE} (serial_number,maintenance_state,status) VALUES ('{serial_number}',{maintenance_state},{status});"""


    ENGINE.execute(query)


    return None


def add_station(serial_number,maintenance_state,associated_bikes):

    # ast.literal_eval evaluate a string and makes it to a list (in this example)
    associated_bikes = ast.literal_eval(associated_bikes)
    
    # if there are bikes to add to the station
    if associated_bikes:

        # SQL Query that allows to insert a record into the table
        query = f"""INSERT INTO {TABLE_NAME_STATION} (serial_number,maintenance_state,associated_bikes) VALUES ('{serial_number}',{maintenance_state}, ARRAY {associated_bikes});"""

    else:
        # else if there isn't any bike => empty list add to this station
        query = f"""INSERT INTO {TABLE_NAME_STATION} (serial_number,maintenance_state,associated_bikes) VALUES ('{serial_number}',{maintenance_state}, ARRAY[]::text[]);"""

    ENGINE.execute(query)


    return None


def add_history_bike(date, operation_type, serial_number, maintenance_state_old, maintenance_state_new, status_old, status_new):
    # SQL Query that allows to insert a record into the table
    query = f"""INSERT INTO {TABLE_NAME_HISTORY_BIKE} (date,operation_type,serial_number,maintenance_state_old,
        maintenance_state_new,status_old,status_new) VALUES ('{date}','{operation_type}','{serial_number}',{maintenance_state_old},
        {maintenance_state_new},{status_old},{status_new});
    """

    ENGINE.execute(query)

    return None


def add_history_station(date, operation_type, serial_number, maintenance_state_old, maintenance_state_new, associated_bikes_old, associated_bikes_new):
    # associated_bikes_old = ast.literal_eval(associated_bikes_old)
    # associated_bikes_new = ast.literal_eval(associated_bikes_new)
    
    if associated_bikes_old:
        if associated_bikes_new:
            # SQL Query that allows to insert a record into the table
            query = f"""INSERT INTO {TABLE_NAME_HISTORY_STATION} (date,operation_type,serial_number,maintenance_state_old,
                maintenance_state_new,associated_bikes_old,associated_bikes_new) VALUES ('{date}','{operation_type}','{serial_number}',{maintenance_state_old},
                {maintenance_state_new}, ARRAY {associated_bikes_old}, ARRAY {associated_bikes_new});
            """
        elif not associated_bikes_new:
            query = f"""INSERT INTO {TABLE_NAME_HISTORY_STATION} (date,operation_type,serial_number,maintenance_state_old,
                maintenance_state_new,associated_bikes_old,associated_bikes_new) VALUES ('{date}','{operation_type}','{serial_number}',{maintenance_state_old},
                {maintenance_state_new}, ARRAY {associated_bikes_old}, ARRAY[]::text[]);
            """
    elif not associated_bikes_old:
        if associated_bikes_new:
            query = f"""INSERT INTO {TABLE_NAME_HISTORY_STATION} (date,operation_type,serial_number,maintenance_state_old,
                maintenance_state_new,associated_bikes_old,associated_bikes_new) VALUES ('{date}','{operation_type}','{serial_number}',{maintenance_state_old},
                {maintenance_state_new}, ARRAY[]::text[], ARRAY {associated_bikes_new});
            """
        elif not associated_bikes_new:
            query = f"""INSERT INTO {TABLE_NAME_HISTORY_STATION} (date,operation_type,serial_number,maintenance_state_old,
                maintenance_state_new,associated_bikes_old,associated_bikes_new) VALUES ('{date}','{operation_type}','{serial_number}',{maintenance_state_old},
                {maintenance_state_new}, ARRAY[]::text[], ARRAY[]::text[]);
            """
    
    
    ENGINE.execute(query)

    return None


def delete_bike(serial_number):

    # SQL Query that allows to insert a record into the table
    query = f"""DELETE FROM {TABLE_NAME_BIKE} WHERE serial_number = '{serial_number}';"""
    ENGINE.execute(query)

    return None


def delete_station(serial_number):

    # SQL Query that allows to insert a record into the table
    query = f"""DELETE FROM {TABLE_NAME_STATION} WHERE serial_number = '{serial_number}';"""
    ENGINE.execute(query)

    return None


def update_bike(serial_number,maintenance_state,status):
    '''
    We assume serial_number can not be modified. Only the bike maintenance state and status.
    '''
    # SQL Query that allows to insert a record into the table
    query = f"""UPDATE {TABLE_NAME_BIKE} SET maintenance_state = {maintenance_state},status={status} WHERE serial_number = '{serial_number}'"""
    ENGINE.execute(query)

    return None


def update_station(serial_number,maintenance_state,associated_bikes):
    '''
    We assume serial_number can not be modified. Only the bike maintenance state and associated bikes.
    '''

    # ast.literal_eval evaluate a string and makes it to a list (in this example)
    associated_bikes = ast.literal_eval(associated_bikes)

    # if there are bikes to add to the station
    if associated_bikes:
        # SQL Query that allows to insert a record into the table
        query = f"""UPDATE {TABLE_NAME_STATION} SET maintenance_state = {maintenance_state},associated_bikes=ARRAY {associated_bikes} WHERE serial_number = '{serial_number}'"""
    else:
        # no bike to add to the station => empty list
        query = f"""UPDATE {TABLE_NAME_STATION} SET maintenance_state = {maintenance_state},associated_bikes=ARRAY[]::text[] WHERE serial_number = '{serial_number}'"""
    ENGINE.execute(query)

    return None

def is_bike_in_db(serial_number):
    ''''
    Will return True or False to check whether the bike is in db or not
    '''

    # If the dictionary is not empty, it means the bike is in DB. Otherwise, it is not.
    return len(get_bike(serial_number)) > 0


def is_station_in_db(serial_number):
    ''''
    Will return True or False to check whether the station is in db or not
    '''

    # If the dictionary is not empty, it means the station is in DB. Otherwise, it is not.
    return len(get_station(serial_number)) > 0


def get_bike(serial_number):
    '''
    Given a serial number, return a dictionary with the relevant information.
    '''
    # get a dataframe from the database for the serial number bike given
    df = pd.read_sql_query(f"""select * from "{TABLE_NAME_BIKE}" where "serial_number" = '{serial_number}'""",con=ENGINE)
    number_of_rows, _ = df.shape

    # We return empty dic if no bike matches this serial number
    dic_info = {key:convert_type(df[key][0]) for key in df.columns} if number_of_rows else {}

    return dic_info


def get_station(serial_number):
    '''
    Given a serial number, return a dictionary with the relevant information.
    '''
    
    # get a dataframe from the database for the serial number bike given
    df = pd.read_sql_query(f"""select * from "{TABLE_NAME_STATION}" where "serial_number" = '{serial_number}'""",con=ENGINE)
    number_of_rows, _ = df.shape

    # We return empty dic if no bike matches this serial number
    dic_info = {key:convert_type(df[key][0]) for key in df.columns} if number_of_rows else {}

    return dic_info

def get_number_of_bikes():
    '''
    Returns number of bikes that are in the DB
    '''

    # get a dataframe from the database
    df = pd.read_sql_query(f'select count(*) from "{TABLE_NAME_BIKE}"',con=ENGINE)

    count = convert_type(df["count"][0])

    return count


def get_number_of_stations():
    '''
    Returns number of stations that are in the DB
    '''
    
    # get a dataframe from the database
    df = pd.read_sql_query(f'select count(*) from "{TABLE_NAME_STATION}"',con=ENGINE)

    count = convert_type(df["count"][0])

    return count


def convert_type(o):
    # value need to be converted when changes dataframe to dictionary (not json serializable) 
    if isinstance(o, np.int64): return int(o)  
    if isinstance(o, np.bool_): return bool(o)
    return o
    

def get_all_bikes():
    '''    
    Returns a dataframe of the database table    
    '''    

    # get all bikes in a dataframe
    df = get_df_from_db(TABLE_NAME_BIKE)
    number_of_rows, _ = df.shape    
    # We return empty dic if no bike is bound    
    dic_info = [{key:convert_type(df.iloc[k][key]) for key in df.columns} for k in range(len(df))] if number_of_rows else {}
    return dic_info
    

def get_all_station():
    '''    
    Returns a dataframe of the database table    
    '''    

    # get all stations in a dataframe
    df = get_df_from_db(TABLE_NAME_STATION)
    number_of_rows, _ = df.shape    
    # We return empty dic if no bike is bound    
    dic_info = [{key:convert_type(df.iloc[k][key]) for key in df.columns} for k in range(len(df))] if number_of_rows else {}
    return dic_info
    

def get_df_from_db(table_name):
    """ Function to get a dataframe from a database

    Args:
        table_name (string): name of the table where data are

    Returns:
        dataframe : df with all informations needed
    """
    df = pd.read_sql_query(f'select * from "{table_name}"',con=ENGINE)
    return df
  


def get_changes_between_dates_bikes(min_date,max_date):
    '''
    Given min and max dates, return a dictionary with the relevant information.
    '''

    # get a dataframe from database with informations between 2 dates provided
    df = pd.read_sql_query(f"""select * from "{TABLE_NAME_HISTORY_BIKE}" 
    where "date" between '{min_date}' and '{max_date}'""",con=ENGINE)
    number_of_rows, _ = df.shape

    # We return empty dic if no bike matches this serial number
    dic_info = df.to_dict('index')

    return dic_info


def get_changes_between_dates_stations(min_date,max_date):
    '''
    Given min and max dates, return a dictionary with the relevant information.
    '''

    # get a dataframe from database with informations between 2 dates provided
    df = pd.read_sql_query(f"""select * from "{TABLE_NAME_HISTORY_STATION}" 
    where "date" between '{min_date}' and '{max_date}'""",con=ENGINE)
    number_of_rows, _ = df.shape

    # We return empty dic if no bike matches this serial number
    dic_info = df.to_dict('index')

    return dic_info
################################################################################################
