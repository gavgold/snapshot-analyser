#! /Users/Gavin/.local/share/virtualenvs/snapshot-analyser-qpeeRxI0/bin/python3

import boto3
import click

# Always create a session connection to AWS
# Create relevant resources
session = boto3.Session(profile_name='pytrain')
ec2 = session.resource('ec2')

def filter_instances(project):
    "Filter instances based on supplied project"

    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

# cli group of commands
@click.group()
def cli():
    """Snapshot Analyser manages instances and snapshots"""

@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--project',default=None,
    help='Only volumes for instances for the supplied project (tag Project:<name>)')
def list_volumes(project):
    "List volumes"

    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key']:t['Value'] for t in i.tags or []}
        for v in i.volumes.all():
          print(", ".join((
          i.id,
          v.id,
          v.state,
          v.volume_type,
          str(v.size) + "GiB",
          v.encrypted and "Encrypted" or "Not Encrypted",
          tags.get('Project', 'No Project'),
          tags.get('Name', '-')
        )))
    return()
   
@cli.group('snapshots')
def snapshots():
    """Commands for volumes"""

@snapshots.command('list')
@click.option('--project',default=None,
    help='Only snapshots of volumes for instances for the supplied project (tag Project:<name>)')
def list_snapshots(project):
    "List snapshots"

    instances = filter_instances(project)

    for i in instances:
      tags = {t['Key']:t['Value'] for t in i.tags or []}
      for v in i.volumes.all():
        for s in v.snapshots.all():
            print(", ".join((
              i.id,
              v.id,
              v.volume_type,
              str(v.size) + "GiB",
              s.id,
              s.start_time.strftime("%c"),
              s.progress,
              s.state,
              s.description,
              tags.get('Project', 'No Project'),
              tags.get('Name', '-')
              )))
    return()

# List ec2 instances
@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project',default=None,
    help='Only instances for the supplied project (tag Project:<name>)')
def list_instamces(project):
    "List EC2 instances"
  
    instances = filter_instances(project)

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
            tags.get('Name', '-'))))

    return()

@instances.command('stop')
@click.option('--project',default=None,
    help='Only instances for project (tag Project:<name>)')
def stop_instamces(project):
    "Stop EC2 instances"
  
    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key']:t['Value'] for t in i.tags or []}
        
        if i.state['Name'] == 'stopped':
            print('Instance {0} {1} is alredy {2}'.format(i.id,tags.get('Name', 'No Name Avail'),i.state['Name'])) 
        elif not i.state['Name'] == 'running':
            print('Instance {0} {1} is not in a running state - current state is {2}'.format(i.id,tags.get('Name', 'No Name Avail'),i.state['Name']))
        else:
            print('Stopping instance {0} {1} - current state is {2}'.format(i.id,tags.get('Name', 'No Name Avail'),i.state['Name']))
            i.stop()
        return


@instances.command('start')
@click.option('--project',default=None,
    help='Only instances for project (tag Project:<name>)')
def start_instamces(project):
    "Start EC2 instances"
  
    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key']:t['Value'] for t in i.tags or []}
        
        if i.state['Name'] == 'running':
            print('Instance {0} {1} is alredy {2}'.format(i.id,tags.get('Name', 'No Name Avail'),i.state['Name'])) 
        elif not i.state['Name'] == 'stopped':
            print('Instance {0} {1} is not in a stopped state - current state is {2}'.format(i.id,tags.get('Name', 'No Name Avail'),i.state['Name']))
        else:
            print('Starting instance {0} {1} - current state is {2}'.format(i.id,tags.get('Name', 'No Name Avail'),i.state['Name']))
            i.start()
        return

@instances.command('snapshot')
@click.option('--project',default=None,
    help='Only instances for the supplied project (tag Project:<name>)')
def create_snapshot(project):
    "Create snapshot of EC2 instance volumes"
  
    instances = filter_instances(project)

    for i in instances:
      tags = {t['Key']:t['Value'] for t in i.tags or []}
      for v in i.volumes.all():
        # i.stop()
        # i.wait_until_stopped()
        v.create_snapshot(
            Description='created by snapshotanaly',
            DryRun=False
        )
        print(", ".join((
            "Creating snapshot: ",
            i.id,
            v.id,
            v.volume_type,
            str(v.size) + "GiB",
            tags.get('Project', 'No Project'),
            tags.get('Name', '-')
            )))
        # i.start()

    return()

if __name__ == '__main__':
    cli()
