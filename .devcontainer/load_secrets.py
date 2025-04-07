import boto3
from botocore.exceptions import ClientError
import json

def get_secret(secret_name: str) -> str:
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

def create_secret_file(secret_json: str):
    """Write secrets to a .env file."""
    try:
        secrets = json.loads(secret_json)  # Ensure the secret is a JSON object
    except json.JSONDecodeError:
        print("Secret is not a valid JSON string.")
        return

    with open("secrets.env", "w") as f:  # Open in write mode
        for key, value in secrets.items():  # Use .items() to iterate correctly
            f.write(f"{key}={value}\n")  # Write each key-value pair

if __name__ == "__main__":
    json_secrets = get_secret("prod-secrets")
    if json_secrets:  # Ensure the secret was retrieved
        create_secret_file(json_secrets)
