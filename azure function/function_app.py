import azure.functions as func
import json
import logging
import uuid
from azure.cosmos import CosmosClient
from keys import CONNECTION_STRING

# Replace with your Cosmos DB connection string

cosmos_client = CosmosClient.from_connection_string(CONNECTION_STRING)
database = cosmos_client.get_database_client("database")
container = database.get_container_client("userdata")

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
# @app.cosmos_db_output(arg_name="outputDocument", database_name="database",container_name="userdata", connection="CosmosDbConnectionSetting")

def http_trigger(req: func.HttpRequest) -> func.HttpResponse:

    # Logging
    logging.info('Python HTTP trigger processed a request')

    # Get request body
    try:
        req_body = req.get_json()
    except ValueError:
        logging.warning("Invalid JSON data in request")
        return func.HttpResponse(
            "Error: Invalid JSON data in request body",
            status_code=401
        )

    # Extract data from request body
    name = req_body.get("name")
    email = req_body.get("email")
    message = req_body.get("message")

    # Validate data (optional)
    if not name or not email or not message:
        logging.warning("Missing required fields in request body")
        return func.HttpResponse(
            "Error: Missing required fields in request body",
            status_code=402
        )

    # Create document for Cosmos DB
    new_document = {
        "id": str(uuid.uuid4()),  # Generate unique ID
        "name": name,
        "email": email,
        "message": message,
    }

    logging.info(new_document)
    logging.info(type(new_document))


    ## Write data to Cosmos DB
    try:
        container.create_item(new_document)
    except json.JSONDecodeError as e:
        logging.warning("Could not write data to CosmosDB")
        return func.HttpResponse(
            e,
            status_code=403
        )


    # # Success response
    # logging.info(f"Data written to Cosmos DB: {new_document}")
    return func.HttpResponse(
        "Data successfully stored in Cosmos DB",
        status_code=200
    )