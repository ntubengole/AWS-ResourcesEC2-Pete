import boto3

ec2 = boto3.resource('ec2', aws_access_key_id='',
                     aws_secret_access_key='',
                     region_name='')

# create VPC
#provide your cidr block
vpc = ec2.create_vpc(CidrBlock='')
# we can assign a name to vpc, or any resource, by using tag
vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc"}])
vpc.wait_until_available()
print(vpc.id)

# create then attach internet gateway
ig = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
print(ig.id)

# create a route table and a public route
route_table = vpc.create_route_table()
route = route_table.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ig.id
)
print(route_table.id)

# create subnet
#Provide the subnet Cidr
subnet = ec2.create_subnet(CidrBlock='', VpcId=vpc.id)
print(subnet.id)

# associate the route table with the subnet
route_table.associate_with_subnet(SubnetId=subnet.id)

# Create sec group
sec_group = ec2.create_security_group(
    GroupName='secg1', Description='slice_0 sec group', VpcId=vpc.id)
sec_group.authorize_ingress(
    CidrIp='0.0.0.0/0',
    IpProtocol='tcp',
    FromPort=22,
    ToPort=22
)
print(sec_group.id)


# find image id ami-01fee56b22f308154 / us-west-2
# Create instance
instances = ec2.create_instances(
    ImageId='ami-01fee56b22f308154', InstanceType='t2.micro', MaxCount=1, MinCount=1,
    NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_group.group_id]}])
instances[0].wait_until_running()
print(instances[0].id)
print("Your instance is up and running")