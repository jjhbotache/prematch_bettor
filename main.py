import multiprocessing

import threading

from python.scrape import *
from python.classes import EventsSet
from python.telegram_functions import broadcast_msg
import Levenshtein
from itertools import combinations



def get_event_groups(events, threshold=5, group_size=2):
    groups = []
    for group in combinations(events, group_size):
        distances = [Levenshtein.distance(group[i].event_name, group[j].event_name) 
                     for i in range(len(group)) for j in range(i + 1, len(group))]
        if all(distance <= threshold for distance in distances):
            groups.append(group)
    return groups

def wrapper(func):
    return func()


# Crear una lista de funciones a ejecutar
functions = [scrape_wplay, scrape_betplay, scrape_codere]


while True:
# Crear un pool de procesos
    with multiprocessing.Pool() as pool:
    # Mapear las funciones y ejecutarlas en paralelo
        results = pool.map(wrapper, functions)
    print("\n")
    
    similar_event_groups = get_event_groups(sum(results,[]), threshold=5)
    event_sets = [EventsSet(group) for group in similar_event_groups]
    sure_bets = [event_set for event_set in event_sets if event_set.is_sure_bet]

    msg_to_broadcast = "\n\n".join([str(s) for s in sure_bets])
    broadcast_msg(msg_to_broadcast)








