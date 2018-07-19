# snapshot-analyser
Demo project to manage AWS EC2 instance snapshots

## About
The project is a demo which uses boto3 to manage AWS EC2 instance snapshots

## Configure
This project requires Python 3 and boto3
It makes use of pipenv to manage the package - you'll need to install pipenv

You will also need an AWS IAM user with CLI access for EC2 instances

```
pip3 install pipenv
pip3 install boto3

aws configure --profile snapshotanaly
```

## Running
```
pipenv run "python snapshotanaly/snapshotanaly.py"`
```