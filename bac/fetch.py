LICEE = {
    968: 'COLEGIUL "RICHARD WURMBRAND", IAȘI',
    1317: 'COLEGIUL AGRICOL ŞI DE INDUSTRIE ALIMENTARĂ "VASILE ADAMACHI", IAŞI',
    704: 'COLEGIUL NAŢIONAL "COSTACHE NEGRUZZI", IAŞI',
    12: 'COLEGIUL NAȚIONAL "EMIL RACOVIŢĂ", IAŞI',
    74: 'COLEGIUL NAȚIONAL "GARABET IBRĂILEANU", IAȘI'
}

VERBOSE = True
URL_BASE = 'https://bacalaureat.edu.ro/Pages/JudetUnitRezultMedie.aspx?Jud=26&IdUnitInv='

def fetch_data(liceu_id, liceu_name):
    if VERBOSE:
        print(f"Fetching data for {liceu_name} (ID: {liceu_id})")
    url = URL_BASE + str(liceu_id)

for liceu_id, liceu_name in LICEE.items():
    fetch_data(liceu_id, liceu_name)