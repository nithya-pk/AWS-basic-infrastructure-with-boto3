import boto3

# create an EC2 client
ec2 = boto3.client('ec2')

# parameters for the instance
image_id = 'ami-0df24e148fdb9f1d8'  
instance_type = 't3.micro'
key_name = 'vockey'
security_group_id = 'sg-01ef55bd3e10fa230'  
subnet_id = 'subnet-03b119f5fa6ebc76d'  
max_count = 1
min_count = 1

# launch the new instance
response = ec2.run_instances(
    ImageId=image_id,
    InstanceType=instance_type,
    KeyName=key_name,
    MaxCount=max_count,
    MinCount=min_count,
    NetworkInterfaces=[{
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'SubnetId': subnet_id,
        'Groups': [security_group_id]
    }]
)

instance_id = response['Instances'][0]['InstanceId']

# add a name tag to the instance
instance_name = 'MyEC2Instance'

ec2.create_tags(Resources=[instance_id], Tags=[{"Key": "Name", "Value": instance_name}])

print(f"Launched EC2 instance {instance_id} in subnet {subnet_id}")