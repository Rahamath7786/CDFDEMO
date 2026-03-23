import os
from dotenv import load_dotenv
from cognite.client import CogniteClient
from cognite.client.config import ClientConfig
from cognite.client.credentials import OAuthClientCredentials

load_dotenv()

config = ClientConfig(
    client_name="my-django-app",   # any name
    project=os.getenv("CDF_PROJECT"),
    base_url=os.getenv("CDF_BASE_URL"),
    credentials=OAuthClientCredentials(
        token_url=os.getenv("CDF_TOKEN_URL"),
        client_id=os.getenv("CDF_CLIENT_ID"),
        client_secret=os.getenv("CDF_CLIENT_SECRET"),
        scopes=[],
        audience=os.getenv("CDF_AUDIENCE"),
    ),
)

client = CogniteClient(config)