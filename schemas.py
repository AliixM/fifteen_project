from grpc import Status
from pydantic import BaseModel
from enum import IntEnum


# ----------------------------- pydantic Models -----------------------------

class State(IntEnum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """
    CASSE = 1
    NEUF = 2
    BON_ETAT = 3


class Bike(BaseModel):
    """ Bike class that describes bike

    Args:
        serial_number : bike identifier (integer)
        status : 
        maintenance_state : 
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
    """_summary_

    Args:
        BaseModel (_type_): _description_
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

if __name__ == '__main__':

    # ----------------------------- examples -----------------------------

    velo = Bike(serial_number="CH45RT", status=0, maintenance_state=State.BON_ETAT)
    velo2 = Bike(serial_number="AB124GG", status=0, maintenance_state=State.CASSE)
    velo3 = Bike(serial_number="1478HGT", status=1, maintenance_state=State.NEUF)

    stat = Station(serial_number="456", maintenance_state=State.CASSE, associated_bikes=[velo, velo2, velo3])

    print(velo.dict())