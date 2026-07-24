import requests as re
from bs4 import BeautifulSoup

LICEE = {}

def first_request():
    resp = re.get('https://admitere.edu.ro/Pages/Primele10Spec.aspx?jud=26')
    txt = resp.text

    soup = BeautifulSoup(txt, "html.parser")
    table = soup.find("table", class_='mainTable')
    if table is None:
        print("Table is Not FOUND!")

    rows = table.find_all("tr")
    if rows is None or len(rows) == 0:
        print("NO rows FOUND")

    rows = rows[1:]
    for row in rows:
        tds = row.find_all("td")
        LICEE[tds[1].text + ", " + tds[3].text] = float(tds[6].text)


# Returns a list of high schools of potential to be admitted to
# Considers this year's last grade
def admitted_to(grade: float, option_list: list):
    l = []
    for option in option_list:
        if option not in LICEE.keys():
            pass
        
        if grade > LICEE[option]:
            l.append(option)
    
    return l

if __name__ == '__main__':
    first_request()
    print(LICEE)
    keys = list(LICEE.keys())
    print(admitted_to(8.82, [keys[1], keys[2], keys[5], keys[7], keys[10], keys[14], keys[15]]))