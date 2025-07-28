import azure.functions as func
import logging
import web_request as WB
import json


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_get_fuel_price")
def http_get_fuel_price(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
   
    try:
        prices = WB.fetch_fuel_prices()
    except Exception as e:
        print("❌ Ошибка при парсинге:", e)



    return func.HttpResponse(
        json.dumps(prices),
        status_code=200,
        mimetype="application/json")
        
        