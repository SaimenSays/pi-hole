import csv
import requests
from datetime import datetime

url = "https://www.watchlist-internet.at/liste-betruegerischer-shops/csv/"
response = requests.get(url)
response.encoding = "utf-8"

domains = set()
for row in csv.reader(response.text.splitlines(), delimiter=';'):
    if row and row[0] != "Domain":
        raw = row[0].strip().lower()
        if raw:
            # Alles nach "/" entfernen (inkl. Unterseiten)
            domain = raw.split("/")[0]

            # Optional: http(s) entfernen, falls vorhanden
            domain = domain.replace("http://", "").replace("https://", "")
            
            if domain:
                domains.add(domain)

# Datum im ISO-Format
date_str = datetime.utcnow().strftime("%Y-%m-%d")

with open("watchlist-internet.txt", "w") as f:
    # Kommentar-Header (Pi-hole versteht # als Kommentar)
    f.write(f"# Quelle: {url}\n")
    f.write(f"# Generiert am: {date_str} (UTC)\n")
    f.write(f"# Anzahl Domains: {len(domains)}\n\n")

    for d in sorted(domains):
        f.write(d + "\n")
