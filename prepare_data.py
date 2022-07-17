################################################################################################
import random
import string
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
from postgresql_funcs import add_bike, get_all_bikes, add_station
################################################################################################
def create_table_bike():
    '''
    Allows to create the bike database  
    '''
    # database name
    profile = db.Table(
        TABLE_NAME_BIKE,                                        
        metadata_obj,                                    
        db.Column('serial_number', db.String, primary_key=True),  
        db.Column('maintenance_state', db.Integer),                    
        db.Column('status', db.Boolean),                
    )

    # Create the profile table
    metadata_obj.create_all(ENGINE)

    return None


def create_table_station():
    '''
    Allows to create the station database  
    '''
    # database name
    profile = db.Table(
        TABLE_NAME_STATION,                                        
        metadata_obj,                                    
        db.Column('serial_number', db.String, primary_key=True),  
        db.Column('maintenance_state', db.Integer),                    
        db.Column('associated_bikes', db.ARRAY(db.String)),                
    )

    # Create the profile table
    metadata_obj.create_all(ENGINE)

    return None


def create_history_bike_table():
    '''
        Allows to create the history table for bikes  
    '''
    profile = db.Table(
        TABLE_NAME_HISTORY_BIKE,
        metadata_obj,
        db.Column('operation_id', db.Integer, primary_key=True, autoincrement=True),
        db.Column('date', db.Date),
        db.Column('operation_type', db.String),
        db.Column('serial_number', db.String),
        db.Column('maintenance_state_old', db.Integer),
        db.Column('maintenance_state_new', db.Integer),
        db.Column('status_old', db.Boolean),
        db.Column('status_new', db.Boolean)
    )

    # Create the profile table
    metadata_obj.create_all(ENGINE)

    return None


def create_history_station_table():
    '''
        Allows to create the history table for  stations
    '''
    profile = db.Table(
        TABLE_NAME_HISTORY_STATION,
        metadata_obj,
        db.Column('operation_id', db.Integer, primary_key=True, autoincrement=True),
        db.Column('date', db.Date),
        db.Column('operation_type', db.String),
        db.Column('serial_number', db.String),
        db.Column('maintenance_state_old', db.Integer),
        db.Column('maintenance_state_new', db.Integer),
        db.Column('associated_bikes_old', db.ARRAY(db.String)),
        db.Column('associated_bikes_new', db.ARRAY(db.String))
    )

    # Create the profile table
    metadata_obj.create_all(ENGINE)

    return None


def generate_random_serial_number():
    '''
    Generates a random serial number string.
    Random serial number. Three letters + 7 numbers.
    '''
    
    serial_number = "".join([random.choice(string.ascii_letters.upper()) for k in range(3)] + [str(int(random.random()*10)) for k in range(7)])

    return serial_number


def generate_random_data_bike():
    '''
    Function that allows to generate random records for the bike database    
    '''

    # We decide to add 1000 random records to the bike database
    N = 1000

    for k in tqdm(range(N)):
        
        # Random integer in [1,2,3]
        maintenance_state = int(random.random()*3) + 1

        # Random status in [False,True]
        status = bool(int(random.random()*2))

        # Random serial number. Three letters + 7 numbers.
        serial_number = generate_random_serial_number()

        
        # Adding the new bike information to the DB.
        add_bike(serial_number,maintenance_state,status)

    return None


def generate_random_data_station():
    '''
    Function that allows to generate random records for the station database    
    '''

    # We decide to add 50 random records to the station database
    N = 50
    MAX_BIKES = 10
    # create history
    history = set()

    for k in tqdm(range(N)):

        # available bikes are bikes that are not already associated with a station
        # not in history
        available_bikes = [bike["serial_number"] for bike in get_all_bikes() if not bike["serial_number"] in history]

        # Random integer in [1,2,3]
        maintenance_state = int(random.random()*3) + 1

        # Random bike in available bikes
        # min(MAX_BIKES, len(available_bikes)) avoid prevents stations from having too many bikes associated with them
        # maximum 10 bikes per station
        associated_bikes_number = int(random.random()*min(MAX_BIKES, len(available_bikes)))

        # choose randomly bikes
        associated_bikes = random.sample(available_bikes, associated_bikes_number)

        # Random serial number. Three letters + 7 numbers.
        serial_number = generate_random_serial_number()

        # add to history bikes that were selected
        for k in associated_bikes:
            history.add(k)
        
        # Adding the new station information to the DB.
        add_station(serial_number,maintenance_state,associated_bikes)

    
    return None

################################################################################################


if __name__ == "__main__":

    # Create tables for the database : bike, station, history_statio, history_bike

    # create_table_bike()
    generate_random_data_bike()

    # create_table_station()
    # generate_random_data_station()

    # create_history_station_table()
    # create_history_bike_table()