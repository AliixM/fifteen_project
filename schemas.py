from pydantic import BaseModel
from enum import IntEnum, Enum
################################################################################################

# enum classes
class State(IntEnum):
    """ 
    Enumerate class for the different states of the bike
    """
    CASSE = 1
    NEUF = 2
    BON_ETAT = 3


class Operation(str, Enum):
    """
    Enum class for the different types of operations (CRUD)
    """
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


# pydantic models
class Bike(BaseModel):
    """ Class that describes bike

    Args:
        serial_number (string): bike identifier 
        status (boolean): bike is rented or not by a client
        maintenance_state (integer): see if the bike is in good condition or not
    """
    serial_number : str
    status : bool
    maintenance_state : State

    # to prevent the user from typing too long serial number
    class Config:
        max_anystr_length = 10
        error_msg_templates = {
            'value_error.any_str.max_length': 'max_length:{limit_value}',
        }



class Station(BaseModel):
    """ Class that describes station

    Args:
        serial_number (string) : station identifier
        maintenance_state (integer): station is in good condition or not
        associated_bikes (list of bikes) : list of bikes associated to the station
    """
    serial_number : str
    maintenance_state : State
    associated_bikes : list[Bike]

    # to prevent the user from typing too long serial number
    class Config:
        max_anystr_length = 10
        error_msg_templates = {
            'value_error.any_str.max_length': 'max_length:{limit_value}',
        }

################################################################################################

if __name__ == '__main__':

    # ----------------------------- examples -----------------------------

    velo = Bike(serial_number="CH45RT", status=0, maintenance_state=State.BON_ETAT)
    velo2 = Bike(serial_number="AB124GG", status=0, maintenance_state=State.CASSE)
    velo3 = Bike(serial_number="1478HGT", status=1, maintenance_state=State.NEUF)

    stat = Station(serial_number="456", maintenance_state=State.CASSE, associated_bikes=[velo, velo2, velo3])

    # print(velo.dict())