def simplify_list(lista):
    return [elemento for sublista in lista for elemento in (simplify_list(sublista) if isinstance(sublista, list) else [sublista])]

def levenshtein_distance(str1, str2):
    # Inicializar la matriz de distancias
    dp = [[0 for _ in range(len(str2) + 1)] for _ in range(len(str1) + 1)]
    
    # Llenar la primera fila y columna
    for i in range(len(str1) + 1):
        dp[i][0] = i
    for j in range(len(str2) + 1):
        dp[0][j] = j
    
    # Llenar la matriz utilizando la fórmula de Levenshtein
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No se necesita operación
            else:
                dp[i][j] = min(dp[i - 1][j] + 1,    # Eliminación
                               dp[i][j - 1] + 1,    # Inserción
                               dp[i - 1][j - 1] + 1)  # Sustitución
    
    # La distancia de Levenshtein es el valor en la esquina inferior derecha de la matriz
    return dp[len(str1)][len(str2)]

if __name__ == "__main__":
    print(
        levenshtein_distance("holaa", "holasa") # 1
    )

