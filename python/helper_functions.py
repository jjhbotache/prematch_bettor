from typing import List
from googlesearch import search
from levenshtein_distance import Levenshtein

def simplify_list(lista):
    return [elemento for sublista in lista for elemento in (simplify_list(sublista) if isinstance(sublista, list) else [sublista])]

def football_name_normalize(name:str):
    name_to_return = name.lower()
    
    words_to_remove = [
        "fc",
        "cf",
        "real",
        "athletic",
        "club",
        "sporting",
        "deportivo",
        "real",
        "cd",
        "ud",
        "sd",
        "cf",
        "city",
        "united",
        "-rj",
        "independiente",
        "Fcv",
        "Club deportivo",
        "vallecano",
        "de córdoba",
        "doradas",
        "county",
        "osc",
        "of"
    ]
    for word in words_to_remove:
        name_to_return = name_to_return.replace(word.lower(),"")
    return name_to_return.strip().capitalize()

def create_events_groups(events):
    events_sorted = sorted(events, key=lambda x: x.event_name)
    
    events_grouped = [
        [events_sorted[0]]
    ]
    
    max_distance = 7
    for event in events_sorted[1:]:
        if Levenshtein(
            football_name_normalize(event.event_name),
            football_name_normalize(events_grouped[-1][0].event_name)
            ).distance() < max_distance:
            events_grouped[-1].append(event)
        else:
            events_grouped.append([event])
        
    
    # print(*[e.event_name for e in events_sorted], sep="\n")
    for events in events_grouped:
        print(*[e.event_name for e in events], sep="\n")
        print("-"*80)
    return events_grouped
    
    # Dictionary to store grouped events
    event_groups = {}

    for event in events:
        # Find the most similar group
        best_match = None
        best_distance = float('inf')

        for group_id in event_groups:
            # Compare event_id without the bookmaker prefix using Levenshtein distance
            distance = levenshtein_distance(event.event_name, event_groups[group_id][0].event_name)
            if distance < best_distance:
                best_distance = distance
                best_match = group_id

        # If a similar group is found and the distance is small enough, add to that group
        if best_match and best_distance <= 3:  # Adjust threshold as needed
            event_groups[best_match].append(event)
        else:
            # Create a new group
            event_groups[event.event_id] = [event]


    # for each group, if 2 events are from the same bookmaker, remove the one of them
    for group_id, group in event_groups.items():
        bookmakers = set(event.bookmaker for event in group)
        if len(bookmakers) == 1:
            event_groups[group_id] = group[:1]
            
    # filter by the groups that have only 1 event
    event_groups = {group_id: group for group_id, group in event_groups.items() if len(group) > 1}
        
        
    print("Event groups:",event_groups)
    input()
    return event_groups


if __name__ == "__main__":
    pass    
