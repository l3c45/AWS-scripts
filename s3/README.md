# Download Files from Amazon S3 Bucket

This Python script allows you to download all files from an Amazon S3 bucket to a local location.

## Prerequisites

Before running this script, make sure you have Python and the necessary libraries installed:

- Python 3.x
- boto3
- argparse

You can install the dependencies with the following command:

```bash
pip install boto3 argparse
```

## Usage

1. Clone this repository to your local machine:

```bash
git clone <repository URL>
cd <repository name>
```

2. Run the `downloadAllFiles.py` script specifying the name of the S3 bucket and the local path where you want to save the downloaded files:

```bash
python downloadAllFiles.py <bucket-name> <local-path>
```

For example:

```bash
python downloadAllFiles.py my-bucket /download/path
```

## Parameters

- `<bucket-name>`: Name of the Amazon S3 bucket from which you want to download the files.
- `<local-path>`: Local path where you want to save the downloaded files.

## Notes

- Make sure you have AWS credentials properly configured in your local environment to access the S3 bucket.
- This script will not overwrite local files if they already exist in the download path. New files will be downloaded and added to the destination folder.

```
