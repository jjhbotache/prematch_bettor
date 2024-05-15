# in this file we will scrape the data from the website and store it in a json file
import requests
import bs4
from helper_functions import simplify_list
from classes import Event,Bet,Bookmaker
from constants.constants import DEBUG

def scrape_wplay():
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
      except Exception as e:
        continue
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


    
def scrape_betplay():
  pass

def scrape_codere():
  pass

if __name__ == '__main__':
  scrape_wplay()