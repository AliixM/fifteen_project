from flask import Flask, jsonify, request, make_response
################################################################################################
from schemas import State, Bike, Station, Operation
from postgresql_funcs import *
################################################################################################
import datetime
################################################################################################

# define the flask app
app = Flask(__name__)

# launch debug
app.debug = True

################################################################################################
# data to test pydantic classes

bikes = []


velo = Bike(serial_number="1234", status=True, maintenance_state=State.BON_ETAT)
velo2 = Bike(serial_number="1245", status=True, maintenance_state=State.CASSE)
velo3 = Bike(serial_number="1478", status=False, maintenance_state=State.NEUF)

bikes.append(velo)
bikes.append(velo2)
bikes.append(velo3)


##########################################   CRUD   ############################################

date = datetime.date.today()
NULL="null"

##########################################   CREATE   ############################################

@app.route('/create_bike_api/', methods=['POST'])
def create_bike_api():
    """ 
        Function to create a bike in the database using
        a serial_number, a status and maintenance_state

    Returns:
        A json message indicating that the bike has been created
    """

    # operation type to insert in the history table
    operation_type = Operation.CREATE

    # check if arguments are provided
    if 'serial_number' in request.args:
        serial_number = str(request.args['serial_number'])
    else:
        return jsonify({"error" : "No serial number provided."})
    if 'status' in request.args:
        status = str_to_bool(request.args['status'])
    else:
        return jsonify({"error" : "No status provided."})
    if 'maintenance_state' in request.args:
        maintenance_state = request.args['maintenance_state']
    else:
        return jsonify({"error" : "No maintenance state provided."})
 
    # add new bike to the database
    add_bike(serial_number, maintenance_state, status)

    # add a change in history table
    add_history_bike(date, operation_type, serial_number, NULL, maintenance_state, NULL, status)

    return jsonify({"message":"bike created"})



@app.route('/create_station_api/', methods=['POST'])
def create_station_api():
    """ 
        Function to create a station in the database using
        a serial_number, a maintenance_state and a list of associated bikes

    Returns:
        A json message indicating that the bike has been created
    """
    
    # operation type to insert in the history table
    operation_type = Operation.CREATE
    
    # check if arguments are provided
    if 'serial_number' in request.args:
        serial_number = str(request.args['serial_number'])
    else:
        return jsonify({"error" : "No serial number provided."})
    if 'associated_bikes' in request.args:
        associated_bikes = request.args['associated_bikes']
    else:
        return jsonify({"error" : "No associated_bikes provided."})
    if 'maintenance_state' in request.args:
        maintenance_state = request.args['maintenance_state']
    else:
        return jsonify({"error" : "No maintenance state provided."})
    
    # add new bike to the database
    add_station(serial_number, maintenance_state, associated_bikes)
    
    # add a change in history table
    add_history_station(date, operation_type, serial_number, NULL, maintenance_state, associated_bikes, associated_bikes)

    return jsonify({"message":"station created"})

##########################################   READ   ############################################

@app.route('/get_bike_api/', methods=['GET'])
def get_bike_api():
    """ Function that takes the serial_number of a bike and retrieves its information

    Returns:
        A dictionnary list with bike information (json format)
    """
    # Checks if an ID is provided in a URL.
    # ID => assigned to a variable.
    # no ID => error message displayed in the browser.
    if 'serial_number' in request.args:
        serial_number = str(request.args['serial_number'])
    else:
        return jsonify({"error" : "No ID provided."})
 
    results = get_bike(serial_number)

    # if there is no bike matching with the ID, an empty list is returned

    return jsonify(results)


@app.route('/get_station_api/', methods=['GET'])
def get_station_api():
    """ Function that takes the serial_number of a station and retrieves its information

    Returns:
        A dictionnary list with station information (json format)
    """
    # Checks if an ID is provided in a URL.
    # ID => assigned to a variable.
    # no ID => error message displayed in the browser.
    if 'serial_number' in request.args:
        serial_number = str(request.args['serial_number'])
    else:
        return jsonify({"error" : "No ID provided."})
 
    results = get_station(serial_number)

    # if there is no bike matching with the ID, an empty list is returned

    return jsonify(results)


@app.route('/get_bikes/', methods=['GET'])
def get_bikes():
    """ Function that finds informations of all bikes in the database

    Returns:
        A list of dict with bikes informations (json format)
    """

    results = get_all_bikes()
    return jsonify(results)


@app.route('/get_stations/', methods=['GET'])
def get_stations():
    """ Function that finds informations of all stations in the database

    Returns:
        A list of dict with staions informations (json format)
    """
    results = get_all_station()
    return jsonify(results)


@app.route('/get_number_stations/', methods=['GET'])
def get_number_stations():
    """ Function that finds the count of stations in the database

    Returns:
        Number of stations
    """
    return jsonify({"number of stations": get_number_of_stations()})


@app.route('/get_number_bikes/', methods=['GET'])
def get_number_bikes():
    """ Function that finds the count of bikes in the database

    Returns:
        Number of bikes
    """
    return jsonify({"number of bikes": get_number_of_bikes()})


##########################################   UPDATE   ############################################


def str_to_bool(stat):
    """ Function that changes string to boolean

    Args:
        stat (string): status 

    Raises:
        ValueError: raised if the string is not true or false

    Returns:
        boolean 
    """
    if stat.lower() == "false":
        return False
    elif stat.lower() == "true":
        return True
    else:
        raise ValueError("Unrecognized type")


