import os
from dotenv import load_dotenv
from edgar import set_identity, Company

# writes environment variables to os environment
load_dotenv()

# accesses variable from os environment
user_agent = os.getenv("SEC_user_agent")

set_identity(user_agent)

print(Company("AAPL").get_financials().balance_sheet())
