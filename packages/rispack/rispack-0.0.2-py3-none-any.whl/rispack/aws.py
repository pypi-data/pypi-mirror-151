import json
import os 

from boto3 import client, session
from requests_aws_sign import AWSV4Sign


AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')


def get_signed_auth():
    """Returns a signed uri for calling endpoints with IAM authorization."""

    sess = session.Session()
    credentials = sess.get_credentials()
    service = "execute-api"

    return AWSV4Sign(credentials, AWS_REGION, service)


def get_ssm_parameter(name, encrypted=False):
    """Return a parameter value from the Systems Manger parameter store.

    :param name: The parameter name.
    :param encrypted: Flag indicating if the value is encrypted or not.
    """
    cli = client("ssm")
    param = cli.get_parameter(Name=name, WithDecryption=encrypted)

    return param["Parameter"]["Value"] if param else None


def render_response(code=200, body="", headers={}, base64=False, cors="*"):
    """Return a formatted response for AWS API Gateway.

    :param code: A HTTP status code.
    :param body: The response body as a string, list or dictionary.
    :param headers: A dictionary with the response headers.
    :param base64: Flag indicating if the body is base64 encoded.
    :param cors: CORS allowed domain, default to *.
    """
    headers["Access-Control-Allow-Origin"] = cors

    if isinstance(body, (dict, list)):
        body = json.dumps(body, ensure_ascii=False)

    return {
        "statusCode": code,
        "headers": headers,
        "body": body,
        "isBase64Encoded": base64,
    }


def get_secret(name):
  """Return a secret value from Secrets Manger.

  :param name: The secret name.
  """

  sess = session.Session()

  client = sess.client(
      service_name="secretsmanager", region_name=AWS_REGION
  )

  secret = client.get_secret_value(SecretId=name)

  return secret["SecretString"]

def get_proxy_token(endpoint: str, port: str, user: str):
    session = session.Session()
    client = session.client('rds')

    return client.generate_db_auth_token(
        DBHostname=endpoint,
        Port=port,
        DBUsername=user,
        Region=AWS_REGION,
    )

    