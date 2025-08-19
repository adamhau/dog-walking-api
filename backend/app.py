from flask import Flask, jsonify, request
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
from flask_cors import CORS


#Firebase setup
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://rtpdatabase-42167-default-rtdb.firebaseio.com/"
})

# Creates a Flask application instance
app = Flask(__name__)
CORS(app)

#helper func to validate dog id
def validate_dog_id(dog_id):
    ref = db.reference(f"/dogs/{dog_id}")
    dog = ref.get()
    return dog is not None
    
#helper func to validate walker ids
def validate_walker_id(walker_id):
    ref = db.reference(f"/dogwalkers/{walker_id}")
    walker = ref.get()
    return walker is not None

#Here I define the routes for the Flask application.
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Dog Walking API!"})

#Routes for Dogs

@app.route("/dogs", methods=["GET"]) #GET method to retrieve the list of dogs
def get_dogs():
    ref = db.reference("/dogs")
    dogs = ref.get() or {}
    return jsonify(list(dogs.values()))

@app.route("/dogs/<dog_id>", methods=["GET"]) #GET to receive a specific dog (Made this for Postman testing)
def get_dog_by_id(dog_id):
    ref = db.reference(f"/dogs/{dog_id}")
    dog = ref.get() #returns dog info or None

    if dog:
        return jsonify(dog), 200
    else:
        return jsonify({"error": f"Dog {dog_id} not found."}), 404


