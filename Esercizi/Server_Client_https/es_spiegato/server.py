from flask import Flask, request, make_response, jsonify
import base64

# Define a list of users with their credentials and permissions
users: list[dict] = [
    {
        "username": "admin",
        "password": "admin01",
        "rights": {
            "add_citzen": True,
            "view_citzens": True,
            "edit_citzen": True,
            "delete_citzen": True
        }
    },
    {
        "username": "basic",
        "password": "basic01",
        "rights": {
            "add_citzen": False,
            "view_citzens": True,
            "edit_citzen": False,
            "delete_citzen": False
        }
    },
]

# Function to verify if the client is authenticated
def verify_auth() -> dict | None:
    """
    Verify the authentication extracting and decrypting the credentials
    inserted by the client from the request packet taken in input.
    """

    # Extract the encrypted content of 'Authorization' header from the request packet
    enc_auth_header: str = request.headers.get('Authorization')

    # Remove the "Basic " prefix from the encrypted header
    enc_auth_data: str = enc_auth_header[6:]

    # Decode the Base64-encoded credentials
    dec_auth_data: str = base64.b64decode(enc_auth_data).decode('utf-8')

    # Split the decrypted credentials into username and password
    input_username, input_password = dec_auth_data.split(':')

    # Loop through users to find a match with the provided credentials
    for user in users:
        # If the username and password match, return the user dictionary
        if input_username == user["username"] and input_password == user["password"]:
            return user  # Return user dict if found
    
    # If no match is found, return None
    return None

# List to store citizen data
citzens: list[dict] = list()

# Create Flask app instance
api: Flask = Flask(__name__)

# Function to check permissions for the authenticated user
def check_permissions(user: dict, action: str) -> bool:
    """
    Check if the user has the specified permission for an action.
    """
    return user["rights"].get(action, False)



# Operation 1: Add citizen ----------------------------------------------------
@api.route(rule='/add_citzen', methods=['POST'])
def add_citzen() -> None:
    # Check if the user is authenticated
    user = verify_auth()
    if not user:
        # If authentication fails, return 401 Unauthorized
        return make_response(jsonify({"Msg": "Authentication failed"}), 401)
    
    else:
        # Check if the user has permission to add citizens
        if not check_permissions(user, "add_citzen"):
            return make_response(jsonify({"Msg": "Permission denied"}), 403)

        # Ensure the content is in JSON format
        if request.headers.get('Content-Type') == 'application/json':
            # Assign an ID to the new citizen (increment last ID or start from 0)
            new_id = 0 if not citzens else int(citzens[-1]["id"]) + 1
            
            # Set the new ID as a string in the citizen data
            request.json["id"] = str(new_id)
            
            # Add the new citizen data to the list
            citzens.append(request.json)
            
            # Return success message with the new citizen ID
            return make_response(jsonify({"Msg": "Citizen added", "id": request.json["id"]}), 200)

# ----------------------------------------------------------------------------



# Operation 2: View citizens -------------------------------------------------
@api.route('/view_citzens', methods=['GET'])
def view_citzens() -> None:
    # Check if the user is authenticated
    user = verify_auth()
    if not user:
        # If authentication fails, return 401 Unauthorized
        return make_response(jsonify({"Msg": "Authentication failed"}), 401)
    
    else:
        # Check if the user has permission to view citizens
        if not check_permissions(user, "view_citzens"):
            return make_response(jsonify({"Msg": "Permission denied"}), 403)

        # Return the list of all citizens
        return jsonify(citzens)
# ----------------------------------------------------------------------------



# Operation 3: Edit citizen --------------------------------------------------
@api.route('/edit_citzen/<id>', methods=['PUT'])
def edit_citzen(id: str):
    # Check if the user is authenticated
    user = verify_auth()
    if not user:
        # If authentication fails, return 401 Unauthorized
        return make_response(jsonify({"Msg": "Authentication failed"}), 401)
    
    else:
        # Check if the user has permission to edit citizens
        if not check_permissions(user, "edit_citzen"):
            return make_response(jsonify({"Msg": "Permission denied"}), 403)

        # Get the new data for the citizen from the request body
        updated_data = request.json
        
        # Search for the citizen by ID
        for citzen in citzens:
            # If citizen is found, update their data
            if citzen["id"] == id:
                citzen.update(updated_data)
                # Return success message
                return make_response(jsonify({"Msg": "Citizen values successfully edited"}), 200)
        
        # If citizen ID is not found, return 404 Not Found
        return make_response(jsonify({"Msg": "Citizen ID not found"}), 404)

# ----------------------------------------------------------------------------



# Operation 4: Delete citizen ------------------------------------------------
@api.route('/delete_citzen/<id>', methods=['DELETE'])
def delete_citzen(id: str):
    # Check if the user is authenticated
    user = verify_auth()
    if not user:
        # If authentication fails, return 401 Unauthorized
        return make_response(jsonify({"Msg": "Authentication failed"}), 401)
    
    else:
        # Check if the user has permission to delete citizens
        if not check_permissions(user, "delete_citzen"):  # Should be delete_citzen
            return make_response(jsonify({"Msg": "Permission denied"}), 403)

        # Search for the citizen by ID
        for index, citzen in enumerate(citzens):
            # If citizen is found, remove them from the list
            if citzen["id"] == id:
                citzens.pop(index)
                # Return success message
                return make_response(jsonify({"Msg": "Citizen successfully deleted"}), 200)
        
        # If citizen ID is not found, return 404 Not Found
        return make_response(jsonify({"Msg": "Citizen ID not found"}), 404)

# ----------------------------------------------------------------------------



# Start the Flask server -----------------------------------------------------
if __name__ == "__main__":
    # Run the Flask app on host 0.0.0.0, port 8085, with an ad-hoc SSL context
    api.run(host="0.0.0.0", port=8085, ssl_context='adhoc')
# ----------------------------------------------------------------------------
