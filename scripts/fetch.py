import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

#Making a request to API to fetch articles about Britney Spears
def fetch_guardian_articles():

  load_dotenv()
  
  key = os.getenv("GUARDIAN_KEY")
  if not key:
    raise SystemExit("API key not found. Add to .env file.")
  
  url = "https://content.guardianapis.com/search"

  #Dictionary of parameters to pass to the API 
  params = {
    "q": ' "Britney Spears" ',
    "api-key": key,
    }

  #Joining parameters to URL to make request
  response = requests.get(url, params=params)
  print(response.status_code)

  #Converts reply text into a dictionary
  data = response.json()

  #Prints number of articles returned and the first article in the list
  print(data["response"]["total"])
  print(data["response"]["results"][0])
  
  #Iterate through to fetch every page of results
  all_articles = []
  page = 1
  
  while True:
     
     params = {"q": ' "Britney Spears" ',
        "page": page,
        "page-size": 50, #max no. of articles per page
        "show-fields": "headline, trailText", #headline and summary
        "api-key": key,
        }
     
     r = requests.get(url, params=params)
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
  df = pd.DataFrame([{
  
  "date": a["webPublicationDate"],
  "section": a.get("sectionName"),
  "headline": a.get("fields", {}).get("headline", a["webTitle"]), #???
  "trail": a.get("fields", {}).get("trailText"),
  "url": a["webUrl"],
    
    } for a in bunch_of_articles])

  df["date"] = pd.to_datetime(df["date"])
  df["year"] = df["date"].dt.year

  print(df["date"].min(), df["date"].max())
  df.head() #Shows format of first few rows
  
  #Visualising the spread of articles by year
  df["year"].value_counts().sort_index().plot(kind="bar", figsize=(12, 4)),
  
  #Visualising the spread of articles by section
  df["section"].value_counts().head(10)

  return df

fetched_britney = fetch_guardian_articles() #Catch the list of articles returned by the function

table = to_dataframe(fetched_britney) #Pass the list of articles to the function to create a table

print(table)