import azure.functions as func
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="http_trigger")
def http_trigger(req:func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger processed a request')

    logging.info(req.get_json())

    response_body =  json.dumps({
        "message":"success"
    })

    response = func.HttpResponse(
        headers={
        "Access-Control-Allow-Origin": "https://nice-meadow-010225a00.5.azurestaticapps.net/",
        "Vary": "Origin",
        "Access-Control-Allow-Methods":"*",
        "Content-Type": "application/json"
        },
        status_code=200,  # Set status code to Created
        body=response_body
    )

    logging.info(response.get_body())
 
    return response

 # "Content-Type": "application/json",




# @app.route(route="http_trigger")
# def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )
    
   