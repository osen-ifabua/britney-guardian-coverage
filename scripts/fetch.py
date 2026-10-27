import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv
from pathlib import Path

URL = "https://content.guardianapis.com/search"
QUERY = '"Britney Spears"'

#Making a request to API to fetch articles about Britney Spears
def fetch_guardian_articles():
    """ Downloads every page of results for QUERY and returns them as a list"""
  
    load_dotenv()
  
    key = os.getenv("GUARDIAN_KEY")
    if not key:
        raise SystemExit("API key not found. Add to .env file.")

    #Dictionary of parameters to pass to the API 
    params = {
        "q": QUERY,
        "api-key": key,
    }

    #Joining parameters to URL to make request
    response = requests.get(URL, params=params)
    print(response.status_code)

    #Converts reply text into a dictionary
    data = response.json()

  #TEST: Prints number of articles returned and the first article in the list
  #print(data["response"]["total"])
  #print(data["response"]["results"][0])
  
    #Iterate through to fetch every page of results
    all_articles = []
    page = 1
  
    while True:
       
       params = {
            "q": QUERY,
            "page": page,
            "page-size": 50, #max articles per page
            "show-fields": "headline,trailText", #headline and summary line
            "api-key": key,
        }
       
       r = requests.get(URL, params=params)
       r.raise_for_status() #if error
       
       resp = r.json()["response"]
       all_articles.extend(resp["results"]) #adds articles to list individually
       
       print(f"page {page} of {resp['pages']}")
       
       if page >= resp["pages"]:
          break
       
       page += 1
       time.sleep(0.3) #Paces requests so server isn't overwhelmed
       
    return all_articles

#Creates list of dictionaries, one for each article --> row in a table
def to_dataframe(bunch_of_articles):
   
   """Turns list of articles into a table, one row per article"""
   df = pd.DataFrame([{
      "date": a["webPublicationDate"],
      "section": a.get("sectionName"),
      "headline": a.get("fields", {}).get("headline", a["webTitle"]), #Returns article's fields dictionary, if it exists, and then the headline. If not, returns the webTitle
      "trail": a.get("fields", {}).get("trailText"),
      "url": a["webUrl"],
    
    } for a in bunch_of_articles])
   
   df["date"] = pd.to_datetime(df["date"]) #Converts dates from plaintext to Python dates to work with
   df["year"] = df["date"].dt.year #Creates year column

   return df

#Running this script 
if __name__ == "__main__":
    
    fetched_britney = fetch_guardian_articles() #Catch the list of articles returned by the function
    britney_table = to_dataframe(fetched_britney) #Pass the list of articles to the function to create a table

    print(britney_table["date"].min(), britney_table["date"].max()) #Shows date range of fetched articles

    Path("data/raw").mkdir(parents=True, exist_ok=True)
    britney_table.to_csv("data/raw/britney_guardian_raw.csv", index=False) #Saves table to CSV file

    print("Saved to data/raw/britney_guardian_raw.csv")