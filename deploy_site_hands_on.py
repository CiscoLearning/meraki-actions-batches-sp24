import meraki
import csv
import random
import json


API_KEY = 'fb90cd91db2a93d361af743921d896d015a3477a'

# Instantiate a Meraki dashboard API session
dashboard = meraki.DashboardAPI(API_KEY)


def get_org_id():
    # get the organization ID
    # Step 1 - Make a call to the organizations endpoint to get a list of organizations
    #
    #
    #
    orgs = dashboard.organizations.getOrganizations()
    for org in orgs: # iterate through the list of organizations
        if org['name'] == 'Cisco U.': #
              # Step 2 - organization ID to create_network_batch function
              #
              #
              #
              create_network_batch(org['id'])

            break


def create_network_batch(org_id):
    # Create networks in an organization
    payload = []
    with open('inventory.csv', newline='\n', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        actions = []
        for row in reader:
            action = {
              # Step 3 - build actions list for batch network creation
              #
              #
            }
            actions.append({ # append the action to the actions list
                # Step 4 - define the resource path, operation and action to perform
                #
                #
                #
            })
        # Step 5 - call the createOrganizationActionBatch endpoint to create networks in the organization
        #
        #
        # result =

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
            # Step 6 - build the list of devices to claim into the organization
            #
            #
            #
        devices = mx + mr + ms
    # Step 7 - call the claimIntoOrganization endpoint to claim devices into the organization
    #
    #
    # resp =

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
                        # Step 8 - build the action to assign devices to networks
                        #
                        #
                        #
                    })
        # Step 9 - call the claimIntoOrganization endpoint to claim devices into the organization
        #
        #
        # result =
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
                        # Step 10 - build the action to configure Wireless Network in the organization
                        #
                        #
                        #
                    })
                    for (device, type, ip) in devices:
                        if type == 'AP' or type == 'SW':
                            actions.append({
                                # Step 11 - build the action to configure Wireless Network in the organization
                                #
                                #
                                #
                            })
                            actions.append({
                                # Step 12 - build the action for management VLAN configuration
                                #
                                #
                                #
                            })
                        if type == 'MX':
                            actions.append({
                                # Step 13 - build the action for MX L3 firewall configuration
                                #
                                #
                                }
                            })

        # Step 14 - call the createOrganizationActionBatch endpoint to configure devices in the organization
        #
        #
        # result = dashboard.organizations.createOrganizationActionBatch(organizationId=org_id, actions=actions, confirmed=True, synchronous=False)
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
