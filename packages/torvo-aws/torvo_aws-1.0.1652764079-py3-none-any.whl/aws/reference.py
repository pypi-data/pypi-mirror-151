
import boto3

def next_token(function, *args, **kwargs):
    responses = []
    while True:
        response = function(*args, **kwargs)
        if 'NextToken' in response:
            kwargs['NextToken'] = response['NextToken']
        else:
            break
    return responses

def read(session = None, properties = {}):
    if session = None:
        session = boto3.session.Session()
    client = session.client('ec2')
    describe_properties = {
        "Filters": [{ 'Name': 'tag:Name', 'Values': [ name ]}]
    }
    while True:
        describe_response = client.describe_vpcs(**describe_properties)
        if 'NextToken' in describe_response:
            describe_properties['NextToken'] = describe_response['NextToken']
        else:
            break
    if len(describe_response['Vpcs']) > 1: 
        raise Exception("Found multiple VPCs with the same name.")
    else if len(describe_response['Vpcs']) == 1:
        return describe_response['Vpcs'][0]
    else: 
        return None








        create_response = client.create_vpc(
            CidrBlock = cidr,
            TagSpecifications = [{'Tags': [{ 'Key': 'Name', 'Value': name }]}]
        )
    else:
        response = client.modify_vpc_attribute(
            EnableDnsHostnames = { 'Value': enable_dns_hostnames },
            EnableDnsSupport = { 'Value': enable_dns_support },
            VpcId = describe_response['Vpcs']['VpcId']
        )
    return   


    import boto3

    def _client(session):
        return session.client('ec2')

    def create(session, **kwargs):
        client = _client(session)
        vpc_response = client.create_vpc(
            CidrBlock = kwargs['CidrBlock'],
            TagSpecifications = [{
                'Tags': [{ 'Key': 'Name', 'Value': kwargs['Name'] }]
            }]
        )
        return

    def read(session, **kwargs):
        client = _client(session)
        describe_response = client.describe_vpcs(
            Filters = [{ 'Name': 'tag:Name', 'Values': [ kwargs['Name'] ] }]
        )
        if len(describe_response) > 1: raise Exception("Found multiple VPCs with the same name.")
        return 

    vpc_name = "vpc_iac_example"
    print("Reading VPC")
    describe_response = boto3.client('ec2').describe_vpcs(
        Filters = [{ 'Name': 'tag:Name', 'Values': [ vpc_name ] }]
    )
    if len(describe_response['Vpcs']) > 1: raise Exception("Found multiple vpcs with the name: " + vpc_name)
    print(json.dumps(describe_response['Vpcs'], indent = 2))

    hello world

    if len(describe_response['Vpcs']) == 0:
        print("Creating VPC")
        create_response = boto3.client('ec2').create_vpc(
            CidrBlock = '10.0.0.0/16',
            TagSpecifications = [{ 
                'ResourceType': 'vpc',
                'Tags': [ { 'Key': 'Name', 'Value': vpc_name } ]
            }]
        )
        print(json.dumps(create_response['Vpc'], indent = 2))
    else:
        print("Updating VPC")
        
        # Update

