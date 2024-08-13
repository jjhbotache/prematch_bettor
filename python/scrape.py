# in this file we will scrape the data from the website and store it in a json file
import json
import requests
import bs4
import time

from .helper_functions import create_events_groups, simplify_list
from .classes import Event,Bet,Bookmaker
from .constants.constants import DEBUG

import threading
import time
import concurrent.futures

save_on_json = False

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
    try:
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

      if save_on_json:
        # write the data in a json file
        with open('wplay_events.json', 'w', ) as outfile:
          try:
            json.dump([event.dict() for event in list_of_events], outfile, indent=2, ensure_ascii=False)
          except Exception as e:
            if DEBUG:print(f"Error writing the json file: {e}")

      print("Scraped events from Wplay:", len(list_of_events))
      return list_of_events
    
    except Exception as e:
      print(f"Error scraping Wplay: {e}")
      return []

# @timed_scrape
def scrape_betplay() -> list[Event]:
  try:
    # create a bookmaker obj
    betplay_bookmaker = Bookmaker("Betplay","https://betplay.com.co/apuestas#sports-hub/football")
    events = []
    
    main_url_petition = "https://graphql.kambicdn.com/"
    headers = {
          "Authorization": "kambi",
          "Content-Type": "application/json"
      }
    query = """
          query getGroups($sport: String!, $offering: String!, $market: String!, $language: String!) {
              groups(
                  sport: $sport
                  groupInternationalGroups: true
                  addAllSubGroupsToTopLeagues: true
                  offering: $offering
                  market: $market
                  language: $language
              ) {
                  groups {
                      name
                      level
                      id
                      countryCode
                      abbreviation
                      path
                      groups {
                          name
                          id
                          level
                          path
                      }
                  }
                  topLeagues {
                      id
                      name
                      sortOrder
                      countryCode
                      path
                  }
              }
          }
      """
    variables = {
          "sport": "football",
          "offering": "betplay",
          "market": "CO",
          "language": "es_CO"
      }
    payload = {
          "query": query,
          "variables": variables
      }
    
    response = requests.post(main_url_petition, headers=headers, json=payload)
    
    important_paths_lists = [
      [league["path"] for league in group["groups"]] for group in response.json()["data"]["groups"]["groups"]
    ]
    paths = simplify_list(important_paths_lists)
    
    
    # for each path, get the events
    
    for path in paths:
      if len(path.split("/"))<3:continue
      for attemp in range(3):
        try:
          response = requests.get(f"https://na-offering-api.kambicdn.net/offering/v2018/betplay/listView/{path}/all/matches.json?lang=es_CO&market=CO&client_id=2&channel_id=1&ncid=1723476962160&useCombined=true&useCombinedLive=true")
          data = response.json()
          break
        except Exception as e:
          time_to_wait = 2 ** (attemp)
          print(f"Error retrieving data from API: {e}, waiting {time_to_wait} seconds")
          time.sleep(time_to_wait )
      else:
        raise Exception("Failed to retrieve data from API after 3 attempts")
      events_from_quey = data["events"]
      for event_from_quey in events_from_quey:
        try:
          bets = [e["outcomes"] for e in event_from_quey["betOffers"] if e["betOfferType"]["id"] == 2][0]
          parsed_bets = [
            Bet(
              bookmaker=betplay_bookmaker,
              bet_name=bet.get("participant", "Draw"),
              odd=bet["odds"]/1000
            )
            for bet in bets
          ]
          events.append(Event(parsed_bets))
        except Exception as e:
          if DEBUG:print(f"Error creating the event: {e}")
          continue
    

    if save_on_json:
      # write the data in a json file
      with open('betplay_events.json', 'w', ) as outfile:
        try:
          json.dump([event.dict() for event in events], outfile, indent=2, ensure_ascii=False)
        except Exception as e:
          if DEBUG:print(f"Error writing the json file: {e}")
      
    print("Scraped events from Betplay:", len(events))
    return events
  
  except Exception as e:
    print(f"Error scraping Betplay: {e}")
    return []

# @timed_scrape
def scrape_codere() -> list[Event]:
  try:
    events = []
    def scrape_league_events(leage, local_bm):
      response = requests.get(f"https://m.codere.com.co/NavigationService/Home/GetEvents?parentId={leage['node_id']}&gameTypes=1").json()
      league_events = []
      for e in response:
        if e["isLive"] or e["SportName"] != "Fútbol": continue
        try:
          game_results = e["Games"][0]["Results"]
          bets = [
            Bet(
              bookmaker=local_bm,
              bet_name=r["Name"],
              odd=r["Odd"]
            ) for r in game_results]
          league_events.append(Event(bets))
        except Exception as e:
          if DEBUG:print(f"Error creating the event: {e}")
          continue

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
    
    if save_on_json:
      # write on json file
      with open('codere_events.json', 'w', ) as outfile:
        try:
          json.dump([event.dict() for event in events], outfile, indent=2, ensure_ascii=False)
        except Exception as e:
          if DEBUG:print(f"Error writing the json file: {e}")
      
    print("Scraped events from Codere:", len(events))
    return events
  
  except Exception as e:
    print(f"Error scraping Codere: {e}")
    return []
    
    
if __name__ == '__main__':
  print("Scraping data from the bookmakers...")
  while True:
    print("Scraping betplay...")
    scrape_betplay()
  with concurrent.futures.ThreadPoolExecutor() as executor:
    wplay_future = executor.submit(scrape_wplay)
    betplay_future = executor.submit(scrape_betplay)
    codere_future = executor.submit(scrape_codere)

    events = [
      *wplay_future.result(),
      *betplay_future.result(),
      *codere_future.result(),
    ]
  
  events_sets = create_events_groups(events)
  input()
  
  
  