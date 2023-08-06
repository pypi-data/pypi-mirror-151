from os import getenv
from opentmi_client import OpenTmiClient

client = OpenTmiClient(host=getenv('OPENTMI_HOST'))
client.login_with_access_token(access_token=getenv('GITHUB_ACCESS_TOKEN'))
