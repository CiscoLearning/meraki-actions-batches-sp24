import meraki
import csv
import random
import json

# API_KEY = ''

API_KEY = 'fb90cd91db2a93d361af743921d896d015a3477a'

# Instantiate a Meraki dashboard API session
dashboard = meraki.DashboardAPI(API_KEY)


def get_org_id():
    # get the organization ID
    orgs = dashboard.organizations.getOrganizations()
    for org in orgs: # iterate through the list of organizations
        if org['name'] == 'Cisco U.': #
            create_network_batch(org['id']) # create networks in the organization
            break


def create_network_batch(org_id):
    # Create networks in an organization
    payload = []
    with open('inventory.csv', newline='\n', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        actions = []
        for row in reader:
            action = {
                "name": row['Location'].replace(',', ' -'), # replace comma with hyphen
                "productTypes": ['appliance', 'switch', 'wireless', 'camera'], # list of product types
                "tags": random.sample(['foo', 'bar', 'baz', 'spam', 'ham', 'eggs'], 3), # random sample of tags
                "timeZone": row['Timezone'], # timezone from csv file
                "notes": f"Address-{row['Address']}"   # address from csv file
            }
            actions.append({ # append the action to the actions list
                "resource": f"/organizations/{org_id}/networks", # resource path
                "operation": "create", # operation to perform
                "body": action # action to perform
            })
        result = dashboard.organizations.createOrganizationActionBatch(organizationId=org_id, actions=actions, confirmed=True, synchronous=True)

        output_json_file('create_networks.json', actions)

        # Claim devices into an organization
        claim_org_devices(org_id)


def claim_org_devices(org_id):
    # Claim devices into an organization
    devices = []
    with open('inventory.csv', newline='\n', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        mx, mr, ms = [], [], []
        for row in reader:
            mx.append(row['MX device'])
            mr.append(row['MR device'])
            ms.append(row['MS device'])
        devices = mx + mr + ms
    resp = dashboard.organizations.claimIntoOrganization(org_id, serials=devices)

    # Assign devices to networks in an organization
    assign_devices_network(org_id)


def assign_devices_network(org_id):
    # Assign devices to networks in an organization
    with open('inventory.csv', newline='\n', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        actions = []
        for row in reader:
            network_name = row['Location'].replace(',', ' -')
            networks = dashboard.organizations.getOrganizationNetworks(org_id)
            for network in networks:
                if network['name'] == network_name:
                    network_id = network['id']
                    devices = [row['MX device'], row['MR device'], row['MS device']]
                    actions.append({
                        "resource": f"/networks/{network_id}/devices",
                        "operation": "claim",
                        "body": {"serials": devices}
                    })
        result = dashboard.organizations.createOrganizationActionBatch(organizationId=org_id, actions=actions, confirmed=True, synchronous=True)
        output_json_file('claim_devices.json', actions)

        # Configure devices in an organization
        batch_config_devices(org_id)


def batch_config_devices(org_id):
    # Batch configure devices in an organization
    with open('inventory.csv', newline='\n', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        actions = []
        for row in reader:
            network_name = row['Location'].replace(',', ' -')
            networks = dashboard.organizations.getOrganizationNetworks(org_id)
            for network in networks:
                if network['name'] == network_name:
                    network_id = network['id']
                    devices = [(row['MX device'],'MX',row['MX IP']), (row['MR device'],'AP',row['MR IP']), (row['MS device'],'SW',row['MS IP'])]
                    actions.append({
                        'resource': f'/networks/{network_id}/wireless/ssids/0',
                        'operation': 'update',
                        'body': {
                            'number': 0,
                            'name': 'Cisco U. Wifi',
                            'enabled': True,
                            'splashPage': 'None',
                            'ssidAdminAccessible': False,
                            'radiusAccountingEnabled': False
                        }
                    })
                    for (device, type, ip) in devices:
                        if type == 'AP' or type == 'SW':
                            actions.append({
                                'resource': f'/networks/{network_id}/devices/{device}',
                                'operation': 'update',
                                'body': {
                                    'name': type + ' - Device',
                                    'address': row['Address'],
                                    'moveMapMarker': True,
                                    'notes': 'Installed via ActionBatch Automation'
                                }

                            })
                            actions.append({
                                'resource': f'/networks/{network_id}/devices/{device}/managementInterfaceSettings',
                                'operation': 'update',
                                'body': {
                                    'wan1': {
                                        'usingStaticIp': True,
                                        'vlan': row['Mgmt. VLAN'],
                                        'staticIp': ip,
                                        'staticGatewayIp': ip[:-1] + '1',  # strip last digit, and use MX which is .1
                                        'staticSubnetMask': '255.255.255.0',
                                        'staticDns': ['208.67.220.220', '208.67.222.222'],
                                    }
                                }
                            })
                        if type == 'MX':
                            actions.append({
                                'resource': f'/networks/{network_id}/appliance/vlans',
                                'operation': 'create',
                                'body': {
                                    'id': row['Mgmt. VLAN'],
                                    'name': f'Site {type} - Management',
                                    'subnet': f'10.{ip[3:4]}.1.0/24',
                                    'applianceIp': f'{ip}'
                                }
                            })

        result = dashboard.organizations.createOrganizationActionBatch(organizationId=org_id, actions=actions, confirmed=True, synchronous=False)
        output_json_file('config_devices.json', actions)


def output_json_file(filename, actions):
    # Output the actions to a JSON file
    with open(filename, 'w') as fp:
        payload = {
            'confirmed': True,
            'synchronous': False,
            'actions': actions
        }
        json.dump(payload, fp, indent=2)


if __name__ == '__main__':
    # It all starts here
    get_org_id()
