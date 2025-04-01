def _counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    # Contar ocurrencias del dígito actual
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    
    # Acumular el conteo
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Construir array de salida
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    
    # Copiar al array original
    for i in range(n):
        arr[i] = output[i]