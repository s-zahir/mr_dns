# Mr-Dns for Kali Linux
Mr-Dns is a Domain Information Gathering tool that is written with Python Script. Its gather Information such IP address , Subdomains etc.
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
Check your shell with command 
```bash
echo $0

```
Edit .bashrc or .zshrc

```bash
nano ~/.bashrc

```
```bash
nano ~/.zshrc

```
Add path in the last of the file.

```bash
export PATH=$PATH:/home/(use your username here)/.local/bin

```
Example: 
```bash
export PATH=$PATH:/home/kali/.local/bin

```

After adding the path and installation is done close the previous terminal and open new one to try this tool.
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