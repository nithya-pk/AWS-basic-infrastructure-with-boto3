
import boto3

# create a new VPC
ec2 = boto3.resource('ec2')

vpc_cidr = '10.0.0.0/16'
vpc_name = 'nk-vpc'

vpc = ec2.create_vpc(CidrBlock=vpc_cidr)

# add a name tag to the VPC
vpc.create_tags(Tags=[{"Key": "Name", "Value": vpc_name}])

# enable DNS support and hostnames for the VPC
vpc.modify_attribute(
    EnableDnsSupport={'Value': True}
)
vpc.modify_attribute(
    EnableDnsHostnames={'Value': True}
)

# create an internet gateway and attach it to the VPC
gateway_name = 'nk-igw'

gateway = ec2.create_internet_gateway()
gateway.create_tags(Tags=[{"Key": "Name", "Value": gateway_name}])

vpc.attach_internet_gateway(InternetGatewayId=gateway.id)

# create a route table and a public route for the internet gateway
route_table_name = 'nk-routetable'

route_table = vpc.create_route_table()
route_table.create_tags(Tags=[{"Key": "Name", "Value": route_table_name}])

route_table.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=gateway.id
)

# create a publicsubnet in the VPC
subnet_cidr = '10.0.0.0/24'
subnet_name = 'MySubnet'

subnet = ec2.create_subnet(
    CidrBlock=subnet_cidr,
    VpcId=vpc.id
)

# add a name tag to the subnet
subnet.create_tags(Tags=[{"Key": "Name", "Value": subnet_name}])

# associate the subnet with the route table
route_table.associate_with_subnet(SubnetId=subnet.id)

# create a security group for the VPC
security_group_name = 'MySecurityGroup'

security_group = ec2.create_security_group(
    GroupName=security_group_name,
    Description='My security group',
    VpcId=vpc.id
)

# allow incoming SSH traffic to the security group
security_group.authorize_ingress(
    IpPermissions=[{
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }]
)

print("VPC created successfully!")
