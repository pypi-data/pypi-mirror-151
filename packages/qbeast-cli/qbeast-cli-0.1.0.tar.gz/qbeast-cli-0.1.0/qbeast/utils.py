import os


# Qbeast CLI version definition
__version__ = "0.1.0"

# Qbeast-sharing default profile path
home_dir = os.path.expanduser("~")
__qbeast_sharing_profile_path__ = home_dir + "/.qbeast/profile.txt"


def get_aws_credentials():
    """
    Get AWS credentials from the aws CLI.
    """
    if os.path.exists(home_dir + "/.aws/config") and os.path.exists(home_dir + "/.aws/credentials"):
        aws_cfg = open(home_dir + "/.aws/config").read()
        aws_cred = open(home_dir + "/.aws/credentials").read()
        # TODO: Get other than first profile
        aws_region = aws_cfg.split("\n")[1].split("=")[1]
        aws_access_key = aws_cred.split("\n")[1].split("=")[1]
        aws_secret_access_key = aws_cred.split("\n")[2].split("=")[1]
        
        return (aws_region, aws_access_key, aws_secret_access_key)
    else:
        raise Exception("AWS credentials not found. Please run \"aws configure\"")