# Mr-Dns for Kali Linux
Mr-Dns is simple Domain gathering information tool that is written with Python Script.
#


## Requirement to Run Mr-Dns
Make sure you have installed the Python packages if you didn't past this commands in terminal and it will install the required packages.

```bash
pip install requests dnspython whois

```

- **requests:** This package is used for making HTTP requests to fetch IP and subdomain information.

- **dnspython:** This package is used for DNS resolution to fetch DNS records.

- **whois:** This package is used to query WHOIS information for domain server details.

## Adding Path
Edit .bashrc or zshrc

```bash
nano ~/.bashrc
nano ~/.zshrc

```
Add path in the last of the file.

```bash
export PATH=$PATH:/home/(use your username here)/.local/bin

```
## How to Install

```bash
git clone https://github.com/s-zahir/mr_dns.git

```
Go to the same directory where you clone the tool and type

```bash
pip install . 

```
To uninstall the tool 

```bash
pip uninstall mr_dns

```
## How to Use
After completing the installtion you need to type in your terminal 

```bash
mr_dns www.bing.com 

```