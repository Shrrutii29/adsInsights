import requests
import pandas as pd
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")

# base URL
url = f"https://graph.facebook.com/v22.0/act_{AD_ACCOUNT_ID}/insights"

# parameters for API request
params = {
    "access_token" : ACCESS_TOKEN,
    "fields": "account_id,spend,clicks,impressions,ctr,cpc,cpm,cpp,publisher_platform",
    "level": "ad"
}

# list to store all pages of data
all_data = []

# handle pagination
try:
    while url:
        response = requests.get(url, params=params)
        data = response.json().get("data", [])
        all_data.extend(data)
        
        paging = response.json().get("paging", {})
        url = paging.get("next")
        
        params = {}
        
except Exception as e:
    print(f"Unexpected error occurred: {e}")
      
# save data in csv file
if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv("ads_insights.csv", index=False)
    print(" success - data stored in ads_insights.csv")
else:
    print("No data retrieved")

