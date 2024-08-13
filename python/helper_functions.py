from typing import List
from googlesearch import search
from levenshtein_distance import Levenshtein
import unicodedata

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

def create_events_groups(events):
    events_sorted = sorted(events, key=lambda x: football_name_normalize(x.event_name))
    
    events_grouped = [
        [events_sorted[0]]
    ]
    
    max_distance = 5
    for event in events_sorted[1:]:
        if Levenshtein(
            football_name_normalize(event.event_name),
            football_name_normalize(events_grouped[-1][0].event_name)
            ).distance() < max_distance:
            events_grouped[-1].append(event)
        else:
            events_grouped.append([event])
    
    # print the groups
    # for group in events_grouped:
    #     print("*"*100)
    #     for event in group:
    #         print(event.event_name)
    # input("Press enter to continue")
    
    return events_grouped
    


if __name__ == "__main__":
    pass    
