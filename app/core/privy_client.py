from privy import PrivyAPI
from dotenv import load_dotenv
import os


load_dotenv()
PRIVY_APP_ID = os.getenv("PRIVY_APP_ID")
PRIVY_APP_SECRET = os.getenv("PRIVY_APP_SECRET")

privy_client = PrivyAPI(
    app_id=PRIVY_APP_ID,
    app_secret=PRIVY_APP_SECRET
)