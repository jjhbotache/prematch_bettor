def simplify_list(lista):
    return [elemento for sublista in lista for elemento in (simplify_list(sublista) if isinstance(sublista, list) else [sublista])]
