#! /Users/Gavin/.local/share/virtualenvs/snapshot-analyser-qpeeRxI0/bin/python3

import boto3
import click

# Always create a session connection to AWS
# Create relevant resources
session = boto3.Session(profile_name='pytrain')
ec2 = session.resource('ec2')

# List ec2 instances
@click.command()
def list_instamces():
    "List EC2 instances"
  
    for i in ec2.instances.all():
        print('|'.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            i.private_ip_address,
            i.tags[0]['Value'])))

    return()

if __name__ == '__main__':
    list_instamces()
