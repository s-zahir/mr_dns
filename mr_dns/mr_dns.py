# mr_dns_tool/mr_dns/mr_dns.py

import dns.resolver
import requests
import whois
import socket
import argparse

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
    print(f"Gathering DNS information for domain: {domain}\n")
    dns_records = get_dns_records(domain)
    for record_type, records in dns_records.items():
        print(f"{record_type} records: {records}")

    print("\nGathering IP information for A records:\n")
    for ip in dns_records.get('A', []):
        ip_info = get_ip_info(ip)
        print(f"IP: {ip} - Info: {ip_info}")

    print("\nEnumerating subdomains:\n")
    subdomains = get_subdomains(domain)
    for subdomain in subdomains:
        print(f"Subdomain: {subdomain}")
        sub_dns_records = get_dns_records(subdomain)
        for record_type, records in sub_dns_records.items():
            print(f"{subdomain} {record_type} records: {records}")
            if record_type == 'A':
                for ip in records:
                    ip_info = get_ip_info(ip)
                    print(f"{subdomain} IP: {ip} - Info: {ip_info}")

    print("\nFetching server information:\n")
    server_info = get_server_info(domain)
    print(f"Server info: {server_info}")

    print("\nGetting IP address:\n")
    ip_address = get_ip_address(domain)
    print(f"IP address: {ip_address}")

def main():
    parser = argparse.ArgumentParser(description='Gather domain information.')
    parser.add_argument('domain', type=str, help='The domain to gather information for')
    args = parser.parse_args()
    gather_domain_info(args.domain)
