import requests
from bs4 import BeautifulSoup
from datetime import datetime



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

