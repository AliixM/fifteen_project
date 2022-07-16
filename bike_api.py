from schemas import State, Bike, Station
from flask import Flask, jsonify, request, make_response



# define the flask app
app = Flask(__name__)

# launch debug
app.debug = True



# data test

bikes = []


velo = Bike(serial_number="1234", status=True, maintenance_state=State.BON_ETAT)
velo2 = Bike(serial_number="1245", status=True, maintenance_state=State.CASSE)
velo3 = Bike(serial_number="1478", status=False, maintenance_state=State.NEUF)

bikes.append(velo)
bikes.append(velo2)
bikes.append(velo3)

# ----------------------------- CRUD -----------------------------

# ----------------------------- CREATE -----------------------------

@app.route('/create_bike/', methods=['GET', 'POST'])
def create_bike():
    if 'serial_number' in request.args:
        serial_number = int(request.args['serial_number'])
    else:
        return jsonify({"error" : "No serial number provided."})
    if 'status' in request.args:
        status = bool(request.args['status'])
    else:
        return jsonify({"error" : "No status provided."})
    if 'maintenance_state' in request.args:
        maintenance_state = request.args['maintenance_state']
    else:
        return jsonify({"error" : "No maintenance state provided."})
 
    add_bike()


    return jsonify({"message":"bike created"})

# ----------------------------- READ -----------------------------
@app.route('/get_bike/', methods=['GET'])
def get_bike():
    # Checks if an ID is provided in a URL.
    # ID => assigned to a variable.
    # no ID => error message displayed in the browser.
    if 'serial_number' in request.args:
        serial_number = str(request.args['serial_number'])
    else:
        return jsonify({"error" : "No ID provided."})
 
    # Create an empty list to store the results
    results = []
 
    # Loop over the data to get the results corresponding to the provided ID.
    # IDs are unique, but other fields can return multiple results
    for bike in bikes:
        if bike.serial_number == str(serial_number):
            results.append(bike.dict())

    # if there is no bike matching with the ID, an empty list is returned

    return jsonify(results)



@app.route('/get_bikes/', methods=['GET'])
def get_bikes():
    results = []
    for bike in bikes:
        results.append(bike.dict())
    return jsonify(results)

# ----------------------------- UPDATE -----------------------------

@app.route('/update_bike/', methods=['PUT'])
def update_bike():
    
    if 'serial_number' in request.args:
        serial_number = int(request.args['serial_number'])
    else:
        return jsonify({"error" : "No serial number provided."})
    if 'status' in request.args:
        status = bool(request.args['status'])
    else:
        return jsonify({"error" : "No status provided."})
    if 'maintenance_state' in request.args:
        maintenance_state = (request.args['maintenance_state'])
    else:
        return jsonify({"error" : "No maintenance state provided."})

    

    return jsonify({"message" : "bike updated"})

# ----------------------------- DELETE -----------------------------

@app.route('/delete_bike/', methods=['GET', 'POST'])
def delete_bike():
    if 'serial_number' in request.args:
        serial_number = str(request.args['serial_number'])
    else:
        return jsonify({"error" : "No serial number provided."})

    cpt = 0
    for bike in bikes:
        if bike.serial_number == str(serial_number):
            cpt = 1
            bikes.remove(bike)

    if cpt == 0:
        return jsonify({"error": "bike not found"})
        
    return jsonify({"message": "bike deleted"})

app.run()