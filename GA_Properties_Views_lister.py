from pandas.io.json import json_normalize
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service

service = get_service('analytics', 'v3', scopes='https://www.googleapis.com/auth/analytics.readonly', key_file_location='secret.json' )
account_summaries = service.management().accountSummaries().list().execute()

flat_list=[item for sublist in account_summaries['items'] for item in sublist['webProperties']]
GA_overview=json_normalize(flat_list, record_path=['profiles'],meta=['id','name','websiteUrl'],meta_prefix='_')
print(GA_overview)

writer = pd.ExcelWriter('Google_Analytics_Accounts_Properties_Views.xlsx', engine='xlsxwriter')

GA_overview.to_excel(writer, sheet_name='Sheet1', index=False)

writer.save()
