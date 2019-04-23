RESOURCE = "https://graph.microsoft.com"  # Add the resource you want the access token for
TENANT = "Your tenant"  # Enter tenant name, e.g. contoso.onmicrosoft.com
AUTHORITY_HOST_URL = "https://login.microsoftonline.com"
CLIENT_ID = "Your client id "  # copy the Application ID of your app from your Azure portal
CLIENT_SECRET = "Your client secret"  # copy the value of key you generated when setting up the application

ISSUER = "https://sts.windows.net/<tenant>" # Identifies the security token service (STS) that constructs and returns the token, and the Azure AD tenant in which the user was authenticated.
EMAIL_DOMAINS = ["workplace.com"] # List of domains to accept.