import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = str(os.getenv('SECRET_KEY'))
ALGORITHM = "HS256"