#! /Users/Gavin/.local/share/virtualenvs/snapshot-analyser-qpeeRxI0/bin/python3

import boto3
import click

# Always create a session connection to AWS
# Create relevant resources
session = boto3.Session(profile_name='pytrain')
ec2 = session.resource('ec2')

# List ec2 instances
@click.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project',default=None,
    help='Only instances for project (tag Project:<name>)')
def list_instamces(project):
    "List EC2 instances"
  
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        tags = {t['Key']:t['Value'] for t in i.tags or []}
        print('|'.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            i.private_ip_address,
            tags.get('Project', 'No Project'),
            tags.get('Name', 'No Name'))))

    return()

@instances.command('stop')
@click.option('--project',default=None,
    help='Only instances for project (tag Project:<name>)')
def stop_instamces(project):
    "Stop EC2 instances"
  
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        tags = {t['Key']:t['Value'] for t in i.tags or []}
        
        if i.state['Name'] == 'stopped':
            print('Instance {0} {1} is alredy {2}'.format(i.id,tags.get('Name', 'No Name Avail'),i.state['Name'])) 
        elif not i.state['Name'] == 'running':
            print('Instance {0} {1} is not in a running state - {2}'.format(i.id,tags.get('Name', 'No Name Avail'),i.state['Name']))
        else:
            print('Stopping instance {0} {1} - {2}'.format(i.id,tags.get('Name', 'No Name Avail'),i.state['Name']))
            i.stop()

if __name__ == '__main__':
    instances()
