import csv
from ipwhois import IPWhois
import ipaddress
from collections import defaultdict

def main():

    with open('results.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        ip_cidr = {}
        for row in readCSV:
            ip = row[0]
            print(ip)
            obj = IPWhois(row[0])
            try:
                resp = obj.lookup_whois()
                cidr = resp["nets"][0]['cidr']
                print("CIDR: ", cidr)
                #print("IP Range: ", [str(ip) for ip in ipaddress.IPv4Network(cidr)])
                ip_cidr[ip] = cidr
                # group ip with the same cidr
            except Exception:
                print("skipped ", ip)
            ip_cidr_grouped = defaultdict(list)

            for key, value in ip_cidr.items():
                ip_cidr_grouped[value].append(key)

        for key,value in ip_cidr_grouped.items():
            print(key, "=>", value)
main()
