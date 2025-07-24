import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pprint
import azure.functions as func
import logging


URL = "https://www.neste.lv/lv/content/degvielas-cenas"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_fuel_prices():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    rows = table.find_all("tr")[1:]  # Пропускаем заголовок

    result = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 3:
            continue  # Пропускаем некорректные строки

        fuel_name = cols[0].get_text(strip=True)
        price = cols[1].get_text(strip=True).replace(",", ".")
        locations = [addr.strip() for addr in cols[2].get_text(strip=True).split(",")]

        result.append({
            "fuel_type": fuel_name,
            "price_eur_per_liter": float(price),
            "locations": locations
        })

    return result

def save_to_json(data, filename="neste_prices.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "data": data
        }, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    try:
        prices = fetch_fuel_prices()
        pprint.pprint(prices, sort_dicts=False)
    except Exception as e:
        print("❌ Ошибка при парсинге:", e)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_get_fuel_price")
def http_get_fuel_price(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )