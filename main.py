import multiprocessing


from python.scrape import *
from python.classes import EventsSet





def wrapper(func):
    return func()

send_msg = False                        

# Crear una lista de funciones a ejecutar
functions = [scrape_wplay, scrape_betplay, scrape_codere]
if send_msg:
    from python.telegram_functions import broadcast_msg

while True:
# Crear un pool de procesos
    with multiprocessing.Pool() as pool:
    # Mapear las funciones y ejecutarlas en paralelo
        results = pool.map(wrapper, functions)
    print("\n")
    
    combined_events = sum(results,[])
    similar_event_groups = [groups for groups in create_events_groups(combined_events) if len(groups) > 1]
    for events in similar_event_groups:
        print(*[e.event_name for e in events], sep="\n")
        print("-"*80)
        
    event_sets = [EventsSet(group) for group in similar_event_groups]
    sure_bets = [event_set for event_set in event_sets if event_set.is_sure_bet]
    sure_bets.sort(key=lambda x: x.profit, reverse=True)


    print("Sure bets found:", len(sure_bets))
    if sure_bets:
        msg_to_broadcast = "\n\n".join([str(s) for s in sure_bets[:20]])
        print(msg_to_broadcast)
        for _ in range(3):
            try:
                if send_msg:broadcast_msg(msg_to_broadcast)
                break
            except Exception:
                continue








