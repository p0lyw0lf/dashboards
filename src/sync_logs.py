#!/usr/bin/env python3

from datetime import date, timedelta
import glob
import importlib.resources as impresources
import os
import subprocess

from secrets import secrets

folder_to_tsv = impresources.files(__name__) / "folder_to_tsv.sh"


def sync_logs(site_name: str, days_delta: int = 28):
    """
    Syncs all logs corresponding to the given site into the cache (not the observablehq one, a local one)
    """
    cfg = secrets[site_name]
    bucket = cfg["AWS_BUCKET_NAME"]
    env = os.environ.copy()
    for var in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION_NAME"]:
        env[var] = cfg[var]

    output_folder = f"tmp/{bucket}"

    # First, sync bucket. This is so we know everything that's inside.
    p = subprocess.run(["aws", "s3", "sync", "--delete",
                       f"s3://{bucket}", output_folder], stdout=subprocess.PIPE, env=env)
    p.check_returncode()

    # Then, find all the folders that are before a certain cutoff
    now = date.today()
    cutoff = now - timedelta(days=days_delta)

    to_remove = []

    # {output_folder}/{yyyy}/{MM}/{dd}
    for folder in glob.iglob(f"{output_folder}/*/*/*/"):
        [year, month, day] = folder[len(output_folder)+1:-1].split("/")
        folder_date = date(int(year), int(month), int(day))
        if folder_date < cutoff:
            to_remove.append(f"{year}/{month}/{day}")

    # Then, remove all those folders
    for folder in to_remove:
        p = subprocess.run(["aws", "s3", "rm", "--recursive",
                           f"s3://{bucket}/{folder}"], stdout=subprocess.PIPE, env=env)
        p.check_returncode()

        p = subprocess.run(
            ["rm", "-rf", f"{output_folder}/{folder}"], stdout=subprocess.PIPE)
        p.check_returncode()

    # Finally, generate the CSV from the given folder
    p = subprocess.run(
        ["bash", str(folder_to_tsv), str(output_folder)])
    p.check_returncode()
