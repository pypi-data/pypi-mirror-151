import click
import os

from qbeast.utils import __qbeast_sharing_profile_path__ as __default_profile__


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("--profile", "-p", help="(WIP) Path to use a different profile for qbeast-sharing")
def main(profile):
    __check_existing_profile__(__default_profile__)

    # TODO: USE custom profile
    if profile is not None:
        print("You can not using a custom profile yet. Using profile from \"{}\"".format(__default_profile__))


# Check that the path for the profile exists
def __check_existing_profile__(profile):
    if not os.path.exists(profile):
        print("The profile path \"{}\" does not exist. Please download your profile and store it in that location" .format(__default_profile__))
        exit(1)