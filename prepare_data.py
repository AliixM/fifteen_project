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
TABLE_NAME = "bikes"
DB_NAME = "cuirpjup"
################################################################################################
from postgresql_funcs import add_bike
################################################################################################
def create_table_bike():
    '''
    Allows to create the bike database  
    '''
    # database name
    profile = db.Table(
        TABLE_NAME,                                        
        metadata_obj,                                    
        db.Column('serial_number', db.String, primary_key=True),  
        db.Column('maintenance_state', db.Integer),                    
        db.Column('status', db.Boolean),                
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

    # We decide to add 100 random records to the bike database
    N = 100

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

################################################################################################


if __name__ == "__main__":

    generate_random_data_bike()