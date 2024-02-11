# CloudWatch Log Tailer

This Python script allows you to tail CloudWatch logs in real-time using the boto3 library. It provides a CLI interface to select a CloudWatch log group and start listening for new log events.

## Prerequisites

Before using this script, ensure you have the following installed:

- Python 3.x
- boto3
- pynput
- click

You can install the required Python packages using pip:

```bash
pip install boto3 pynput click
```

## Usage

1. Clone this repository to your local machine.

2. Navigate to the directory containing the script.

3. Run the script using Python:

```bash
python cloudwatch_log_tailer.py
```

4. Follow the prompts to select a CloudWatch log group and start tailing the logs.

## Features

- Real-time log tailing: Listen for new log events as they are emitted.
- Interactive CLI: Select the CloudWatch log group from a list of available options.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Notes

- Make sure you have AWS credentials properly configured in your local environment to access the S3 bucket.
- This script will not overwrite local files if they already exist in the download path. New files will be downloaded and added to the destination folder.

```
