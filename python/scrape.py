# in this file we will scrape the data from the website and store it in a json file
import json
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

from .helper_functions import simplify_list
from .classes import Event,Bet,Bookmaker
from .constants.constants import DEBUG

import threading
import time

def timed_scrape(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func()
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
    return wrapper


# @timed_scrape
def scrape_wplay() -> list[Event]:
    """
    This function scrapes pre-match events from the Wplay website and returns a list of Event objects.

    Parameters:
    None

    Returns:
    list[Event]: A list of Event objects containing the scraped pre-match events.
    """
    # create a bookmaker obj
    wplay_bookmaker = Bookmaker("Wplay","https://apuestas.wplay.co/es#upcoming-tab-FOOT")
    
    page = requests.get(wplay_bookmaker.link)
    parsed_page = bs4.BeautifulSoup(page.content, 'html.parser')
    
    tabs = parsed_page.find_all(
      name='div',
      attrs={"class": ["fragment","expander"]}
    )
    # filter the tabs by the ones that haven't a class "wplay-footer"
    tabs = [tab for tab in tabs if not "wplay-footer" in tab["class"]]
    
    list_of_list_of_events = [
              tab.find_all(
                name='div',
                attrs={"class": ["mkt","mkt_content"]}
              ) 
              for tab in tabs]
    list_of_list_of_events = [list_of_events for list_of_events in list_of_list_of_events if list_of_events]
    events = simplify_list(list_of_list_of_events)
    # filtrar por los que tengan <span class="inplay-banner-title">VIVO </span> elimina los (envivo)
    prematch_events = [event for event in events if not event.find_all(name='span',attrs={"class":"inplay-banner-title"})]
    

    list_of_events = []
    
    
    for event in prematch_events:
      try:
        mk_element = event.find(name='div',attrs={"class":"markets"})
        cols_elements = mk_element.find_all(name='td')
        bet_dicts = [
          {
            "odd":col.find("span",attrs={"class":"price dec"}).text,
            "name":col.find("span",attrs={"class":"seln-label"}).text.strip(),
          }
          for col in cols_elements
        ]
        list_of_events.append(
          Event(
            bets=[
              Bet(
                bet_name=bet_dict["name"],
                bookmaker=wplay_bookmaker,
                odd=bet_dict["odd"]
              )
              for bet_dict in bet_dicts
            ]
          )
        )
      except Exception as e:
        if DEBUG:print(f"Error scraping event: {event}, error: {e}")
        continue
      
    if DEBUG:
      print("*"*80)
      print(f"Scraped {len(list_of_events)} events from Wplay:")
      if len(list_of_events) < 4:
        print(*list_of_events,sep=f"\n{'-'*80}\n")
      else:
        print(*list_of_events[:2],sep=f"\n{'-'*80}\n")
        print("...")
        print(*list_of_events[-2:],sep=f"\n{'-'*80}\n")
      print("*"*80)


    # write the data in a json file
    with open('wplay_events.json', 'w', ) as outfile:
      json.dump([event.dict() for event in list_of_events], outfile, indent=2, ensure_ascii=False)

    print("Scraped events from Wplay:", len(list_of_events))
    return list_of_events

# @timed_scrape
def scrape_betplay() -> list[Event]:
  # create a bookmaker obj
  betplay_bookmaker = Bookmaker("Betplay","https://betplay.com.co/apuestas#sports-hub/football")
  "https://na-offering-api.kambicdn.net/offering/v2018/betplay/listView/football/colombia/liga_betplay_dimayor/all/matches.json?lang=es_CO&market=CO&client_id=2&channel_id=1&ncid=1722807203096&useCombined=true&useCombinedLive=true"

  main_response = requests.get("https://na-offering-api.kambicdn.net/offering/v2018/betplay/event/live/open.json?lang=es_CO&market=CO&client_id=2&channel_id=1&ncid=1722807612994").json()
  
  football_groups_per_country = [ group for group in main_response["group"]["groups"] if group["englishName"] == "Football"][0]["groups"]
  
  
  leages_per_country = [
    {
      "leages":[l["termKey"] for l in g["groups"]],
      "country":g["termKey"]
    }
  for g in football_groups_per_country ]
  
  events = []  
  
  for list_of_leages in leages_per_country:
    for l in list_of_leages["leages"]:
      response = requests.get(f"https://na-offering-api.kambicdn.net/offering/v2018/betplay/listView/football/{list_of_leages['country']}/{l}/all/matches.json?lang=es_CO&market=CO&client_id=2&channel_id=1&ncid=1722808065781&category=12579").json()
      leage_events = [e for e in response["events"] if "liveData" not in e.keys() ]
      
      for e in leage_events:
        try: outcomes = e["betOffers"][0]["outcomes"]
        except: continue
        events.append(Event([
          Bet(
            bookmaker=betplay_bookmaker,
            bet_name=outcomes[0]["participant"],
            odd=outcomes[0]["odds"]/1000
          ),
          Bet(
            bookmaker=betplay_bookmaker,
            bet_name="Draw",
            odd=outcomes[1]["odds"]/1000
          ),
          Bet(
            bookmaker=betplay_bookmaker,
            bet_name=outcomes[2]["participant"],
            odd=outcomes[2]["odds"]/1000
          )
        ]))
  
  # write the data in a json file
  with open('betplay_events.json', 'w', ) as outfile:
    json.dump([event.dict() for event in events], outfile, indent=2, ensure_ascii=False)
  
  print("Scraped events from Betplay:", len(events))
  return events

# @timed_scrape
def scrape_codere() -> list[Event]:
  events = []
  def scrape_league_events(leage, local_bm):
    response = requests.get(f"https://m.codere.com.co/NavigationService/Home/GetEvents?parentId={leage['node_id']}&gameTypes=1")
    league_events = []
    for e in response.json():
        try:
            league_events.append(e["Games"][0])
        except:
            pass
    
    league_events = [
        Event([
            Bet(
                bookmaker=local_bm,
                bet_name=event["Results"][0]["Name"],
                odd=event["Results"][0]["Odd"]
            ),
            Bet(
                bookmaker=local_bm,
                bet_name="Draw",
                odd=event["Results"][1]["Odd"]
            ),
            Bet(
                bookmaker=local_bm,
                bet_name=event["Results"][2]["Name"],
                odd=event["Results"][2]["Odd"]
            )
        ])
        for event in league_events
    ]
    
    events.extend(league_events)
    
  local_bm = Bookmaker("Codere", "https://m.codere.com.co/deportesCol/#/HomePage")
  response = requests.get("https://m.codere.com.co/NavigationService/Home/GetCountries?parentid=358476322")
  countries = response.json()
  leages = [
      {
          "name": l[0]["Name"],
          "node_id": l[0]["NodeId"]
      }
      for l in [c["Leagues"] for c in countries]
  ]
  
  threads = []
  for leage in leages:
      thread = threading.Thread(target=scrape_league_events, args=(leage, local_bm))
      threads.append(thread)
      thread.start()

  for thread in threads:
      thread.join()
  
  # write on json file
  with open('codere_events.json', 'w', ) as outfile:
    json.dump([event.dict() for event in events], outfile, indent=2, ensure_ascii=False)
  
  print("Scraped events from Codere:", len(events))
  return events
    
    
if __name__ == '__main__':
  print("Scraping data from the bookmakers...")
  
  threads = [
    threading.Thread(target=scrape_wplay),
    threading.Thread(target=scrape_betplay),
    threading.Thread(target=scrape_codere),
  ]
  
  for thread in threads: thread.start()
  
  for thread in threads: thread.join()