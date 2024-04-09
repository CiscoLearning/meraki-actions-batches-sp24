###### Step 1 - Make a call to the organizations endpoint to get a list of organizations

orgs = dashboard.organizations.getOrganizations()


###### Step 2 - organization ID to create_network_batch function

create_network_batch(org['id']) # create networks in the organization



###### Step 3 - build actions list for batch network creation
- https://developer.cisco.com/meraki/api-v1/supported-resources/ 
- search for: Create a network


"name": row['Location'].replace(',', ' -'), # replace comma with hyphen
"productTypes": ['appliance', 'switch', 'wireless', 'camera'], # list of product types
"tags": random.sample(['foo', 'bar', 'baz', 'spam', 'ham', 'eggs'], 3), # random sample of tags
"timeZone": row['Timezone'], # timezone from csv file
"notes": f"Address-{row['Address']}"   # address from csv file


###### Step 4 - define the resource path, operation and action to perform
"resource": f"/organizations/{org_id}/networks", # resource path
"operation": "create", # operation to perform
"body": action # action to perform


###### Step 5 - call the createOrganizationActionBatch endpoint to create networks in the organization
result = dashboard.organizations.createOrganizationActionBatch(organizationId=org_id, actions=actions, confirmed=True, synchronous=True)


###### Step 6 - build the list of devices to claim into the organization
- https://developer.cisco.com/meraki/api-v1/claim-network-devices/

mx.append(row['MX device'])
mr.append(row['MR device'])
ms.append(row['MS device'])



###### Step 7 - call the claimIntoOrganization endpoint to claim devices into the organization


resp = dashboard.organizations.claimIntoOrganization(org_id, serials=devices)



###### Step 8 - build the action to assign devices to networks
- https://developer.cisco.com/meraki/api-v1/supported-resources/ 
- search for: Claim devices into a network

"resource": f"/networks/{network_id}/devices",
"operation": "claim",
"body": {"serials": devices}



##### Step 9 - call the claimIntoOrganization endpoint to claim devices into the organization
 result = dashboard.organizations.createOrganizationActionBatch(organizationId=org_id, actions=actions, confirmed=True, synchronous=True)



##### Step 10 - build the action to configure Wireless Network in the organization
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



###### Step 11 - build the action to configure Wireless Network in the organization
'resource': f'/networks/{network_id}/devices/{device}',
'operation': 'update',
'body': {
    'name': type + ' - Device',
    'address': row['Address'],
    'moveMapMarker': True,
    'notes': 'Installed via ActionBatch Automation'



###### Step 12 - build the action for management VLAN configuration
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




###### Step 13 - build the action for MX L3 firewall configuration
'resource': f'/networks/{network_id}/appliance/vlans',
'operation': 'create',
'body': {
    'id': row['Mgmt. VLAN'],
    'name': f'Site {type} - Management',
    'subnet': f'10.{ip[3:4]}.1.0/24',
    'applianceIp': f'{ip}'




###### Step 14 - call the createOrganizationActionBatch endpoint to configure devices in the organization
result = dashboard.organizations.createOrganizationActionBatch(organizationId=org_id, actions=actions, confirmed=True, synchronous=False)





