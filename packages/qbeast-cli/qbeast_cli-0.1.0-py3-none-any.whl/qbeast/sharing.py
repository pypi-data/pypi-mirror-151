import click
import requests
import json

from qbeast.main import main
from qbeast.utils import __qbeast_sharing_profile_path__ as profile_file
from qbeast.utils import get_aws_credentials

@main.group()
def expo():
    """qbeast-sharing commands"""
    pass

@expo.command("create")
@click.argument("path")
@click.argument("share_name")
@click.argument("schema_name")
@click.argument("table_name")
@click.option("--percentage", "-p", default=100, help="Percentage of data to share")
def create(path, share_name, schema_name, table_name, percentage):
    """Create a new share"""

    # Load profile with credentials
    qbeast_sharing_profile = json.loads(open(profile_file).read())

    # Load S3 credentials from profile
    aws_region, aws_access_key, aws_secret_access_key = get_aws_credentials()
    
    # Prepare requests
    headers = dict()
    headers["Authorization"] = f"Bearer {qbeast_sharing_profile['bearerToken']}"
    endpoint = qbeast_sharing_profile['endpoint']


    # Send request to create a SHARE
    body_json = {"name": share_name,
                 "description": "Share created with qbeast CLI"}
    new_share = requests.post(f"{endpoint}/shares",
                          headers=headers,
                          json=body_json)
    new_share_name = ""
    if new_share.status_code == 201: # Created
        new_share_name = new_share.json()["name"]
        print(f"Share created:\n\t Name of the new share: '{new_share_name}'")
    else:
        raise Exception(f"Error creating share: {new_share.text}")

    # Send request to add a SCHEMA to the share
    body_json = {"name": schema_name,
                 "description": "Schema created with qbeast CLI"}
    new_schema = requests.post(f"{endpoint}/shares/{new_share_name}/schemas",
                           headers=headers,
                           json=body_json)
    new_schema_name = ""
    if new_schema.status_code == 201: # Created
        new_schema_name = new_schema.json()["name"]
        print(f"Schema added to the share '{new_share_name}':\n\t Name of the new schema: '{new_schema_name}'")
    else:
        raise Exception(f"Error adding schema to share: {new_schema.text}")

    # Send request to add TABLE to the schema
    storage_config = {"type": "S3",
                      "region": aws_region,
                      "bucket": path.split("/")[2],
                      "path": path,
                      "accessKey": aws_access_key,
                      "secretAccessKey": aws_secret_access_key}
    body_json = {"name": table_name,
                "storage": storage_config,
                "format": {
                    "type": "Qbeast",
                    "precision": percentage / 100
                },
                "presignedUrlValidityPeriod": 60,
                "description": "Table created with qbeast CLI"}
    new_table = requests.post(f"{endpoint}/shares/{new_share_name}/schemas/{new_schema_name}/tables",
                          headers=headers,
                          json=body_json)
    new_table_name = ""
    if new_table.status_code == 201: # Created
        new_table_name = new_table.json()["name"]
        print(f"Table added to the schema '{new_schema_name}' of the share '{new_share_name}':\n\t Name of the new table: '{new_table_name}'")
    else:
        raise Exception(f"Error adding table to schema: {new_table.text}")


@expo.command("invite")
@click.argument("share_name")
@click.argument("invitee_name")
@click.argument("invitee_email")
def invite(share_name, invitee_name, invitee_email):
    """Invite a user to a share"""
    qbeast_sharing_profile = json.loads(open(profile_file).read())
    headers = dict()
    headers["Authorization"] = f"Bearer {qbeast_sharing_profile['bearerToken']}"
    endpoint = qbeast_sharing_profile['endpoint']

    body_json = {"share": share_name,
                 "inviteeName": invitee_name,
                 "inviteeEmail": invitee_email}
    
    invitation = requests.post(f"{endpoint}/invitations",
                           headers=headers,
                           json=body_json)
    if invitation.status_code == 201:
        print(f"Invitation sent to {invitee_name} ({invitee_email})")
    else:
        raise Exception(f"Error inviting user: {invitation.text}")