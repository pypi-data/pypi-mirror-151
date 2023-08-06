from google.oauth2 import service_account
from google.analytics.admin import AnalyticsAdminServiceClient
from google.api_core.exceptions import PermissionDenied, InvalidArgument

from arcane.ga4.exception import GoogleAnalyticsV4AccountException

class GaV4Client:
    def __init__(
        self,
        property_id: str,
        gcp_service_account: str
    ):
        self.property_id = property_id

        scopes = ['https://www.googleapis.com/auth/analytics.readonly']
        self.credentials = service_account.Credentials.from_service_account_file(gcp_service_account, scopes=scopes)


    def get_property_name(self) -> str:
        client = AnalyticsAdminServiceClient(credentials=self.credentials)

        try:
            property_ = client.get_property(name=f"properties/{self.property_id}")
        except PermissionDenied:
            raise GoogleAnalyticsV4AccountException(f'We cannot access your property with the id: {self.property_id} from the Arcane account. Are you sure you granted access and gave the correct ID?')
        except InvalidArgument as err:
            raise GoogleAnalyticsV4AccountException(str(err))
        return str(property_.display_name)
