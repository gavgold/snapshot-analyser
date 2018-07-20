import boto3

# Always create a session connection to AWS
# Create relevant resources
session = boto3.Session(profile_name='pytrain')
ec2 = session.resource('ec2')

# List ec2 instances
def list_instamces():
    for i in ec2.instances.all():
        print(i.instance_id,i.key_name,i.state)

if __name__ == '__main__':
    list_instamces()
