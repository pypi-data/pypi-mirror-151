"""
    | **Session**

        | boto3.session.Session()

    | **Properties**
    
        | { 
        |     Name = 'string',
        |     CidrBlock = 'string',
        |     AmazonProvidedIpv6CidrBlock = True|False,
        |     Ipv6Pool = 'string',
        |     Ipv6CidrBlock = 'string',
        |     Ipv4IpamPoolId = 'string',
        |     Ipv4NetmaskLength = 123,
        |     Ipv6IpamPoolId = 'string',
        |     Ipv6NetmaskLength = 123,
        |     InstanceTenancy = 'default'|'dedicated'|'host',
        |     Ipv6CidrBlockNetworkBorderGroup = 'string',
        |     Tags = [
        |         {
        |             'Key': 'string',
        |             'Value': 'string'
        |         }
        |     ]
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
        | }

"""

import boto3

from . import paginate

def parse_properties(properties):
    if 'Tags' in properties and 'TagSpecifications' not in properties:
        properties['TagSpecifications'] = [
            { 
                "ResourceType": "vpc", 
                "Tags": properties['Tags'] 
            }
        ]
    return properties

def create(session, properties):
    """Create a VPC with the Name tag."""
    properties = parse_properties(properties)
    return

def update(session, properties):
    """Update a VPC with the Name tag."""
    return

def delete(session, properties):
    """Delete a VPC with the Name tag."""
    return

def put(session, properties):
    """Create or Update a VPC with the Name tag."""
    return

def read(session, properties):
    """Read a VPC by the Name tag or return None."""
    responses = paginate.next_token(
        session.client('ec2').describe_vpcs(
            Filters = [{ 'Name': 'tag:Name', 'Values': [ properties['Name'] ]}]
        )
    )
    vpcs = []
    for response in responses:
        vpcs.extend(response['Vpcs'])
    if len(vpcs) > 1: 
        raise Exception("Found multiple VPCs with the same name.")
    elif len(vpcs) == 1:
        return vpcs[0]
    else: 
        return None

# response = client.modify_vpc_attribute(
#     EnableDnsHostnames={
#         'Value': True|False
#     },
#     EnableDnsSupport={
#         'Value': True|False
#     },
#     VpcId='string'
# )

# response = client.describe_vpc_attribute(
#     Attribute='enableDnsSupport'|'enableDnsHostnames',
#     VpcId='string',
#     DryRun=True|False
# )

# def read(session, **kwargs):
#     client = _client(session)
#     describe_response = client.describe_vpcs(
#         Filters = [{ 'Name': 'tag:Name', 'Values': [ kwargs['Name'] ] }]
#     )
#     if len(describe_response) > 1: raise Exception("Found multiple VPCs with the same name.")
#     return 

# vpc_name = "vpc_iac_example"
# print("Reading VPC")
# describe_response = boto3.client('ec2').describe_vpcs(
#     Filters = [{ 'Name': 'tag:Name', 'Values': [ vpc_name ] }]
# )
# if len(describe_response['Vpcs']) > 1: raise Exception("Found multiple vpcs with the name: " + vpc_name)
# print(json.dumps(describe_response['Vpcs'], indent = 2))

# def create(session, **kwargs):
#     client = _client(session)
#     vpc_response = client.create_vpc(
#         CidrBlock = kwargs['CidrBlock'],
#         TagSpecifications = [{
#             'Tags': [{ 'Key': 'Name', 'Value': kwargs['Name'] }]
#         }]
#     )
#     return
# create_response = boto3.client('ec2').create_vpc(
#             CidrBlock = '10.0.0.0/16',
#             TagSpecifications = [{ 
#                 'ResourceType': 'vpc',
#                 'Tags': [ { 'Key': 'Name', 'Value': vpc_name } ]
#             }]
#         )
#         print(json.dumps(create_response['Vpc'], indent = 2))

# def update():
#     response = client.modify_vpc_attribute(
#         EnableDnsHostnames = { 'Value': enable_dns_hostnames },
#         EnableDnsSupport = { 'Value': enable_dns_support },
#         VpcId = describe_response['Vpcs']['VpcId']
#     )
#     return





