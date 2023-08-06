"""Configuration."""
import os

CLIENT_ID = "5f0ef15fa8037afc5992380960561151"
DEFAULT_SHOP = ""
AUTH_TIMEOUT = 240

CLI_ENV = os.getenv("CLI_ENV", "prod")

# product environment, use .com domain
if CLI_ENV == "prod":
    ACCOUNT_API_URL = "https://accounts.funpinpin.com/api"
    PARTNER_API_URL = "https://partners.funpinpin.com/api"
    DOMAIN_SUFFIX = "com"
else:
    ACCOUNT_API_URL = "https://accounts.funpinpin.top/api"
    PARTNER_API_URL = "https://partners.funpinpin.top/api"
    DOMAIN_SUFFIX = "top"

REDIRECT_URI = "http://127.0.0.1:3456"
