import boto3

ec2 = boto3.client("ec2")


def lambda_handler(event, context):

    # Find instances with Auto-Stop tag
    stop_response = ec2.describe_instances(
        Filters=[
            {
                "Name": "tag:Action",
                "Values": ["Auto-Stop"]
            },
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    )

    for reservation in stop_response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            ec2.stop_instances(
                InstanceIds=[instance_id]
            )

            print(f"Stopped instance: {instance_id}")

    # Find instances with Auto-Start tag
    start_response = ec2.describe_instances(
        Filters=[
            {
                "Name": "tag:Action",
                "Values": ["Auto-Start"]
            },
            {
                "Name": "instance-state-name",
                "Values": ["stopped"]
            }
        ]
    )

    for reservation in start_response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            ec2.start_instances(
                InstanceIds=[instance_id]
            )

            print(f"Started instance: {instance_id}")

    return {
        "statusCode": 200,
        "body": "EC2 automation completed"
    }