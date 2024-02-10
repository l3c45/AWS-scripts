import argparse
import boto3
from pathlib import Path

s3 = boto3.client("s3")

def get_file_folders(s3_client, bucket_name, prefix=""):
    file_names = []
    folders = []

    default_kwargs = {
        "Bucket": bucket_name,
        "Prefix": prefix
    }
    next_token = ""

    while next_token is not None:
        updated_kwargs = default_kwargs.copy()
        if next_token != "":
            updated_kwargs["ContinuationToken"] = next_token

        response = s3_client.list_objects_v2(**default_kwargs)
        contents = response.get("Contents")

        for result in contents:
            key = result.get("Key")
            if key[-1] == "/":
                folders.append(key)
            else:
                file_names.append(key)

        next_token = response.get("NextContinuationToken")

    return file_names, folders



def download_files(s3_client, bucket_name, local_path, file_names, folders):
    local_path = Path(local_path)

    for folder in folders:
        folder_path = Path.joinpath(local_path, folder)
        folder_path.mkdir(parents=True, exist_ok=True)

    for file_name in file_names:
        file_path = Path.joinpath(local_path, file_name)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        s3_client.download_file(
            bucket_name,
            file_name,
            str(file_path)
        )



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="downloadAllFiles",
        description="Download all files from s3 bucket."
    )
    parser.add_argument(
        "bucket-name",
        metavar="BUCKET",
        type=str,
        help="Enter the bucket name.",
    )
    parser.add_argument(
        "download-path",
        metavar="PATH",
        type=str,
        help="Enter the path where save files.",
    )
    args = parser.parse_args()
    bucket_name = vars(args)["bucket-name"]
    download_path = vars(args)["download-path"]

    file_names, folders = get_file_folders(s3,bucket_name)

    download_files(
        s3,
        bucket_name,
        download_path,
        file_names,
        folders
    )
