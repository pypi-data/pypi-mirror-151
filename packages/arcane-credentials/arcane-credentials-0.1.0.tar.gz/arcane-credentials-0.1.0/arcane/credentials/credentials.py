import json
from typing import Dict, Optional
from google.oauth2.credentials import Credentials
from arcane.datastore import Client as DatastoreClient
from arcane.secret import decrypt
from arcane.core import BadRequestError, USER_OAUTH_CREDENTIAL_KIND

from .exceptions import EmptyCredentialsError



def decrypt_credentials(credentials_encrypt: bytes, secret_key_file: str):
    credentials = json.loads(decrypt(credentials_encrypt, secret_key_file).decode('utf-8'))
    credentials['token'] = None
    return Credentials(**credentials)


def _init_datastore_client(gcp_credentials_path, gcp_project):
    if not gcp_credentials_path and not gcp_project:
            raise BadRequestError('gcp_credentials_path or gcp_project should not be None if datastore_client is not provided')
    return DatastoreClient.from_service_account_json(
            gcp_credentials_path, project=gcp_project)
    
def get_user_crendential_entity(user_email: str, 
                        datastore_client: Optional[DatastoreClient] = None, 
                        gcp_credentials_path: Optional[str] = None, 
                        gcp_project: Optional[str] = None ) -> Dict:
    
    if not datastore_client:
        datastore_client = _init_datastore_client(gcp_credentials_path, gcp_project)
    query = datastore_client.query(kind=USER_OAUTH_CREDENTIAL_KIND).add_filter('email', '=', user_email)
    users_credential = list(query.fetch())
    if len(users_credential) == 0:
        raise BadRequestError(f'Error while getting user credentials with mail: {user_email}. No entity corresponding.')
    elif len(users_credential) > 1:
        raise BadRequestError(f'Error while getting user credentials with mail: {user_email}. Several entities corresponding: {users_credential}')
    return users_credential[0]


def get_user_decrypted_credentials(user_email: str, 
                                   secret_key_file: str, 
                                   gcp_credentials_path: Optional[str], 
                                   gcp_project: Optional[str], 
                                   datastore_client: Optional[DatastoreClient]):
    
    user_credentials = get_user_crendential_entity(user_email, datastore_client, gcp_credentials_path, gcp_project)

    if user_credentials.get('credentials') is None:
        error_message = "Please renew the access you give us. To do so: \n \n" \
            "1 - Please visit: https://myaccount.google.com/permissions \n" \
            "2 - Search for AMS in 'Third-party apps with account access' list \n" \
            "3 - Click on it and press on 'Remove Access' \n" \
            "4 - Close this dialog and try again to add an account \n \n" \
            "If the problem persists, please contact our support team."
        raise EmptyCredentialsError(error_message)

    credentials = decrypt_credentials(user_credentials['credentials'], secret_key_file)
    return credentials
