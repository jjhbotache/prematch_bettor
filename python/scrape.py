# in this file we will scrape the data from the website and store it in a json file
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
  # create a bookmaker obj
  betplay_bookmaker = Bookmaker("Betplay","https://betplay.com.co/apuestas#sports-hub/football")
  # Configurar opciones de Edge headless
  edge_options = Options()
  if not DEBUG:
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")

  driver = webdriver.Edge(options=edge_options)
  wait = WebDriverWait(driver, 10)  # wait up to 10 seconds
  driver.implicitly_wait(10)
  driver.get(betplay_bookmaker.link)
  
  def get_leages():
    # wait for the page to load
    driver.find_element(By.XPATH,"//p[contains(text(), 'Ligas principales')]")
    # get all the divs with the attribute "data-touch-feedback=true"
    leages_divs = driver.find_elements(By.CSS_SELECTOR, "div[data-touch-feedback='true']")
    leages_divs.append(driver.find_element(By.CSS_SELECTOR,"div.sc-ckEbSK.dfONcu"))
    divs_to_exclude = [ "Fichajes", "Premios Internacionales","Especiales" ]
    leages_divs = [leage for leage in leages_divs if not leage.text in divs_to_exclude]
    return leages_divs
  
  leages_divs = get_leages()
  leages_names_to_scrape = [leage.text for leage in leages_divs]
  leages_visited = []
  events = []
  
  while len(leages_names_to_scrape)>0:
    driver.get(betplay_bookmaker.link)
    leages_divs = get_leages()
    
    try:
      leage = [leage for leage in leages_divs if not leage.text in leages_visited][0]
      leages_visited.append(leage.text)
    except IndexError:
      print("ended")
      break
    except Exception as e:
      print("There was an error while trying to get the leage, skipping...")
      print("❌")
      continue
      
      
    if DEBUG:print(f"Scraping {leage.text}...",end="")
    try: leage.click()  
    except Exception as e:
      try: 
        if DEBUG: print("\nThere was an error while trying to click the leage, trying again...")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.sc-ckEbSK.dfONcu')))
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-touch-feedback='true']")))
        leage.click()
        
      except Exception as e:
        print("There was an error while trying to click the leage, skipping...")
        print("❌")
        continue
      
      
    events_lis = driver.find_elements(By.CSS_SELECTOR, "li.KambiBC-sandwich-filter__event-list-item")
    # for each li, create an event ands store it in a list
    for li in events_lis:
      teams = li.find_element(By.CSS_SELECTOR,"div.KambiBC-sandwich-filter__event-detail").text.split("\n")
      odds = li.find_elements(By.CSS_SELECTOR,"button.sc-bcXHqe.bIpOnq.sc-ipEyDJ.jhSst.KambiBC-betty-outcome")
      events.append(Event([
        Bet(
          bookmaker=betplay_bookmaker,
          bet_name=teams[0],
          odd=float(odds[0].text)
        ),
        Bet(
          bookmaker=betplay_bookmaker,
          bet_name="Draw",
          odd=float(odds[1].text)
        ),
        Bet(
          bookmaker=betplay_bookmaker,
          bet_name=teams[1],
          odd=float(odds[2].text)
        )        
      ]))
    if DEBUG:print("✅ Done!",)
     
  print(*events,sep="\n")
  
  # with open("betplay.html","w") as file: file.write(parsed_page.prettify())
  input("continue"); driver.close()

def scrape_codere():
  pass

if __name__ == '__main__':
  scrape_betplay()