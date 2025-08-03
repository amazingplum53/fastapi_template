import boto3
from botocore.exceptions import ClientError
import json
from os import environ

SECRETS_FILE_NAME = "secrets"
AWS_SECRET_NAME = "prod-secrets"
FILE_PATH = "/server/decouple/decouple/secret"


def get_secret(secret_name: str = AWS_SECRET_NAME) -> str:
    """Fetch a secret from AWS Secrets Manager."""
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        return None

    secret = get_secret_value_response.get('SecretString', None)

    if not secret:
        print("No secret found or it's binary data.")
        return None

    return secret


def create_secret_file(secret_json: str, file_name: str = SECRETS_FILE_NAME):
    """Write secrets to a .env file."""
    try:
        secrets = json.loads(secret_json)  # Ensure the secret is a JSON object
    except json.JSONDecodeError:
        print("Secret is not a valid JSON string.")
        return

    with open(f"{FILE_PATH}/{file_name}.json", 'w') as f:
        json.dump(secrets, f, indent=4)

    output = ""

    for key, value in secrets.items():
        output += f'export {key}="{value}"\n'

    with open(f"{FILE_PATH}/{file_name}.source", "w") as f:
        f.write(output)


def load_secrets_file(file_name: str = SECRETS_FILE_NAME):

    try:
        secrets = {}

        with open(f"{FILE_PATH}/{file_name}.json", "r") as f:
            secrets = json.loads(f.read())

    except json.JSONDecodeError:
        print("Secret is not a valid JSON string.")
        return  

    output = ""

    for key, value in secrets.items():
        environ[key] = value


if __name__ == "__main__":

    json_secrets = get_secret(AWS_SECRET_NAME)

    create_secret_file(json_secrets)

    load_secrets_file()

    print(environ.get("pulumi_access_token"))
    
