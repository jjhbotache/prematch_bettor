from typing import List
from googlesearch import search
from levenshtein_distance import Levenshtein
import unicodedata
import json


def load_events_from_json(json_file_path):
    """
    Given a JSON file path, loads the data and returns a list of Event objects.
    """
    from python.classes import Bet, Bookmaker, Event
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    events = []
    
    for event_data in data:
        # Create the bookmaker object
        bookmaker_data = event_data["bookmaker"]
        bookmaker = Bookmaker(bookmaker_data["name"], bookmaker_data["link"])
        
        # Create the list of bets for the event
        bets = []
        for bet_data in event_data["bets"]:
            bet = Bet(
                bookmaker=bookmaker, 
                bet_name=bet_data["bet_name"], 
                odd=bet_data["odd"]
            )
            bets.append(bet)
        
        # Create the event object
        event = Event(bets=bets)
        events.append(event)
    
    return events
 
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def simplify_list(lista):
    return [elemento for sublista in lista for elemento in (simplify_list(sublista) if isinstance(sublista, list) else [sublista])]

def football_name_normalize(name:str):
    name_to_return = name.lower()
    
    words_to_remove = [
        "-",
        " ",
        "(",
        ")",
        "21",
        "cd",
        "cf",
        "club",
        "county",
        "córdoba",
        "de",
        "deportivo",
        "deportes",
        "doradas",
        "fc",
        "Fc",
        "Fcv",
        "independiente",
        "osc",
        "rj",
        "sd",
        "sub",
        "sporting",
        "ud",
        "Universidad técnica",
        "united",
        "21",
        "22",
        "23",
        "Reserves",
        "vallecano",
        
    ]
    for word in words_to_remove:
        name_to_return = name_to_return.replace(word.lower(),"")
        
    name_to_return = remove_accents(name_to_return)
    return name_to_return.strip().capitalize()

def create_events_groups(events, max_distance=5):
    from python.classes import Event
    events_sorted = sorted(events, key=lambda x: football_name_normalize(x.event_name))
    
    events_grouped:List[Event] = [
        [events_sorted[0]]
    ]
    
    for event in events_sorted[1:]:
        if Levenshtein(
            football_name_normalize(event.event_name),
            football_name_normalize(events_grouped[-1][0].event_name)
            ).distance() < max_distance:
            events_grouped[-1].append(event)
        else:
            events_grouped.append([event])
    
    # print the groups
    
    # input("Press enter to continue")
    
    return events_grouped
    


if __name__ == "__main__":
    pass    
