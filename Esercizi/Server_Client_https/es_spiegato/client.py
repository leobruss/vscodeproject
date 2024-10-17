import requests, requests.auth

# Functions used in the main script ------------------------------------------

# Functions used in the main script --------------------------------------------
# Function to build authentication credentials
def build_creds() -> requests.auth.HTTPBasicAuth:
    # Prompt user to input username and password
    input_username: str = input("Enter username: ")
    input_password: str = input("Enter password: ")

    # Return HTTPBasicAuth object with the provided credentials
    return requests.auth.HTTPBasicAuth(input_username, input_password)

# Function to build the citizen data to be sent in the request
def build_data() -> dict:
    # Prompt user to input citizen details
    name: str = input("Enter your name: ")
    surname: str = input("Enter your surname: ")
    birth: str = input("Enter your birth date: ")
    cf: str = input("Enter your cf: ")

    # Return a dictionary with the citizen data
    return {"nome": name, "cognome": surname, "nascita": birth, "cf": cf}

# Function to display menu options and let the user choose an operation
def choose_option() -> int:
    # Print operation options
    print("\nPlease select one of the following options:")
    print("1. Add citzen")
    print("2. Get citzens")
    print("3. Edit citzen")
    print("4. Remove citzen")
    print("5. Quit\n")
    
    # Loop until a valid option is chosen
    while True:
        try:
            # Get user's choice and validate it
            choice = int(input("Enter the number of your choice (1 - 5): "))
            if choice in range(1, 6):
                return choice
            else:
                print("Invalid option, please choose a number between 1 and 5")
        except ValueError:
            print("Please enter a valid number.")
# ----------------------------------------------------------------------------



# Start of the main script ---------------------------------------------------
if __name__ == "__main__":

    while True:

        # Force the user to authenticate before choosing the operation to execute
        if not auth_creds.username or not  auth_creds.password:
            auth_creds: requests.auth.HTTPBasicAuth = build_creds()
            continue

        # Base URL of the REST API
        BASE_URL: str = "https://127.0.0.1:8085"

        # Get user's choice of operation
        operation_id: int = choose_option()

        # Operation 1 -> Add a new citizen -----------------------------------
        if operation_id == 1:
            # Get citizen data from the user
            data: dict = build_data()

            # Send POST request to add the new citizen
            response: requests.Response = requests.post(
                url = f"{BASE_URL}/add_citzen",
                json = data,
                auth = auth_creds,
                verify = False
            )

            # Check response status and display appropriate message
            if response.status_code == 200:
                print("Request successfully sent")
            else:
                print(f"Error: {response.status_code}")
        # --------------------------------------------------------------------

        # Operation 2 -> Get and display all citizens ------------------------
        elif operation_id == 2:
            # Send GET request to retrieve all citizens
            response: requests.Response = requests.get(
                url = f"{BASE_URL}/view_citzens",
                auth = auth_creds,
                verify = False
            )
            
            # Check response status and display the citizen data
            if response.status_code == 200:
                print("Citzens:\n", response.json())
            else:
                print(f"Error: {response.status_code}")
        # --------------------------------------------------------------------

        # Operation 3 -> Edit an existing citizen by ID ----------------------
        elif operation_id == 3:
            # Get the citizen ID to be modified
            input_id: str = input("\nEnter the user ID whose values you want to modify: ")

            # Prompt for new data, leaving fields blank to skip changes
            print("Enter the new data value, leave blank to not modify:")
            updated_data: dict = build_data()

            # Send PUT request to update the citizen's data
            response: requests.Response = requests.put(
                url = f"{BASE_URL}/edit_citzen/{input_id}",
                json = updated_data,
                auth = auth_creds,
                verify = False
            )

            # Check response status and display appropriate message
            if response.status_code == 200:
                print(f"Data successfully updated: {response.status_code}")
            else:
                print(f"Error: {response.status_code}")
        # --------------------------------------------------------------------

        # Operation 4 -> Delete a citizen by ID ------------------------------
        elif operation_id == 4:
            # Get the citizen ID to be deleted
            input_id: str = input("\nEnter the user ID to delete: ")

            # Send DELETE request to remove the citizen
            response: requests.Response = requests.delete(
                url = f"{BASE_URL}/delete_citzen/{input_id}",
                auth = auth_creds,
                verify=False
            )

            # Check response status and display appropriate message
            if response.status_code == 200:
                print(f"Citzen successfully deleted: {response.status_code}")
            else:
                print(f"Error: {response.status_code}")
        # --------------------------------------------------------------------

        # Operation 5 -> Quit ------------------------------------------------
        elif operation_id == 5:
            # Exit the program
            break
        # --------------------------------------------------------------------



        # Wait for user input before showing the menu again
        input("\n")
