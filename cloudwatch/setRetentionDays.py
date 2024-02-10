import argparse
import boto3

cloudwatch = boto3.client("logs")

def get_cloudwatch_log_groups():
    kwargs = {"limit": 50}
    cloudwatch_log_groups = []

    while True:  # Paginate
        response = cloudwatch.describe_log_groups(**kwargs)

        cloudwatch_log_groups += [log_group for log_group in response["logGroups"]]

        if "NextToken" in response:
            kwargs["NextToken"] = response["NextToken"]
        else:
            break
    print(f"\nFound ${len(cloudwatch_log_groups)} log groups\n")
    return cloudwatch_log_groups


def cloudwatch_set_retention(args):
    retention = vars(args)["retention"]
    cloudwatch_log_groups = get_cloudwatch_log_groups()

    for log_group in cloudwatch_log_groups:
        if "retentionInDays" not in log_group or log_group["retentionInDays"] != retention:
            print(f"Updating : {log_group['logGroupName']}")
            cloudwatch.put_retention_policy(
                logGroupName=log_group["logGroupName"], retentionInDays=retention
            )
        else:
            print(
                f"CloudWatch Log group: {log_group['logGroupName']} already has the specified retention of {log_group['retentionInDays']} days."
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="SetRetentionDays",
        description="Set  retention days for all your CloudWatch Logs."
    )
    parser.add_argument(
        "retention",
        metavar="RETENTION",
        type=int,
        choices=[
            1,
            3,
            5,
            7,
            14,
            30,
            60,
            90,
            120,
            150,
            180,
            365,
            400,
            545,
            731,
            1827,
            3653,
        ],
        help="Enter the retention in days for the CloudWatch Logs.",
    )
    args = parser.parse_args()
    cloudwatch_set_retention(args)