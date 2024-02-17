#!/usr/bin/env python3

import boto3
from pathlib import Path
import click

s3 = boto3.client("s3")

def get_s3_buckets():
    response = s3.list_buckets()
    return response['Buckets']

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




def initCli(buckets):
    print(buckets)

    click.secho("\nAvaiable buckets:\n")
    for idx, bucket in enumerate(buckets):
        click.secho(f"{idx + 1} - {bucket['Name']}")

    @click.command()
    @click.option('--option', prompt='\nSelect an option', type=int, help='Select an option')
    @click.option('--path',  prompt='\nSet the download path',type=str, help='Set download path')
    def cli(option,path):
        if option == 0 or option > len(buckets):
            return  click.secho(f"Invalid option" , fg='red')

        selected_bucket_name=buckets[option-1]['Name']
        click.secho("Downloading all files ...")

        file_names, folders = get_file_folders(s3,selected_bucket_name)

        with click.progressbar(file_names) as bar:
            download_files(
                s3,
                selected_bucket_name,
                path,
                bar,
                folders
            )
        click.secho( "All files downloaded")

    cli()

if __name__ == "__main__":
     buckets=get_s3_buckets()
     initCli(buckets)
