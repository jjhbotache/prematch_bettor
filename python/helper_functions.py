from typing import List

def simplify_list(lista):
    return [elemento for sublista in lista for elemento in (simplify_list(sublista) if isinstance(sublista, list) else [sublista])]

def levenshtein_distance(str1, str2):
    # Verificación de tipos
    if not isinstance(str1, str) or not isinstance(str2, str):
        raise TypeError("Ambos argumentos deben ser strings")

    # Aseguramos que str1 sea la cadena más corta para minimizar el uso de memoria
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    # Inicializar la fila previa
    previous_row = range(len(str2) + 1)

    # Iterar sobre cada carácter de str1
    for i, c1 in enumerate(str1, 1):
        current_row = [i]
        for j, c2 in enumerate(str2, 1):
            insertions = previous_row[j] + 1
            deletions = current_row[j - 1] + 1
            substitutions = previous_row[j - 1] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def create_events_sets(events):
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
        
    return event_groups



if __name__ == "__main__":
    print(
        levenshtein_distance("holaa", "holasa") # 1
    )