@app.route("/dogs", methods=["POST"]) #POST method to add a new dog
def add_dog():
    data = request.get_json()

    required_fields = ["name", "breed", "age"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400


    ref = db.reference("/dogs") #references initial Node
    ref_child = ref.push() #creates child node and generates a unique KEY for it.

    new_dog = {
        "id": ref_child.key, #use the generated key from push
        "name": data.get("name"),
        "breed": data.get("breed"),
        "age": data.get("age")
    }

    ref_child.set(new_dog) #set the child (that has unique id) to the contents of new_dog
    return jsonify(new_dog), 201

@app.route("/dogs/<dog_id>", methods=["DELETE"]) #DELETE method to remove a dog
def delete_dog(dog_id):
    # Delete the dog
    ref = db.reference(f"/dogs/{dog_id}")
    dog_data = ref.get()
    dog_name = dog_data.get("name")
    if not dog_data:
        return jsonify({"error": f"Dog {dog_id} not found."}), 404
    ref.delete()

    # Delete all walks with this dog
    walks_ref = db.reference('walks')
    walks = walks_ref.get()
    if walks:
        for walk_id, walk in walks.items():
            if walk.get('dog_id') == dog_id:
                walks_ref.child(walk_id).delete()
    return jsonify({'message': f'Dog "{dog_name}" and related walks deleted'}), 200

@app.route("/dogs/<dog_id>", methods=["PATCH"])
def patch_dog(dog_id):
    data = request.get_json()

    ref = db.reference(f"/dogs/{dog_id}")
    dog = ref.get()

    if not dog:
        return jsonify({"error": f"Dog {dog_id} not found."}), 404
    
    updates = {}

    # Update only the fields provided in the request
    if "name" in data:
        updates["name"] = data["name"]
    if "breed" in data:
        updates["breed"] = data["breed"]
    if "age" in data:
        updates["age"] = data["age"]

    if not updates:
        return jsonify({"error": "No valid fields to update."}), 400
    
    ref.update(updates)
    dog_edit = ref.get()

    return jsonify(dog_edit), 200
    

#Routes for Dogwalkers (functionality almost identical to dogs)

@app.route("/dogwalkers", methods=["GET"])
def get_dogwalkers():
    ref = db.reference("/dogwalkers")
    dogwalkers = ref.get()
    if not dogwalkers:
        return jsonify([]), 200
    return jsonify(list(dogwalkers.values())), 200

@app.route("/dogwalkers/<walker_id>", methods=["GET"])
def get_walker_by_id(walker_id):
    ref = db.reference(f"/dogwalkers/{walker_id}")
    dogwalker = ref.get()
    if not dogwalker:
        return jsonify({"error": f"Walker {walker_id} not found"}), 404
    return jsonify(dogwalker), 200

@app.route("/dogwalkers", methods=["POST"])
def add_dogwalker():
    data = request.get_json()

    required_fields = ["name", "phone"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400

    ref = db.reference("/dogwalkers")
    ref_child = ref.push()

    new_dogwalker = {
        "id": ref_child.key,
        "name": data.get("name"),
        "phone": data.get("phone")
    }

    ref_child.set(new_dogwalker)
    return jsonify(new_dogwalker), 201

@app.route("/dogwalkers/<walker_id>", methods=["DELETE"])
def delete_walker(walker_id):
    # Delete the walker
    ref = db.reference(f"/dogwalkers/{walker_id}")
    walker_data = ref.get()

    if not walker_data:
        return jsonify({"error": f"Walker {walker_id} not found"}), 404

    walker_name = walker_data.get("name")

    # Delete walker
    ref.delete()

    # Delete all walks with this walker
    walks_ref = db.reference('walks')
    walks = walks_ref.get()
    if walks:
        for walk_id, walk in walks.items():
            if walk.get('walker_id') == walker_id:
                walks_ref.child(walk_id).delete()

    return jsonify({'message': f'Walker "{walker_name}" and related walks deleted'}), 200

@app.route("/dogwalkers/<walker_id>", methods=["PATCH"])
def patch_dogwalker(walker_id):
    data = request.get_json()

    ref = db.reference(f"/dogwalkers/{walker_id}")
    walker = ref.get()
    if not walker:
        return jsonify({"error": f"Walker {walker_id} not found"}), 404

    updated = False
    for field in ["name", "phone"]:
        if field in data:
            walker[field] = data[field]
            updated = True

    if not updated:
        return jsonify({"error": "No valid fields to update"}), 400

    ref.set(walker)
    return jsonify(walker), 200

#Route for Walks

@app.route("/walks", methods=["GET"])
def get_walks():
    ref = db.reference("/walks")
    walks = ref.get() or {}
    return jsonify(list(walks.values()))

@app.route("/walks/<walk_id>", methods=["GET"])
def get_walk_by_id(walk_id):
    ref = db.reference(f"/walks/{walk_id}")
    walk = ref.get()
    if walk:
        return jsonify(walk), 200
    else:    
        return jsonify({"error": f"Walk {walk_id} not found."}), 404

@app.route("/walks/<walk_id>", methods=["DELETE"])
def delete_walk(walk_id):
    ref = db.reference(f"/walks/{walk_id}")
    walk_data = ref.get()

    if not walk_data:
        return jsonify({"error": f"Walk {walk_id} not found."}), 404

    dog_id = walk_data.get("dog_id")
    walker_id = walk_data.get("walker_id")

    # Fetch dog name
    dog_ref = db.reference(f"/dogs/{dog_id}")
    dog_data = dog_ref.get()
    dog_name = dog_data.get("name") if dog_data else "Unknown Dog"

    # Fetch walker name
    walker_ref = db.reference(f"/dogwalkers/{walker_id}")
    walker_data = walker_ref.get()
    walker_name = walker_data.get("name") if walker_data else "Unknown Walker"

    # Delete the walk
    ref.delete()
    return jsonify({"message": f'Walk with {dog_name} and {walker_name} deleted.'}), 200

@app.route("/walks", methods=["POST"])
def add_walks():
    data = request.get_json()
    dog_id = data.get("dog_id")
    walker_id = data.get("walker_id")
    date = data.get("date")

    # Validate dog_id
    if not validate_dog_id(dog_id):
        return jsonify({"error": f"Dog with ID {dog_id} not found."}), 400

    # Validate walker_id
    if not validate_walker_id(walker_id):
        return jsonify({"error": f"Walker with ID {walker_id} not found."}), 400

    # Validate date
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except (ValueError, TypeError):
        return jsonify({"error": "Date must be in YYYY-MM-DD format."}), 400

    ref = db.reference("/walks")
    ref_child = ref.push()

    new_walk = {
        "id": ref_child.key,
        "dog_id": dog_id,
        "walker_id": walker_id,
        "date": date
    }
    #Writes new data to child node
    ref_child.set(new_walk)
    return jsonify(new_walk), 201

@app.route("/walks/<walk_id>", methods=["PATCH"])
def patch_walks(walk_id):
    data = request.get_json()
    ref = db.reference(f"/walks/{walk_id}")
    walk = ref.get()

    if not walk:
        return jsonify({"error": f"Walk {walk_id} not found."}), 404

    updates = {}

    # Validate and update dog_id
    if "dog_id" in data:
        if not validate_dog_id(data["dog_id"]):
            return jsonify({"error": f"Dog ID {data['dog_id']} not found."}), 400
        updates["dog_id"] = data["dog_id"]

    # Validate and update walker_id
    if "walker_id" in data:
        if not validate_walker_id(data["walker_id"]):
            return jsonify({"error": f"Walker ID {data['walker_id']} not found."}), 400
        updates["walker_id"] = data["walker_id"]

    # Validate and update date
    if "date" in data:
        try:
            datetime.strptime(data["date"], "%Y-%m-%d")
        except (ValueError, TypeError):
            return jsonify({"error": "Date must be in YYYY-MM-DD format."}), 400
        updates["date"] = data["date"]

    if not updates:
        return jsonify({"error": "No valid fields to update."}), 400

    ref.update(updates)
    updated_walk = ref.get()

    # Fetch updated dog and walker names
    dog_id = updated_walk.get("dog_id")
    walker_id = updated_walk.get("walker_id")

    dog_ref = db.reference(f"/dogs/{dog_id}")
    dog_data = dog_ref.get()
    dog_name = dog_data.get("name") if dog_data else "Unknown Dog"

    walker_ref = db.reference(f"/dogwalkers/{walker_id}")
    walker_data = walker_ref.get()
    walker_name = walker_data.get("name") if walker_data else "Unknown Walker"

    return jsonify({
        "walk": updated_walk,
        "message": f'Walk updated: {dog_name} with {walker_name}.'
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
