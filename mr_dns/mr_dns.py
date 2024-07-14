# mr_dns_tool/mr_dns/mr_dns.py

import dns.resolver
import requests
import whois
import socket
import argparse
from datetime import datetime

# Define a colorful symbol and green text
color_symbol = "\033[95m★\033[0m"  # Magenta star symbol
green_text = "\033[92m"  # Green text
reset_text = "\033[0m"  # Reset text color

def get_dns_records(domain):
    records = {}
    try:
        # A record
        try:
            a_records = dns.resolver.resolve(domain, 'A')
            records['A'] = [str(record) for record in a_records]
        except dns.resolver.NoAnswer:
            records['A'] = []

        # AAAA record
        try:
            aaaa_records = dns.resolver.resolve(domain, 'AAAA')
            records['AAAA'] = [str(record) for record in aaaa_records]
        except dns.resolver.NoAnswer:
            records['AAAA'] = []

        # MX record
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            records['MX'] = [str(record.exchange) for record in mx_records]
        except dns.resolver.NoAnswer:
            records['MX'] = []

        # NS record
        try:
            ns_records = dns.resolver.resolve(domain, 'NS')
            records['NS'] = [str(record) for record in ns_records]
        except dns.resolver.NoAnswer:
            records['NS'] = []

        # CNAME record
        try:
            cname_records = dns.resolver.resolve(domain, 'CNAME')
            records['CNAME'] = [str(record) for record in cname_records]
        except dns.resolver.NoAnswer:
            records['CNAME'] = []

        # TXT record
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            records['TXT'] = [str(record) for record in txt_records]
        except dns.resolver.NoAnswer:
            records['TXT'] = []

    except dns.resolver.NoNameservers:
        print(f"No nameservers found for domain: {domain}")
    except dns.resolver.NXDOMAIN:
        print(f"The domain {domain} does not exist.")
    except dns.exception.Timeout:
        print(f"Timeout while querying DNS records for domain: {domain}")
    except Exception as e:
        print(f"An error occurred while querying DNS records for domain: {domain}. Error: {e}")

    return records

def get_ip_info(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Could not get IP info: {e}")
        return {}

def get_subdomains(domain):
    subdomains = set()
    try:
        response = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json")
        response.raise_for_status()
        data = response.json()
        for entry in data:
            name_value = entry['name_value']
            if name_value.startswith('*.'):
                name_value = name_value[2:]
            subdomains.add(name_value)
    except requests.RequestException as e:
        print(f"Error fetching subdomains: {e}")

    return list(subdomains)

def get_server_info(domain):
    try:
        domain_info = whois.whois(domain)
        # Add upgrading date
        domain_info['upgrading_date'] = datetime.now().strftime('%Y-%m-%d')
        return domain_info
    except Exception as e:
        print(f"Error fetching server info: {e}")
        return {}

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return "Unable to resolve IP address"

def gather_domain_info(domain):
    print(f"\n\033[1mGathering information for domain: {domain}\033[0m\n")
    
    print(f"\n\033[1mGetting IP Address:\033[0m\n")
    ip_address = get_ip_address(domain)
    print(f"{color_symbol} {green_text}IP address: {ip_address}{reset_text}")

    print(f"\n\033[1mFetching Server Information:\033[0m\n")
    server_info = get_server_info(domain)
    print(f"{color_symbol} {green_text}Server info: {server_info}{reset_text}")

    print(f"\n\033[1mGathering DNS Records:\033[0m\n")
    dns_records = get_dns_records(domain)
    for record_type, records in dns_records.items():
        print(f"{color_symbol} {green_text}{record_type} records: {records}{reset_text}")

    print(f"\n\033[1mEnumerating Subdomains:\033[0m\n")
    subdomains = get_subdomains(domain)
    for subdomain in subdomains:
        print(f"{color_symbol} {green_text}Subdomain: {subdomain}{reset_text}")
        sub_dns_records = get_dns_records(subdomain)
        for record_type, records in sub_dns_records.items():
            print(f"{color_symbol} {green_text}{subdomain} {record_type} records: {records}{reset_text}")
            if record_type == 'A':
                for ip in records:
                    ip_info = get_ip_info(ip)
                    print(f"{color_symbol} {green_text}{subdomain} IP: {ip} - Info: {ip_info}{reset_text}")

def main():
    parser = argparse.ArgumentParser(description='Gather domain information.')
    parser.add_argument('domain', type=str, help='The domain to gather information for')
    args = parser.parse_args()
    gather_domain_info(args.domain)

main()
