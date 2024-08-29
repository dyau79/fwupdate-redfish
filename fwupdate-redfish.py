import requests
import json
from packaging import version

def read_hosts_from_file(filename):
    hosts = []
    with open(filename, 'r') as file:
        for line in file:
            ip, username, password = line.strip().split(';')
            hosts.append({'ip': ip, 'username': username, 'password': password})
    return hosts

def get_current_firmware_version(host):
    url = f"https://{host['ip']}/redfish/v1/UpdateService/FirmwareInventory"
    response = requests.get(url, auth=(host['username'], host['password']), verify=False)
    if response.status_code == 200:
        data = response.json()
        # This is a placeholder. You'll need to adjust this based on the actual JSON structure
        return data.get('Members')[0].get('Version')
    else:
        print(f"Failed to get firmware version for {host['ip']}")
        return None

def compare_firmware_versions(current_version, target_version):
    return version.parse(current_version) < version.parse(target_version)

def update_firmware(host, firmware_url):
    url = f"https://{host['ip']}/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate"
    payload = {
        "ImageURI": firmware_url,
        "TransferProtocol": "HTTP"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers, auth=(host['username'], host['password']), verify=False)
    if response.status_code == 202:
        print(f"Firmware update initiated for {host['ip']}")
    else:
        print(f"Failed to initiate firmware update for {host['ip']}")

def main():
    hosts_file = 'hosts.txt'
    target_firmware_version = '2.0.0'  # Replace with your target firmware version
    firmware_update_url = 'firmware.bin'  # Replace with your firmware location http://example.com/firmware.bin

    hosts = read_hosts_from_file(hosts_file)

    for host in hosts:
        current_version = get_current_firmware_version(host)
        if current_version:
            if compare_firmware_versions(current_version, target_firmware_version):
                print(f"Updating firmware for {host['ip']} from {current_version} to {target_firmware_version}")
                update_firmware(host, firmware_update_url)
            else:
                print(f"Firmware is up to date for {host['ip']}: {current_version}")

if __name__ == "__main__":
    main()
