import subprocess

# nmap -F -sV 192.168.1.155 - стоковый no grepable
# nmap -Pn -sV -oG - 192.168.1.155 для Windows

# nmap --source-port=53 -F -sV -oG - -Pn 192.168.1.155 - stealth for windows
# nmap --source-port=53 -F -sV -oG - -O 192.168.1.155 - stealth for linux

def scan(hosts) -> str:
    nmap_args = ['nmap', '-F', '-sV', '-Pn'] + hosts
    latest_scan_result = subprocess.run(nmap_args, capture_output=True, text=True).stdout

    print(latest_scan_result)

    log = "# TYPE nmap_port_scan gauge\n"

    current_host = None
    current_ip = None

    for line in latest_scan_result.split('\n'):
        line = line.strip()

        if line.startswith("Nmap scan report for"):
            parts = line.split()

            if '(' in line and ')' in line:
                host_start = line.find("for ") + 4
                host_end = line.find(" (")
                current_host = line[host_start:host_end]
                ip_start = line.find("(") + 1
                ip_end = line.find(")")
                current_ip = line[ip_start:ip_end]

            else:
                current_host = parts[-1]
                current_ip = parts[-1]

        elif line.startswith(('PORT ', 'Not shown:', 'Host is up', 'Other addresses', 'Service Info', 'MAC Address')):
            continue

        elif '/' in line and 'tcp' in line and (line.split()[1] in ['open', 'filtered', 'closed']):
            parts = line.split()
            port_info = parts[0].split('/')
            port = port_info[0]
            protocol = port_info[1]
            state = parts[1]
            service = parts[2] if len(parts) > 2 else 'unknown'

            version = 'unknown'
            if len(parts) > 3:
                version = ' '.join(parts[3:])
                version = version.replace('"', '').replace("'", "")

            log += f'nmap_port_scan{{host="{current_host}", ip="{current_ip}", port="{port}", protocol="{protocol}", state="{state}", service="{service}", version="{version}"}} 1\n'

    return log
