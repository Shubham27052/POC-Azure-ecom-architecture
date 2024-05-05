from datetime import datetime, timedelta
import azure.functions as func
import json
import logging
import uuid
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions, BlobType
from keys import CONNECTION_STRING

# Connecting with the CosmosDB database
cosmos_client = CosmosClient.from_connection_string(CONNECTION_STRING)
database = cosmos_client.get_database_client("database")
container = database.get_container_client("userdata")

# Connection to the Blob Storage
sas_token = generate_account_sas(
    account_name="pocecommstorageaccount",
    account_key="key1",
    resource_types=ResourceTypes(service=True),
    permission=AccountSasPermissions(read=True, write=True,delete=True, add=True, create=True,list=True),
    expiry=datetime.now() + timedelta(days=10)
)

blob_service_client = BlobServiceClient(account_url="https://pocecommstorageaccount.blob.core.windows.net/uploadedfiles", credential=sas_token)
container_client = blob_service_client.get_container_client(container="uploadedfiles")

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

    # Getting the file
    req_body = req.get_body()
    form_data = req_body.decode('utf-8').split('&')

    for item in form_data:
        key, value = item.split('=')
        if key == 'file':
            file_data = value
    if not file_data:
        return func.HttpResponse(
            "No file uploaded",
            status_code=400
        )
    
    file_bytes = bytes(file_data, 'utf-8')
    
    # upload data to container
    container_client.upload_blob(name="bro", data=file_bytes, blob_type=BlobType.BLOCKBLOB, metadata={"source": name})

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