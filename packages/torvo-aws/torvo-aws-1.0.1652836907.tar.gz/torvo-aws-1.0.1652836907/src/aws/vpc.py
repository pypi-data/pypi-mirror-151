"""
    | **Session**

        | aws.session.create()

    | **Properties**
    
        | { 
        |     'Name' = 'string',
        |     'CidrBlock' = 'string',
        |     'AmazonProvidedIpv6CidrBlock' = True|False,
        |     'Ipv6Pool' = 'string',
        |     'Ipv6CidrBlock' = 'string',
        |     'Ipv4IpamPoolId' = 'string',
        |     'Ipv4NetmaskLength' = 123,
        |     'Ipv6IpamPoolId' = 'string',
        |     'Ipv6NetmaskLength' = 123,
        |     'InstanceTenancy' = 'default'|'dedicated'|'host',
        |     'Ipv6CidrBlockNetworkBorderGroup' = 'string',
        |     'Tags' = [
        |         {
        |             'Key': 'string',
        |             'Value': 'string'
        |         }
        |     ]
        |     'EnableDnsSupport': True|False,
        |     'EnableDnsHostnames': True|False
        | }
    
    | **Response** 

        | {
        |     'CidrBlock': 'string',
        |     'DhcpOptionsId': 'string',
        |     'State': 'pending'|'available',
        |     'VpcId': 'string',
        |     'OwnerId': 'string',
        |     'InstanceTenancy': 'default'|'dedicated'|'host',
        |     'Ipv6CidrBlockAssociationSet': [
        |         {
        |             'AssociationId': 'string',
        |             'Ipv6CidrBlock': 'string',
        |             'Ipv6CidrBlockState': {
        |                 'State': 'associating'|'associated'|'disassociating'|'disassociated'|'failing'|'failed',
        |                 'StatusMessage': 'string'
        |             },
        |             'NetworkBorderGroup': 'string',
        |             'Ipv6Pool': 'string'
        |         },
        |     ],
        |     'CidrBlockAssociationSet': [
        |         {
        |             'AssociationId': 'string',
        |             'CidrBlock': 'string',
        |             'CidrBlockState': {
        |                 'State': 'associating'|'associated'|'disassociating'|'disassociated'|'failing'|'failed',
        |                 'StatusMessage': 'string'
        |             }
        |         },
        |     ],
        |     'IsDefault': True|False,
        |     'Tags': [
        |         {
        |             'Key': 'string',
        |             'Value': 'string'
        |         }
        |     ]
        |     'EnableDnsSupport': True|False,
        |     'EnableDnsHostnames': True|False
        | }

"""

import copy

from . import paginate
from . import client

def parse_properties(properties):
    copied_properties = copy.deepcopy(properties)
    tags = copied_properties.get('Tags', [])
    tags.append({ 
        "Key": "Name", 
        "Value": copied_properties.pop('Name')
    })
    copied_properties['TagSpecifications'] = [
        { 
            "ResourceType": "vpc", 
            "Tags": tags
        }
    ]
    return copied_properties

def put_vpc_attributes(session, vpc_id, properties):
    responses = []
    if 'EnableDnsSupport' in properties:
        responses.append(client.create(session, 'ec2').modify_vpc_attribute(
            EnableDnsSupport = { 'Value': properties['EnableDnsSupport'] },
            VpcId = vpc_id
        ))
    if 'EnableDnsHostnames' in properties:
        responses.append(client.create(session, 'ec2').modify_vpc_attribute(
            EnableDnsHostnames = { 'Value': properties['EnableDnsHostnames'] },
            VpcId = vpc_id
        ))
    return responses

def create(session, properties):
    """Create a VPC with the Name tag."""
    parsed_properties = parse_properties(properties)
    create_response = client.create(session, 'ec2').create_vpc(**parsed_properties)
    put_vpc_attributes(session, create_response['Vpc']['VpcId'], parsed_properties)
    return read(session, properties)

def read(session, properties):
    """Read a VPC by the Name tag or return None."""
    describe_responses = paginate.next_token(
        client.create(session, 'ec2').describe_vpcs, 
        Filters = [{ 'Name': 'tag:Name', 'Values': [ properties['Name'] ]}]
    )
    vpcs = []
    for describe_response in describe_responses:
        vpcs.extend(describe_response['Vpcs'])
    if len(vpcs) > 1: 
        raise Exception("Found multiple VPCs with the same name.")
    if len(vpcs) < 1:
        return None
    response = vpcs[0]
    response['EnableDnsSupport'] = client.create(session, 'ec2').describe_vpc_attribute(
        Attribute = 'enableDnsSupport',
        VpcId = response['VpcId']
    )
    response['EnableDnsHostnames'] = client.create(session, 'ec2').describe_vpc_attribute(
        Attribute = 'enableDnsHostnames',
        VpcId = response['VpcId']
    )
    return response

def update(session, properties):
    """Update a VPC with the Name tag."""
    parsed_properties = parse_properties(properties)
    read_response = read(session, properties)
    put_vpc_attributes(session, read_response['VpcId'], parsed_properties)
    if 'InstanceTenancy' in parsed_properties:
        tenancy_response = client.create(session, 'ec2').modify_vpc_tenancy(
            VpcId = read_response['VpcId'],
            InstanceTenancy = parsed_properties['InstanceTenancy']
        )
        if tenancy_response == False:
            raise Exception("Error modify_vpc_tenancy failed")
    return read(session, properties)

def delete(session, properties):
    """Delete a VPC with the Name tag."""
    read_response = read(session, properties)
    if read_response == None:
        return None
    response = client.create(session, 'ec2').delete_vpc(
        VpcId = read_response['VpcId']
    )
    return read(session, properties)

def put(session, properties):
    """Create or Update a VPC with the Name tag."""
    read_response = read(session, properties)
    if read_response == None:
        response = create(session, properties)
    else:
        response = update(session, properties)
    return response
