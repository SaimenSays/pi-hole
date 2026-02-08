import csv
import requests

url = "https://www.watchlist-internet.at/liste-betruegerischer-shops/csv/"
response = requests.get(url)
response.encoding = "utf-8"

domains = set()

for row in csv.reader(response.text.splitlines(), delimiter=';'):
    if row and row[0] != "Domain":
        domain = row[0].strip().lower()
        if domain:
            domains.add(domain)

with open("watchlist-internet.txt", "w") as f:
    for d in sorted(domains):
        f.write(d + "\n")
