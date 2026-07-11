import requests as requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

LICEE = {
    968: 'COLEGIUL "RICHARD WURMBRAND", IAȘI',
    1317: 'COLEGIUL AGRICOL ŞI DE INDUSTRIE ALIMENTARĂ "VASILE ADAMACHI", IAŞI',
    704: 'COLEGIUL NAŢIONAL "COSTACHE NEGRUZZI", IAŞI',
    12: 'COLEGIUL NAȚIONAL "EMIL RACOVIŢĂ", IAŞI',
    74: 'COLEGIUL NAȚIONAL "GARABET IBRĂILEANU", IAȘI',
    1189: 'COLEGIUL NAȚIONAL "VASILE ALECSANDRI", IAŞI',
    61: 'COLEGIUL NAȚIONAL, IAŞI'
}

VERBOSE = True
URL_BASE = 'https://bacalaureat.edu.ro/Pages/JudetUnitRezultMedie.aspx?Jud=26&IdUnitInv='
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}

def extract_state(soup):
    return {
        "__VIEWSTATE": soup.find(id="__VIEWSTATE")["value"],
        "__VIEWSTATEGENERATOR": soup.find(id="__VIEWSTATEGENERATOR")["value"],
        "__EVENTVALIDATION": soup.find(id="__EVENTVALIDATION")["value"],
    }

def write_csv(data):
    with open('licee_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([x.split(',')[0] for x in LICEE.values()]) # numele liceelor
        writer.writerows(
            zip_longest(*data.values(), fillvalue="")
        )


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")

    container = soup.find(id="ContentPlaceHolderBody_FinalDiv")
    if container is None:
        return []

    results = []

    for tr in container.find_all("tr", class_=["tr1", "tr2"]):
        tds = tr.find_all("td")

        if len(tds) > 15:
            media = tds[15].get_text(strip=True)
            results.append(media)

    return results

def fetch_data(liceu_id, liceu_name):
    session = requests.Session()

    url = URL_BASE + str(liceu_id)

    # First request to get the initial state and number of pages
    r = session.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    dropdown = soup.find(id="ContentPlaceHolderBody_DropDownList2")
    pages = len(dropdown.find_all("option"))

    state = extract_state(soup)
    results = parse_page(r.text)
    print(f"{liceu_name}: {pages} pages")

    for page in range(2, pages + 1):

        payload = {
            "__EVENTTARGET": "ctl00$ContentPlaceHolderBody$DropDownList2",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            **state,
            "ctl00$ContentPlaceHolderBody$DropDownList2": str(page),
        }

        r = session.post(
            url,
            headers=HEADERS,
            data=payload,
        )

        r.raise_for_status()

        results.extend(parse_page(r.text))
        soup = BeautifulSoup(r.text, "html.parser")
        state = extract_state(soup)
        print(f"page {page}/{pages}")

    return liceu_name, results

if __name__ == "__main__":
    load_dotenv()
    VERBOSE = os.getenv("VERBOSE", "True").lower() in ("true", "1", "t")
    all_data = {}

    for liceu_id, liceu_name in LICEE.items():
        print(f"Fetching data for {liceu_name}...")
        nume, data = fetch_data(liceu_id, liceu_name)
        all_data[nume] = data

    write_csv(all_data)
    print("Data written to licee_data.csv")