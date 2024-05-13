# in this file we will scrape the data from the website and store it in a json file
import requests
import bs4
from helper_functions import simplify_list

def scrape_wplay():
    page = requests.get("https://apuestas.wplay.co/es#upcoming-tab-FOOT")
    # print the page readable
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
    # filtrar por los que tengan <span class="inplay-banner-title">VIVO </span>
    prematch_events = [event for event in events if not event.find_all(name='span',attrs={"class":"inplay-banner-title"})]
    

    data=[]
    for event in prematch_events:
      odds = []
      try:
        mk_element = event.find(name='div',attrs={"class":"markets"})
        cols_elements = mk_element.find_all(name='td')
      except Exception as e:
        continue
      
      
      odds_elements = [
        {
          "odd":col.find("span",attrs={"class":"price dec"}).text,
          "name":col.find("span",attrs={"class":"seln-label"}).text.strip(),
        }
        for col in cols_elements
      ]
      data.append(odds_elements)
    # for each tab we will extract the data ()
    
    # print(*[tab.prettify() for tab in tabs],sep=f"\n{'-'*80}\n")
    print(*data,sep=f"\n{'-'*80}\n")
    # with open('wplay.html', 'w',encoding="utf-8") as f:
    #     f.write(page.content.decode('utf-8'))


    
def scrape_betplay():
  pass

def scrape_codere():
  pass

if __name__ == '__main__':
  scrape_wplay()