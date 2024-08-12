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


if __name__ == "__main__":
    print(
        levenshtein_distance("holaa", "holasa") # 1
    )

if __name__ == "__main__":
    print(
        levenshtein_distance("holaa", "holasa") # 1
    )

