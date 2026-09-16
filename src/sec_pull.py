import os
from dotenv import load_dotenv

# writes environment variables to os environment
load_dotenv()

# accesses variable from os environment
user_agent = os.getenv("SEC_user_agent")