@app.route('/update_bike_api/', methods=['POST'])
def update_bike_api():
    """ Function that update a bike using the serial_number to find it in the database

    Returns:
        A json message indicating that the bike has been updated
    """
    
    # operation type to insert in the history table
    operation_type = Operation.UPDATE

    # check if arguments are provided
    if 'serial_number' in request.args:
        serial_number = str(request.args['serial_number'])
    else:
        return jsonify({"error" : "No serial number provided."})
    if 'status' in request.args:
        status = str_to_bool(request.args['status'])
    else:
        return jsonify({"error" : "No status provided."})
    if 'maintenance_state' in request.args:
        maintenance_state = (request.args['maintenance_state'])
    else:
        return jsonify({"error" : "No maintenance state provided."})

    # find old informations relevant to the bike to add a line in history table
    results = get_bike(serial_number)
    maintenance_state_old = results['maintenance_state']
    status_old = results['status']

    # update bike in the database using the serial number to find it
    # only maintenance state and status can be modified
    update_bike(serial_number, maintenance_state, status)

    # add a change in history table
    add_history_bike(date, operation_type, serial_number, maintenance_state_old, maintenance_state, status_old, status)
    
    return jsonify({"message" : "bike updated"})


@app.route('/update_station_api/', methods=['POST'])
def update_station_api():
    """ Function that update a station using the serial_number to find it in the database

    Returns:
        A json message indicating that the station has been updated
    """

    # operation type to insert in the history table
    operation_type=Operation.UPDATE

    # check if arguments are provided
    if 'serial_number' in request.args:
        serial_number = str(request.args['serial_number'])
    else:
        return jsonify({"error" : "No serial number provided."})
    if 'associated_bikes' in request.args:
        associated_bikes = request.args['associated_bikes']
    else:
        return jsonify({"error" : "No associated bikes provided."})
    if 'maintenance_state' in request.args:
        maintenance_state = (request.args['maintenance_state'])
    else:
        return jsonify({"error" : "No maintenance state provided."})

    # find old informations relevant to the station to add a line in history table
    results = get_station(serial_number)
    maintenance_state_old = results['maintenance_state']
    associated_bikes_old = results['associated_bikes']

    # update station in the database using the serial number to find it
    # only maintenance state and status can be modified
    update_station(serial_number, maintenance_state, associated_bikes)
    
    # add a change in history table
    add_history_station(date, operation_type, serial_number, maintenance_state_old, maintenance_state, associated_bikes_old, associated_bikes)
    
    return jsonify({"message" : "station updated"})

##########################################   DELETE   ############################################


@app.route('/delete_bike_api/', methods=['POST'])
def delete_bike_api():
    """ Function that delete a bike in the database using its serial number

    Returns:
        A json message indicating that the bike has been deleted
    """
    
    # check if serial number is provided
    if 'serial_number' in request.args:
        serial_number = str(request.args['serial_number'])
    else:
        return jsonify({"error" : "No serial number provided."})

    # operation type to insert in the history table
    operation_type = Operation.DELETE

    # find old informations relevant to the bike to add a line in history table
    results = get_bike(serial_number)
    maintenance_state_old = results['maintenance_state']
    status_old = results['status']

    # check if a bike with the serial number given exists 
    if is_bike_in_db(serial_number):
        delete_bike(serial_number)
        add_history_bike(date, operation_type, serial_number, maintenance_state_old, NULL, status_old, NULL)
        return jsonify({"message": "bike deleted"})
    else:
        # if not => return a json error message
        return jsonify({"error": "No bike matching this serial number"})


@app.route('/delete_station_api/', methods=['POST'])
def delete_station_api():
    """ Function that delete a station in the database using its serial number

    Returns:
        A json message indicating that the station has been deleted
    """
    
    # check if arguments are provided
    if 'serial_number' in request.args:
        serial_number = str(request.args['serial_number'])
    else:
        return jsonify({"error" : "No serial number provided."})

    # operation type to insert in the history table
    operation_type = Operation.DELETE
    # find old informations relevant to the bike to add a line in history table
    results = get_station(serial_number)
    maintenance_state_old = results['maintenance_state']
    associated_bikes_old = results['associated_bikes']

    # check if a bike with the serial number given exists 
    if is_station_in_db(serial_number):
        delete_station(serial_number)
        add_history_station(date, operation_type, serial_number, maintenance_state_old, NULL, associated_bikes_old, associated_bikes_old)
        return jsonify({"message": "station deleted"})
    else:
        # if not => return a json error message
        return jsonify({"error": "No station matching this serial number"})


################################################   HISTORY   ################################################

@app.route('/get_changes_history_bikes/', methods=['GET'])
def get_changes_history_bikes():
    """ Function that queries past object states between two dates

    Returns:
        A json response indicating the list of states of the targetted object between provided dates
    # """
    if 'min_date' in request.args:
        min_date = str(request.args['min_date'])
    else:
        return jsonify({"error" : "No min date provided."})
 
    # check if a max date is provided
    if 'max_date' in request.args:
        max_date = str(request.args['max_date'])
    else:
        return jsonify({"error" : "No max date provided."})

    results = get_changes_between_dates_bikes(min_date, max_date)
    # if there is no bike matching with the ID, an empty list is returned

    return jsonify(results)


@app.route('/get_changes_history_bikes/', methods=['GET'])
def get_changes_history_stations():
    """ Function that queries past object states between two dates

    Returns:
        A json response indicating the list of states of the targetted object between provided dates
    # """
    if 'min_date' in request.args:
        min_date = str(request.args['min_date'])
    else:
        return jsonify({"error" : "No min date provided."})
 
    # check if a max date is provided
    if 'max_date' in request.args:
        max_date = str(request.args['max_date'])
    else:
        return jsonify({"error" : "No max date provided."})

    results = get_changes_between_dates_stations(min_date, max_date)
    # if there is no bike matching with the ID, an empty list is returned

    return jsonify(results)


##########################################   API RUN   ############################################

app.run()