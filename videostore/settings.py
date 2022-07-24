"""
All the settings of the application are defined here. 
"""
import dotenv
import os

dotenv.load_dotenv()

DB_URL = os.environ.get("DB_URL")
